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
    branch = models.ForeignKey('Branch', on_delete=models.SET_NULL, null=True, blank=True, related_name='investors')
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True, related_name='investors')
    job_title = models.CharField(max_length=100, blank=True)
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


class Evaluation(models.Model):
    """Owner evaluates an Investor (employee) on multiple professional criteria.

    - `evaluator`: Owner who made the evaluation.
    - `investor`: Investor being evaluated.
    - `department` and `branch`: textual identifiers.
    - Several integer criteria (1-5). `overall_score` is computed as weighted average.
    """
    evaluator = models.ForeignKey(Owner, on_delete=models.SET_NULL, null=True, blank=True, related_name='evaluations_given')
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE, related_name='evaluations_received')
    department = models.CharField(max_length=100, blank=True)
    branch = models.CharField(max_length=100, blank=True)

    professionalism = models.IntegerField(default=5)
    communication = models.IntegerField(default=5)
    quality_of_work = models.IntegerField(default=5)
    punctuality = models.IntegerField(default=5)
    teamwork = models.IntegerField(default=5)

    overall_score = models.DecimalField(max_digits=3, decimal_places=2, editable=False, default=0)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_evaluations')
    approved_at = models.DateTimeField(null=True, blank=True)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def compute_overall(self):
        # simple average across criteria (weights can be adjusted)
        vals = [self.professionalism, self.communication, self.quality_of_work, self.punctuality, self.teamwork]
        return sum(vals) / len(vals)

    def save(self, *args, **kwargs):
        try:
            self.overall_score = round(self.compute_overall(), 2)
        except Exception:
            self.overall_score = 0
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Eval {self.investor.user.username} by {self.evaluator.user.username if self.evaluator else "N/A"} - {self.overall_score}'


class EvaluationCriterion(models.Model):
    """A criterion that admins can manage and weight for evaluations."""
    name = models.CharField(max_length=150)
    weight = models.FloatField(default=1.0)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} (w={self.weight})"


class EvaluationScore(models.Model):
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, related_name='scores')
    criterion = models.ForeignKey(EvaluationCriterion, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        unique_together = ('evaluation', 'criterion')

    def __str__(self):
        return f"{self.criterion.name}: {self.score}"


class EvaluationImage(models.Model):
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='evaluation_images/%Y/%m/%d/')

    def __str__(self):
        return f"Image for {self.evaluation.id}"


class Branch(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=150, unique=True)
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE, null=True, blank=True, related_name='departments')

    def __str__(self):
        if self.branch:
            return f"{self.name} — {self.branch.name}"
        return self.name