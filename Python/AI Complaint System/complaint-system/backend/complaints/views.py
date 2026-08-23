import os

from django.shortcuts import render
from django.http import HttpResponse
import easyocr
from groq import Groq
from complaints.services.prompts import ComplaintService
from django.conf import settings 
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import View
import json 
import pymupdf
from datetime import datetime
from django.http import JsonResponse
from .models import Complaint
from django.utils.dateparse import parse_date
from decimal import Decimal, InvalidOperation
import ollama
from django.http import HttpResponse


@method_decorator(csrf_exempt, name="dispatch")
class ComplaintView(View):
    KEEP_ALIVE = "5m"

    def post(self, request):
        print("i am here")
        data = ""

        if request.content_type and "multipart/form-data" in request.content_type:
            data = request.POST.get("text", "").strip()
            uploaded_file = request.FILES.get("file")

            if uploaded_file:
                if uploaded_file.name.endswith(".pdf"):
                    data += extract_text_from_pdf(uploaded_file)
                else:
                    data += image(uploaded_file)
                    print(data)

        system_prompt = ComplaintService.get_knowledge_base()
        user_input = f"""
<USER_QUESTION>
MY COMPLAINT IS {data}
</USER_QUESTION>
"""

        # Query local Ollama instance
        response = ollama.chat(
            model="qwen3:8b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input},
            ],
            format="json",
            think=False,
            keep_alive=self.KEEP_ALIVE,
        )

        output_text = response["message"]["content"].strip()
        print("output_text",output_text)
        return HttpResponse(output_text)

    def get(self,request):
        context={"API_URL":settings.API_URL}
        return render(request, 'index.html',context)

reader = easyocr.Reader(['en'],gpu=False) 

def image(uploaded_file):
    
    # Read text from an image file path or a numpy array/OpenCV image
    results = reader.readtext(uploaded_file.read(), detail=0)

    # Combine extracted lines
    extracted_text = " ".join(results)
    return extracted_text

def extract_text_from_pdf(uploaded_file):
  pdf_bytes = uploaded_file.read()

  doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")

  extracted_text = ""
  for page in doc:
    extracted_text += page.get_text()

  doc.close()
  return extracted_text.strip()



DATE_FORMATS = ["%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%m/%d/%Y", "%d %b %Y", "%d %B %Y"]


def to_date(value):
    if value in (None, "", "null"):
        return None
    if isinstance(value, str):
        parsed = parse_date(value)
        if parsed:
            return parsed
        for fmt in DATE_FORMATS:
            try:
                return datetime.strptime(value.strip(), fmt).date()
            except ValueError:
                continue
    return None


def to_decimal(value):
    if value in (None, "", "null"):
        return None
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError):
        return None


def to_bool(value):
    if isinstance(value, bool):
        return value
    s = str(value).strip().lower()
    return s in ("true", "yes", "y", "1")


def to_list(value):
    if isinstance(value, list):
        return value
    if isinstance(value, str) and value.strip():
        return [v.strip() for v in value.split(",") if v.strip()]
    return []


def to_str(value):
    if value in (None, "null"):
        return None
    return str(value).strip() or None


@method_decorator(csrf_exempt, name="dispatch")
class SaveComplaintView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        complaint_id = to_str(data.get("complaint_id")) or f"CMP-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        com= Complaint.objects.filter(complaint_id=complaint_id).first()
        if com:
            print("Complaint with this ID already exists.")
            return JsonResponse({"error": "Complaint with this ID already exists."}, status=400)
            

        try:
            complaint = Complaint.objects.create(
                complaint_id=complaint_id,
                complaint_date=to_date(data.get("complaint_date")),
                source=to_str(data.get("source")),
                customer=to_str(data.get("customer")),
                api_name=to_str(data.get("api_name")),
                api_code=to_str(data.get("api_code")),
                batch_lot_no=to_str(data.get("batch_lot_no")),
                manufacturing_date=to_date(data.get("manufacturing_date")),
                retest_date=to_date(data.get("retest_date")),
                quantity_supplied=to_decimal(data.get("quantity_supplied")),
                quantity_affected=to_decimal(data.get("quantity_affected")),
                complaint_category=to_str(data.get("complaint_category")),
                complaint_description=to_str(data.get("complaint_description")),
                specification=to_str(data.get("specification")),
                customer_result=to_str(data.get("customer_result")),
                coa_no=to_str(data.get("coa_no")),
                sample_available=to_bool(data.get("sample_available")),
                investigation_root_cause=to_str(data.get("investigation_root_cause")),
                impacted_batches=to_list(data.get("impacted_batches")),
                capa_required=to_bool(data.get("capa_required")),
                capa_id=to_str(data.get("capa_id")),
                final_conclusion_disposition=to_str(data.get("final_conclusion_disposition")),
                qa_approval_closure=to_bool(data.get("qa_approval_closure")),
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

        return JsonResponse(
            {"message": "Complaint saved successfully!", "id": complaint.id, "complaint_id": complaint.complaint_id},
            status=201,
        )