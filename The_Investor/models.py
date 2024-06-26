from django.db import models
from datetime import datetime
from django.conf import settings
from The_Owner.models import *
from The_Owner.models import Project
from django.contrib.auth.models import User 
from The_Owner.models import Owner

class Investor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='usersphoto/%Y/%m/%d/', blank=True)
    phone = models.CharField(max_length=9)
    total_investor = models.IntegerField(default=0)
    address = models.CharField(max_length=25)
    owner = models.OneToOneField(Owner, on_delete=models.CASCADE, null=True, blank=True)  
    
    def __str__(self):
        return f"Total investor: {self.total_investor}"
   
    def __str__(self):
        return f'Profile of {self.user.username}'
    
    def invested_projects(self):
        return [investment.project for investment in self.investmentrequest_set.all()]
    
    def total_investmentrequest(self):
        return InvestmentRequest.objects.filter(investor=self, is_allowed=True).count()

    
    
###################################investor#######################
class Favorite(models.Model):
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f"investor: {self.investor}"
class InvestmentRequest(models.Model):
    date = models.DateTimeField(default=datetime.now)
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    payer_name = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='pay_images/%Y/%m/%d/', null=True, blank=True)
    is_allowed = models.BooleanField(default=False)
    is_project_rated = models.BooleanField(default=False)  # تعديل هنا


    def __str__(self):
        return f'request of {self.payer_name}'



from django.core.validators import MinValueValidator, MaxValueValidator

class InvestorRatingComment(models.Model):
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)]) # نطاق من 1 إلى 10
    comment = models.TextField()
    comment = models.TextField()


    class Meta:
        unique_together = ('investor', 'project')  # للسماح بتقييم المشروع مرة واحدة فقط

    def __str__(self):
        return f'تقييم المستثمر: {self.investor}, المشروع: {self.project}'

    # def __str__(self):
    #     return f'Profile of {self.user.username}'

class Report(models.Model):
    comment = models.ForeignKey(InvestorRatingComment, on_delete=models.CASCADE)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField(blank=True, null=True)
    date_reported = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Report by {self.reporter.username} on {self.comment.id}'