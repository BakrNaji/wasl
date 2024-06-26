from django.db import models
from datetime import datetime
from django.conf import settings
from The_Owner.models import Owner
from The_Investor.models import Investor
# from FM.models import FinancialMovement  # استيراد FinancialMovement

# كلاس دراسة الجدوى
class FeasibilityStudy(models.Model):
    project_name = models.CharField(max_length=255)
    description = models.TextField()
    market_analysis = models.TextField()
    financial_analysis = models.TextField()
    risk_assessment = models.TextField()
    recommendations = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(Owner, on_delete=models.PROTECT, null=True, blank=True)
    investor = models.ForeignKey(Investor, on_delete=models.PROTECT, null=True, blank=True)
    is_allowed = models.BooleanField(default=False)
    feasibility_study_request = models.ForeignKey('FeasibilityStudyRequest', on_delete=models.CASCADE, related_name='feasibility_studies', null=True, blank=True)

    def __str__(self):
        return self.project_name

# كلاس الدردشة
class Chat(models.Model):
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name='admin_chats')
    owner = models.ForeignKey(Owner, on_delete=models.PROTECT, null=True, blank=True)
    investor = models.ForeignKey(Investor, on_delete=models.PROTECT, null=True, blank=True)
    text = models.TextField(max_length=200, null=True, blank=True)
    admin_reply = models.TextField(max_length=200, null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    feasibility_study = models.ForeignKey(FeasibilityStudy, on_delete=models.CASCADE, related_name='chats')

    def save(self, *args, **kwargs):
        if not self.pk:  # If the chat instance is being created
            if self.owner:
                self.investor = None  # Ensure only owner or investor is set
            elif self.investor:
                self.owner = None  # Ensure only owner or investor is set
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Chat on {self.date} by {self.admin or self.owner or self.investor}"

# كلاس طلب دراسة الجدوى
class FeasibilityStudyRequest(models.Model):
    STUDY_TYPE_CHOICES = [
        ('all', 'الكل'),
        ('market_analysis', 'تحليل السوق'),
        ('financial_analysis', 'التحليل المالي'),
        ('risk_assessment', 'تقييم المخاطر')
    ]

    project_name = models.CharField(max_length=255)
    description = models.TextField()
    goals = models.TextField()
    target_audience = models.TextField()
    competitors = models.TextField()
    resources = models.TextField()
    additional_info = models.TextField(null=True, blank=True)
    study_type = models.CharField(max_length=50, choices=STUDY_TYPE_CHOICES, default='all')
    supporting_documents = models.FileField(upload_to='supporting_documents/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pay_name = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='pay_images/%Y/%m/%d/', null=True, blank=True)
    is_allowed = models.BooleanField(default=False)
    admin_response = models.TextField(null=True, blank=True)
    feasibility_study = models.ForeignKey(FeasibilityStudy, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.project_name
