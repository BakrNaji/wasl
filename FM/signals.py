from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PromoRequest, InvestmentRequest, FinancialReport, FinancialMovement
from Chat.models import FeasibilityStudyRequest
from django.utils import timezone

@receiver(post_save, sender=PromoRequest)
def check_promo_request_expiration(sender, instance, **kwargs):
    instance.check_expiration()

@receiver(post_save, sender=InvestmentRequest)
def update_investment_report(sender, instance, **kwargs):
    today = timezone.now().date()
    report, created = FinancialReport.objects.get_or_create(date=today)
    report.generate_report()

@receiver(post_save, sender=PromoRequest)
def update_promo_report(sender, instance, **kwargs):
    today = timezone.now().date()
    report, created = FinancialReport.objects.get_or_create(date=today)
    report.generate_report()

@receiver(post_save, sender=FeasibilityStudyRequest)
def create_financial_movement_for_feasibility_study(sender, instance, **kwargs):
    if instance.is_allowed:
        statement = f"Payment for feasibility study: {instance.project_name}"
        FinancialMovement.objects.create(
            feasibility_study_request=instance,
            statement=statement,
            income=100,  
            outcome=0,
            pay_method='Online'
        )

@receiver(post_save, sender=FeasibilityStudyRequest)
def update_feasibility_study_report(sender, instance, **kwargs):
    today = timezone.now().date()
    report, created = FinancialReport.objects.get_or_create(date=today)
    report.generate_report()
