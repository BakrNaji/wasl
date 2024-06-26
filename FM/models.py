from django.db import models
from datetime import datetime
from django.conf import settings
from The_Owner.models import *
from The_Investor.models import *



################################promotype######################
from datetime import datetime, timedelta
from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from The_Owner.models import Project, Owner
from datetime import datetime, timedelta
from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from The_Owner.models import Project, Owner
from django.utils import timezone
from datetime import timedelta

from django.utils import timezone
from datetime import timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta
from django.db import models
from django.db import models
from django.utils import timezone
from The_Owner.models import Project, Owner
from django.db import models
from datetime import datetime
from django.utils import timezone
from The_Owner.models import Project, Owner
from The_Investor.models import InvestmentRequest
from django.db import models
from django.utils import timezone
from The_Owner.models import Project
from The_Investor.models import InvestmentRequest
from django.db import models
from django.utils import timezone
from The_Owner.models import Project, Owner
from The_Investor.models import InvestmentRequest, Investor
from django.db import models
from django.utils import timezone
from The_Owner.models import Project, Owner
from The_Investor.models import InvestmentRequest
from The_Investor.models import  Investor


from django.db import models
from datetime import datetime
from django.conf import settings
from The_Owner.models import Project, Owner
from The_Investor.models import InvestmentRequest, Investor
from django.db import models
from datetime import datetime
from django.conf import settings
from The_Owner.models import Owner
from The_Investor.models import Investor
from Chat.models import FeasibilityStudyRequest  # استيراد FeasibilityStudyRequest

class Promotype(models.Model):
    promo_name = models.CharField(max_length=25)
    promo_cost = models.DecimalField(max_digits=5, decimal_places=2)
    time_quantity = models.IntegerField(default=30)
    time_unit = models.CharField(max_length=10, choices=[('days', 'أيام'), ('hours', 'ساعات'), ('minutes', 'دقائق')])

    def save(self, *args, **kwargs):
        if self.time_unit == 'days':
            self.time_quantity *= 86400
        elif self.time_unit == 'hours':
            self.time_quantity *= 3600
        elif self.time_unit == 'minutes':
            self.time_quantity *= 60

        self.time_unit = 'seconds'
        super(Promotype, self).save(*args, **kwargs)

    def __str__(self):
        return self.promo_name

class PromoRequest(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, null=True, blank=True)
    promo_type = models.ForeignKey(Promotype, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)
    pay_name = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='pay_images/%Y/%m/%d/', null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.active and not self.end_date:
            self.start_date = timezone.now()
            self.end_date = self.start_date + timedelta(seconds=self.promo_type.time_quantity)
        
        super(PromoRequest, self).save(*args, **kwargs)

    def __str__(self):
        return f'request of {self.pay_name}'

    def check_expiration(self):
        if self.active and self.end_date and timezone.now() > self.end_date:
            self.active = False
            self.save()

class FinancialMovement(models.Model):
    investment_request = models.ForeignKey(InvestmentRequest, on_delete=models.CASCADE, null=True, blank=True)
    promo_request = models.ForeignKey(PromoRequest, on_delete=models.CASCADE, null=True, blank=True)
    feasibility_study_request = models.ForeignKey(FeasibilityStudyRequest, on_delete=models.CASCADE, null=True, blank=True) 
    statement = models.CharField(max_length=50)
    income = models.DecimalField(max_digits=10, decimal_places=2)
    outcome = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=datetime.now)
    pay_method = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f"{self.statement} - {self.date}"
class FinancialReport(models.Model):
    date = models.DateField(auto_now_add=True)
    total_income = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_outcome = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_income = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    promo_requests = models.ManyToManyField(PromoRequest, related_name='financial_reports')
    promo_projects = models.TextField(null=True, blank=True)
    promo_owners = models.TextField(null=True, blank=True)
    promo_total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    invested_projects = models.TextField(null=True, blank=True)
    investors = models.TextField(null=True, blank=True)
    investment_total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    feasibility_study_requests = models.ManyToManyField(FeasibilityStudyRequest, related_name='financial_reports', blank=True)
    feasibility_study_total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_platform_income = models.DecimalField(max_digits=10, decimal_places=2, default=0)  

    def generate_report(self):
        self.total_income = FinancialMovement.objects.aggregate(total_income=models.Sum('income'))['total_income'] or 0
        self.total_outcome = FinancialMovement.objects.aggregate(total_outcome=models.Sum('outcome'))['total_outcome'] or 0
        self.net_income = self.total_income - self.total_outcome

        promo_requests = PromoRequest.objects.filter(active=True)
        self.promo_projects = ", ".join([request.project.title for request in promo_requests])
        self.promo_owners = ", ".join([request.owner.user.username for request in promo_requests])
        self.promo_total_amount = sum([request.promo_type.promo_cost for request in promo_requests])

        investment_requests = InvestmentRequest.objects.filter(is_allowed=True)
        self.invested_projects = ", ".join([request.project.title for request in investment_requests])
        self.investors = ", ".join([request.investor.user.username for request in investment_requests])
        self.investment_total_amount = 10 * investment_requests.count()

        feasibility_study_requests = FeasibilityStudyRequest.objects.filter(is_allowed=True)
        self.save()  
        self.feasibility_study_requests.set(feasibility_study_requests)
        self.feasibility_study_total_amount = feasibility_study_requests.count() * 100  

        
        self.total_platform_income = self.promo_total_amount + self.investment_total_amount + self.feasibility_study_total_amount

        self.save()

    def __str__(self):
        return f"Financial Report for {self.date}"
