# These videos are the proof of how the project is working
Input 1,2,3
# GO INSIDE THE COMPLAINT FOLDER THERE U WILL FIND THE MAIN CODE 

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Quality Complaint Management System

An AI-powered **Quality Complaint Management System** built with Django.

The system helps users create pharmaceutical/API quality complaints. Instead of entering every field manually, users can provide complaint information through text or upload supported documents/images. The system extracts the information using OCR/document processing and a local AI model, then automatically fills the complaint form.

---

## Features

### 1. Manual Complaint Entry

Users can manually enter complaint information through the complaint form.

The form contains sections for:

* General Information
* Product & Manufacturing Information
* Complaint Details
* Investigation & CAPA
* Disposition & Closure

---

### 2. AI-Based Complaint Extraction

Users can type complaint information into the AI Assistant.

The AI reads the complaint text and extracts structured information such as:

* Complaint ID
* Complaint date
* Customer
* API name
* API code
* Batch/Lot number
* Manufacturing date
* Retest date
* Quantity supplied
* Quantity affected
* Complaint category
* Complaint description
* Specification
* Customer result
* CoA number
* Sample availability
* Investigation/root cause
* Impacted batches
* CAPA information
* Final conclusion/disposition
* QA approval/closure

The extracted information is then automatically filled into the complaint form.

---

### 3. Image OCR

Users can upload an image containing complaint information.

The project uses **EasyOCR** to extract text from the image.

The extracted text is then passed to the local AI model for structured extraction.

---

### 4. PDF Text Extraction

Users can upload a PDF complaint document.

The project uses **PyMuPDF** to extract text from the PDF.

The extracted text is then processed by the AI model.

> **Current implementation:** PDF files are processed using PyMuPDF. Image files are processed using EasyOCR.

---

### 5. Save Complaint

After reviewing the automatically populated form, the user can click:

**Save Record**

The complaint data is sent to Django as JSON and stored in the PostgreSQL database.

---

### 6. Local AI Model

The project uses **Ollama** to run the AI model locally.

Current model:

```text
qwen3:8b
```

The model runs locally rather than requiring the complaint text to be sent to an external LLM service.

---

# Technology Stack

## Backend

* Python
* Django
* Django REST Framework
* PostgreSQL
* Django CORS Headers

## AI

* Ollama
* Qwen3 8B

## OCR & Document Processing

* EasyOCR
* PyMuPDF
* Pillow
* OpenCV
* PyTorch
* Torchvision

## Frontend

* HTML
* CSS
* JavaScript

The frontend is integrated into the Django project.

---

# Project Structure

The main project structure is:

```text
backend/
│
├── complaints/
│   ├── migrations/
│   ├── services/
│   │   └── prompts.py
│   │
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── ...
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── ...
│
├── templates/
│   └── index.html
│
├── .env
├── manage.py
├── requirements.txt
└── db.sqlite3
```

> **Note:** The provided `settings.py` is configured to use **PostgreSQL**, not SQLite. Therefore, PostgreSQL must be configured correctly for the current application settings.

---

# How the Project Works

The basic flow is:

```text
User
  │
  ├── Manually enters complaint
  │
  ├── Types complaint into AI Assistant
  │
  └── Uploads image/PDF
          │
          ▼
     Django Backend
          │
          ├── Image → EasyOCR
          │
          ├── PDF → PyMuPDF
          │
          └── Text → Ollama
                    │
                    ▼
                 qwen3:8b
                    │
                    ▼
             Structured JSON
                    │
                    ▼
             Complaint Form
                    │
                    ▼
              Save Complaint
                    │
                    ▼
               PostgreSQL
```

---

# Requirements

Before running the project, install:

* Python
* PostgreSQL
* Ollama
* Git (if cloning the project)

The Python dependencies are listed in `requirements.txt`.

---

# 1. Clone the Project

If the project is stored in GitHub, clone it:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

Move into the project folder:

```bash
cd <PROJECT_FOLDER>
```

---

# 2. Create a Virtual Environment

It is recommended to create a Python virtual environment.

### Windows

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

After activation, the terminal should show something similar to:

```text
(venv)
```

---

# 3. Install Python Dependencies

Install all required packages:

```bash
pip install -r requirements.txt
```

The project uses packages including:

```text
Django
python-dotenv
django-cors-headers
psycopg2-binary
ollama
PyMuPDF
Pillow
requests
easyocr
opencv-python-headless
torch
torchvision
gunicorn
```

---

# 4. Environment Variables

Create a `.env` file in the main project folder.

The project uses the following environment values:

```env
Groq_API_KEY="xyz"
API_URL=http://127.0.0.1:8000/complaint/call/
```

### Important

The value:

```text
xyz
```

is only a placeholder.

Do **not** put real API keys, passwords, secret keys, database passwords, or other sensitive information in the README or public GitHub repository.

Also make sure `.env` is added to `.gitignore`:

```text
.env
```

---

# 5. PostgreSQL Setup

The current `settings.py` is configured for PostgreSQL.

The application expects a PostgreSQL database with the following configuration structure:

```text
Database engine: PostgreSQL
Database name: complaint-system
Host: localhost
Port: 5432
```

Your local PostgreSQL username and password should be configured privately on your own machine.

### Important Security Rule

Do not copy real database passwords into:

* GitHub
* README files
* screenshots
* public documentation
* source code

Use your own local PostgreSQL credentials.

---

# 6. Run Django Migrations

After configuring PostgreSQL, run:

```bash
python manage.py makemigrations
```

Then:

```bash
python manage.py migrate
```

This creates/updates the required database tables.

The complaint model uses the database table:

```text
complaints
```

---

# 7. Set Up Ollama

The AI functionality requires **Ollama to be installed and running locally**.

The project currently uses:

```text
qwen3:8b
```

Make sure the model is available in Ollama before using the AI Assistant.

Verify that Ollama can see the model:

```bash
ollama list
```

You should see:

```text
qwen3:8b
```

If the model has not been downloaded yet, download the required model using Ollama:

```bash
ollama pull qwen3:8b
```

Then make sure Ollama is running.

The Django application communicates with the local Ollama service when a complaint is submitted to the AI Assistant.

---

# 8. Start the Django Server

Run:

```bash
python manage.py runserver 127.0.0.1:8000
```

The application will then be available at:

```text
http://127.0.0.1:8000/
```

---

# Important: Localhost Configuration

This is important if you are new to Django.

The frontend currently has default API URLs pointing to:

```text
http://127.0.0.1:8000
```

Specifically:

### AI Complaint API

```text
http://127.0.0.1:8000/complaint/call/
```

### Save Complaint API

```text
http://127.0.0.1:8000/complaint/save-complaint/
```

The frontend uses these URLs to communicate with the Django backend.

---

## Why is `127.0.0.1:8000` important?

`127.0.0.1` means:

```text
Your own computer
```

Port `8000` is the port where Django is expected to run.

So:

```text
http://127.0.0.1:8000
```

means:

```text
Django running on my own computer on port 8000
```

---

## What if Django is running on another port?

For example, if you start Django with:

```bash
python manage.py runserver 127.0.0.1:8001
```

then Django is running at:

```text
http://127.0.0.1:8001
```

But the frontend is still configured to send requests to:

```text
http://127.0.0.1:8000
```

Therefore, the AI Assistant and Save functionality may fail.

If you change the Django port, update the API URL configuration accordingly.

---

# URL Structure

The project-level URL configuration includes the complaints application:

```python
path('complaint/', include('complaints.urls'))
```

The complaint application's URLs are:

```python
path('call/', views.ComplaintView.as_view(), name='xyz')
path('', views.ComplaintView.as_view(), name='index')
path('save-complaint/', views.SaveComplaintView.as_view(), name='save_complaint')
```

Therefore, the main API endpoints are:

| Purpose                 | URL                                               |
| ----------------------- | ------------------------------------------------- |
| Complaint page          | `http://127.0.0.1:8000/complaint/`                |
| AI complaint processing | `http://127.0.0.1:8000/complaint/call/`           |
| Save complaint          | `http://127.0.0.1:8000/complaint/save-complaint/` |
| Django admin            | `http://127.0.0.1:8000/admin/`                    |

---

# How to Use the Application

## Step 1 — Open the Application

After starting Django, open:

```text
http://127.0.0.1:8000/complaint/
```

---

## Step 2 — Enter Complaint Information

There are two ways to provide complaint information.

### Option A — Enter information manually

Fill the complaint form yourself.

### Option B — Use the AI Assistant

Use the AI Assistant on the right side of the screen.

You can type complaint information into the chat box.

---

# Uploading a File

The current frontend supports:

```text
Images
PDF files
```

The file input currently accepts:

```text
image/*
application/pdf
```

### Image

For an image:

```text
Image
  ↓
EasyOCR
  ↓
Extracted text
  ↓
Ollama
  ↓
Structured JSON
  ↓
Form fields
```

### PDF

For a PDF:

```text
PDF
  ↓
PyMuPDF
  ↓
Extracted text
  ↓
Ollama
  ↓
Structured JSON
  ↓
Form fields
```

> **Important:** Word document support is not confirmed by the current frontend/backend code provided for this project. The current implementation explicitly supports images and PDFs.

---

# How AI Auto-Fill Works

The AI response is expected to contain structured JSON.

For example:

```json
{
    "complaint_id": "CMP-001",
    "customer": "Example Customer",
    "api_name": "Paracetamol",
    "batch_lot_no": "BATCH-001",
    "sample_available": true,
    "capa_required": false
}
```

The frontend reads the returned JSON and matches the keys with the form fields.

The frontend also contains field aliases so that different naming styles can be recognized.

For example:

```text
complaint_id
Complaint ID
complaintId
```

can be normalized and matched to the same complaint field.

---

# Saving a Complaint

After reviewing the automatically populated information:

1. Check the complaint information.
2. Make any required changes.
3. Click **Save Record**.
4. The frontend sends the form data to:

```text
http://127.0.0.1:8000/complaint/save-complaint/
```

The backend then creates a complaint record in PostgreSQL.

---

# Complaint ID

If the user does not provide a complaint ID, the backend automatically generates one using the current date and time.

The format is:

```text
CMP-YYYYMMDDHHMMSS
```

For example:

```text
CMP-20260826143025
```

If the same complaint ID already exists, the system rejects the new complaint.

---

# AI Prompt / Knowledge Base

The AI extraction instructions are stored in:

```text
complaints/
└── services/
    └── prompts.py
```

The `ComplaintService` contains the knowledge base used by the AI.

The knowledge base instructs the AI to:

* Extract only information available in the complaint.
* Not invent missing information.
* Return `null` when information is unavailable.
* Return an empty array for missing impacted batches.
* Preserve batch/lot numbers.
* Correctly handle boolean fields.
* Distinguish customer test results from manufacturer specifications.
* Avoid treating assumptions as confirmed root causes.
* Return a single valid JSON object.

---

# Complaint Database Model

The main Django model is:

```text
Complaint
```

It contains information for:

### Identification

```text
complaint_id
complaint_date
source
customer
```

### Product / API

```text
api_name
api_code
batch_lot_no
manufacturing_date
retest_date
```

### Quantities

```text
quantity_supplied
quantity_affected
```

### Complaint / Quality Analysis

```text
complaint_category
complaint_description
specification
customer_result
coa_no
sample_available
```

### Investigation / CAPA

```text
investigation_root_cause
impacted_batches
capa_required
capa_id
```

### Conclusion / Closure

```text
final_conclusion_disposition
qa_approval_closure
```

### Timestamps

```text
created_at
updated_at
```

---

# Troubleshooting

## 1. AI Assistant is not working

First check that Django is running:

```bash
python manage.py runserver 127.0.0.1:8000
```

Then check that Ollama is running and that the model exists:

```bash
ollama list
```

Make sure:

```text
qwen3:8b
```

is available.

---

## 2. Connection Error / Failed to Fetch

Check the API URL.

The frontend expects:

```text
http://127.0.0.1:8000/complaint/call/
```

Make sure Django is actually running on:

```text
127.0.0.1:8000
```

---

## 3. Save Record does not work

Check that the Django server is running.

Then verify the save endpoint:

```text
http://127.0.0.1:8000/complaint/save-complaint/
```

Also check that PostgreSQL is running and that the database configuration in `settings.py` is correct.

---

## 4. PostgreSQL Connection Error

If Django shows a PostgreSQL connection error, check:

* PostgreSQL is installed.
* PostgreSQL service is running.
* Database exists.
* Database name is correct.
* Username is correct.
* Password is correct.
* PostgreSQL is listening on port `5432`.

Do not put your actual database password in GitHub or this README.

---

## 5. `qwen3:8b` Not Found

If Ollama reports that the model is not available, check:

```bash
ollama list
```

If it is missing, download it:

```bash
ollama pull qwen3:8b
```

Then restart/recheck Ollama if necessary.

---

## 6. OCR Problems

For image uploads, the project uses:

```text
EasyOCR
```

The current OCR reader is configured for:

```text
English
```

and uses CPU processing.

Poor-quality or difficult-to-read images may produce incomplete OCR text.

---

## 7. PDF Text Is Empty or Incomplete

PDF processing uses PyMuPDF.

The current implementation extracts text directly from PDF pages.

If the PDF contains scanned images rather than selectable text, the current PDF path may not extract the text as expected because the provided implementation uses PDF text extraction rather than OCR for PDF pages.

---

# Debug Mode

The frontend contains a debug mode that can help identify AI-response problems.

When debug mode is enabled, the application can display information such as:

* Raw AI response
* Parsed JSON keys
* Selected fill target
* Updated fields
* Unmatched fields

This can help determine whether a problem is caused by:

```text
AI response
      ↓
JSON parsing
      ↓
Field matching
      ↓
Form auto-fill
```

---

# API Overview

## AI Complaint API

### Endpoint

```text
POST /complaint/call/
```

Full local URL:

```text
http://127.0.0.1:8000/complaint/call/
```

### Request

The endpoint accepts:

```text
multipart/form-data
```

It can contain:

```text
text
file
```

The file can be an image or PDF according to the current frontend implementation.

### Processing

```text
Text/File
   ↓
OCR or PDF extraction
   ↓
Complaint text
   ↓
ComplaintService knowledge base
   ↓
Ollama qwen3:8b
   ↓
JSON response
```

---

# Save Complaint API

### Endpoint

```text
POST /complaint/save-complaint/
```

Full local URL:

```text
http://127.0.0.1:8000/complaint/save-complaint/
```

### Request

The endpoint expects JSON containing complaint fields.

### Successful Response

The backend returns information including:

```json
{
    "message": "Complaint saved successfully!",
    "id": 1,
    "complaint_id": "CMP-001"
}
```

---

# Common Startup Checklist

Every time you want to run the project locally:

### 1. Activate virtual environment

```bash
venv\Scripts\activate
```

### 2. Make sure PostgreSQL is running

Check that your PostgreSQL database is available.

### 3. Make sure Ollama is running

Check the model:

```bash
ollama list
```

Make sure:

```text
qwen3:8b
```

is available.

### 4. Start Django

```bash
python manage.py runserver 127.0.0.1:8000
```

### 5. Open the application

```text
http://127.0.0.1:8000/complaint/
```

---

# Important Configuration Notes

## Django Version

The provided `settings.py` was generated for:

```text
Django 6.1
```

However, the provided `requirements.txt` currently specifies:

```text
Django>=4.2,<6.0
```

These two files have a **version mismatch**.

Before installing dependencies for a fresh setup, verify which Django version the project is intended to use and keep `settings.py` and `requirements.txt` consistent.

Do not silently change either value without confirming the intended project version.

---

## Database Configuration

The provided `settings.py` currently uses:

```text
PostgreSQL
```

not SQLite.

Although a `db.sqlite3` file may exist in the project directory, the current Django database configuration does not use SQLite.

Therefore, for the current configuration, PostgreSQL is the database that Django will connect to.

---

# Security Notes

Never commit sensitive information to GitHub.

Do not commit:

```text
.env
```

or files containing:

```text
API keys
Passwords
Database credentials
Django secret keys
Personal information
```

Use placeholder values such as:

```text
xyz
```

when documenting configuration examples.

---

# Requirements Reference

The project currently lists the following dependencies:

```text
Django>=4.2,<6.0
python-dotenv>=1.0.0
django-cors-headers>=4.3.0
psycopg2-binary>=2.9.9
ollama
pymupdf>=1.23.0
Pillow>=10.0.0
requests>=2.31.0
easyocr>=1.7.0
opencv-python-headless>=4.9.0.80
torch>=2.0.0
torchvision>=0.15.0
gunicorn>=21.2.0
```

---

# Quick Start

For an experienced user, the basic startup process is:

```bash
# Create environment
python -m venv venv

# Activate environment - Windows
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create/update database tables
python manage.py makemigrations
python manage.py migrate

# Make sure Ollama has the required model
ollama pull qwen3:8b

# Start Django
python manage.py runserver 127.0.0.1:8000
```

Then open:

```text
http://127.0.0.1:8000/complaint/
```

---

# Application Summary

The Quality Complaint Management System combines:

```text
Django
   +
PostgreSQL
   +
EasyOCR
   +
PyMuPDF
   +
Ollama / Qwen3 8B
   +
HTML / CSS / JavaScript
```

to provide an AI-assisted workflow for pharmaceutical/API quality complaints.

The main idea is:

```text
Complaint Information
        ↓
 Text / Image / PDF
        ↓
Extraction
        ↓
AI Structured JSON
        ↓
Automatic Form Filling
        ↓
User Review
        ↓
Save Complaint
        ↓
PostgreSQL
```

The system is designed to reduce manual data entry while allowing the user to review the extracted information before saving the complaint record.
