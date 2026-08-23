
# Create your models here.
from django.db import models
from django.utils import timezone


class Complaint(models.Model):
    # Identification
    complaint_id = models.CharField(
        max_length=100, 
        unique=True, 
        null=False, 
        blank=False,
        default="complaint_id", 
        help_text="Unique Complaint Reference ID"
    )
    complaint_date = models.DateField(default=timezone.now, null=True, blank=True)
    source = models.CharField(max_length=150, null=True, blank=True)
    customer = models.CharField(max_length=255, null=True, blank=True)

    # Product / API Details
    api_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="API Name")
    api_code = models.CharField(max_length=100, null=True, blank=True, verbose_name="API Code")
    batch_lot_no = models.CharField(max_length=100, null=True, blank=True, verbose_name="Batch/Lot No")
    manufacturing_date = models.DateField(null=True, blank=True)
    retest_date = models.DateField(null=True, blank=True)

    # Quantities
    quantity_supplied = models.DecimalField(
        max_digits=12, 
        decimal_places=3, 
        null=True, 
        blank=True
    )
    quantity_affected = models.DecimalField(
        max_digits=12, 
        decimal_places=3, 
        null=True, 
        blank=True
    )

    # Complaint & Quality Analysis
    complaint_category = models.CharField(max_length=150, null=True, blank=True)
    complaint_description = models.TextField(null=True, blank=True)
    specification = models.TextField(null=True, blank=True)
    customer_result = models.TextField(null=True, blank=True)
    coa_no = models.CharField(max_length=100, null=True, blank=True, verbose_name="CoA No")
    sample_available = models.BooleanField(null=True, blank=True, default=False)

    # Investigation & CAPA
    investigation_root_cause = models.TextField(null=True, blank=True)
    impacted_batches = models.JSONField(
        default=list, 
        blank=True, 
        help_text="List of impacted batch numbers"
    )
    capa_required = models.BooleanField(null=True, blank=True, default=False, verbose_name="CAPA Required")
    capa_id = models.CharField(max_length=100, null=True, blank=True, verbose_name="CAPA ID")

    # Conclusion & Closure
    final_conclusion_disposition = models.TextField(null=True, blank=True)
    qa_approval_closure = models.BooleanField(
        null=True, 
        blank=True, 
        default=False, 
        verbose_name="QA Approval Closure"
    )

    # Audit Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "complaints"
        ordering = ["-complaint_date", "-created_at"]
        verbose_name = "Complaint"
        verbose_name_plural = "Complaints"

    def __str__(self):
        return f"{self.complaint_id or 'No ID'} - {self.customer or 'Unknown Customer'}"