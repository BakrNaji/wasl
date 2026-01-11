from django.db import models
from datetime import datetime
from django.conf import settings
# from multiupload.fields import MultiFileField


from django.db import models
from django.contrib.auth.models import User


##############################OWner##################################################
class Owner(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='owners/%Y/%m/%d/', blank=True)
    address = models.CharField(max_length=25)  # إضافة حقل العنوان
    phone = models.CharField(max_length=9)
    total_owners = models.IntegerField(default=0)

    def __str__(self):
        return f"Total Owners: {self.total_owners}"

    def __str__(self):
        return f'Profile of {self.user.username}'

##############################Category##################################################

class ProjectCategory(models.Model):
    category = models.TextField(max_length=50)
    def __str__(self):
        return self.category

##############################projectstatus##################################################


class ProjectStatus(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

##############################Project##################################################



class Project(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(ProjectCategory, on_delete=models.CASCADE, null=True, blank=True)
    status = models.ForeignKey(ProjectStatus, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100)
    discripe = models.TextField(max_length=180)
    cost = models.DecimalField(max_digits=5, decimal_places=2)
    details = models.TextField(max_length=1000)
    address = models.CharField(max_length=30)
    image = models.ImageField(upload_to='project_images/', null=True, blank=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(default=datetime.now)
    total_projects = models.IntegerField(default=0)


    def average_rating(self):
        ratings = self.ratings.all()
        if ratings:
            total = sum(rating.rating for rating in ratings)
            return total / len(ratings)
        return 0

   
    def __str__(self):
        return f"Total Projects: {self.total_projects}"
    
    def __str__(self):
        return f"Total Projects: {self.total_projects}"
    


    
    def __str__(self):
        return self.title
      
##############################Photo##################################################

# class ProjectImages(models.Model):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE , related_name='images')
#     image = models.ImageField(upload_to='project_images/' , null=True, blank=True)
#     upload_folder = models.CharField(max_length=255)  # استخدم لتحديد المجلد

#     def save(self, *args, **kwargs):
#         # قم بتحديد المجلد المستهدف لرفع الصور إليه
#         upload_folder = self.upload_folder

#         # حفظ الصور في المجلد المستهدف
#         super().save(*args, **kwargs)


class Photo(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True , blank=True )
    photo_path = models.TextField(max_length=200)

########################
#sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
#receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
from django.db import models
from django.db import models

class Message(models.Model):
    name = models.CharField(max_length=255)
    body = models.TextField()

    # تحديد الحقول كإلزامية
    email = models.EmailField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    admin_response = models.TextField(blank=True, null=True)
    is_read = models.BooleanField(default=False)  # الحقل الجديد


    def __str__(self):
        return self.name




# from django.db import models
# from django.conf import settings
# from django.core.validators import MinValueValidator, MaxValueValidator
# from django.db.models.constraints import UniqueConstraint
# from .models import Project

# class ProjectRating(models.Model):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='ratings')
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     rating = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(5)])
#     comment = models.TextField(blank=True, null=True)

#     class Meta:
#         constraints = [
#             UniqueConstraint(fields=['project', 'user'], name='unique_project_rating')
#         ]

#     def __str__(self):
#         return f"Rating for {self.project.title} by {self.user.username}"

# ==================== نظام التقييم للأقسام والموظفين ====================

class EvaluationCriterion(models.Model):
    """معيار التقييم - مثل النظافة، الترتيب، إلخ"""
    name = models.CharField(max_length=200, verbose_name='اسم المعيار')
    max_observations = models.IntegerField(default=10, verbose_name='الحد الأقصى للملاحظات')
    is_active = models.BooleanField(default=True, verbose_name='نشط')
    order = models.IntegerField(default=0, verbose_name='الترتيب')
    criterion_type = models.CharField(max_length=20, default='department', choices=[('department', 'قسم'), ('employee', 'موظف')], verbose_name='نوع المعيار')
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'معيار التقييم'
        verbose_name_plural = 'معايير التقييم'
    
    def __str__(self):
        return f"{self.name} ({self.get_criterion_type_display()})"


class DepartmentEvaluation(models.Model):
    """تقييم شهري لقسم"""
    from The_Investor.models import Department, Branch
    
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='القسم')
    month = models.DateField(verbose_name='الشهر')
    evaluator = models.ForeignKey(Owner, on_delete=models.SET_NULL, null=True, verbose_name='المقيّم')
    
    # النتائج المحسوبة
    total_observations = models.IntegerField(default=0, editable=False, verbose_name='إجمالي الملاحظات')
    total_score = models.IntegerField(default=0, editable=False, verbose_name='إجمالي النقاط')
    max_possible_score = models.IntegerField(default=0, editable=False, verbose_name='أقصى نقاط ممكنة')
    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0, editable=False, verbose_name='النسبة المئوية')
    
    notes = models.TextField(blank=True, verbose_name='ملاحظات عامة')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-month', 'department']
        unique_together = ['department', 'month']
        verbose_name = 'تقييم القسم'
        verbose_name_plural = 'تقييمات الأقسام'
    
    def __str__(self):
        return f"تقييم {self.department.name} - {self.month.strftime('%Y-%m')}"
    
    def calculate_totals(self):
        """حساب الإجماليات"""
        details = self.details.all()
        
        self.total_observations = sum(d.observations_count for d in details)
        self.max_possible_score = sum(d.criterion.max_observations for d in details)
        
        # النقاط = الحد الأقصى - الملاحظات (كلما قلت الملاحظات كان أفضل)
        self.total_score = self.max_possible_score - self.total_observations
        
        # النسبة المئوية
        if self.max_possible_score > 0:
            self.percentage = (self.total_score / self.max_possible_score) * 100
        else:
            self.percentage = 0
    
    def save(self, *args, **kwargs):
        # حفظ أولاً للحصول على primary key
        is_new = self.pk is None
        super().save(*args, **kwargs)
        # حساب الإجماليات بعد الحفظ فقط
        if not is_new or self.pk:
            self.calculate_totals()
            if self.total_observations != 0 or self.total_score != 0:
                # حفظ مرة أخرى لتحديث الإجماليات
                super().save(update_fields=['total_observations', 'total_score', 'percentage'])


class EvaluationObservation(models.Model):
    """ملاحظة واحدة لمعيار معين"""
    evaluation = models.ForeignKey(DepartmentEvaluation, on_delete=models.CASCADE, related_name='details', verbose_name='التقييم')
    criterion = models.ForeignKey(EvaluationCriterion, on_delete=models.CASCADE, verbose_name='المعيار')
    observations_count = models.IntegerField(default=0, verbose_name='عدد الملاحظات')
    description = models.TextField(blank=True, verbose_name='وصف الملاحظات')
    
    class Meta:
        ordering = ['criterion__order']
        unique_together = ['evaluation', 'criterion']
        verbose_name = 'ملاحظة التقييم'
        verbose_name_plural = 'ملاحظات التقييم'
    
    def __str__(self):
        return f"{self.criterion.name}: {self.observations_count} ملاحظة"
    
    def get_score(self):
        """حساب النقاط لهذا المعيار"""
        max_score = self.criterion.max_observations
        return max(0, max_score - self.observations_count)
    
    def get_percentage(self):
        """حساب النسبة لهذا المعيار"""
        max_score = self.criterion.max_observations
        if max_score > 0:
            return (self.get_score() / max_score) * 100
        return 0


class ObservationImage(models.Model):
    """صورة مرفقة مع ملاحظة"""
    observation = models.ForeignKey(EvaluationObservation, on_delete=models.CASCADE, related_name='images', verbose_name='الملاحظة')
    image = models.ImageField(upload_to='evaluation_observations/%Y/%m/%d/', verbose_name='الصورة')
    caption = models.CharField(max_length=200, blank=True, verbose_name='وصف الصورة')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'صورة الملاحظة'
        verbose_name_plural = 'صور الملاحظات'
    
    def __str__(self):
        return f"صورة لـ {self.observation}"


class EmployeeEvaluation(models.Model):
    """تقييم شهري لموظف"""
    from The_Investor.models import Investor
    
    employee = models.ForeignKey(Investor, on_delete=models.CASCADE, verbose_name='الموظف')
    month = models.DateField(verbose_name='الشهر')
    evaluator = models.ForeignKey(Owner, on_delete=models.SET_NULL, null=True, verbose_name='المقيّم')
    
    # النتائج المحسوبة
    total_observations = models.IntegerField(default=0, editable=False, verbose_name='إجمالي الملاحظات')
    total_score = models.IntegerField(default=0, editable=False, verbose_name='إجمالي النقاط')
    max_possible_score = models.IntegerField(default=0, editable=False, verbose_name='أقصى نقاط ممكنة')
    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0, editable=False, verbose_name='النسبة المئوية')
    
    notes = models.TextField(blank=True, verbose_name='ملاحظات عامة')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-month', 'employee']
        unique_together = ['employee', 'month']
        verbose_name = 'تقييم الموظف'
        verbose_name_plural = 'تقييمات الموظفين'
    
    def __str__(self):
        return f"تقييم {self.employee.user.username} - {self.month.strftime('%Y-%m')}"
    
    def calculate_totals(self):
        """حساب الإجماليات"""
        details = self.details.all()
        
        self.total_observations = sum(d.observations_count for d in details)
        self.max_possible_score = sum(d.criterion.max_observations for d in details)
        self.total_score = self.max_possible_score - self.total_observations
        
        if self.max_possible_score > 0:
            self.percentage = (self.total_score / self.max_possible_score) * 100
        else:
            self.percentage = 0
    
    def save(self, *args, **kwargs):
        # حفظ أولاً للحصول على primary key
        is_new = self.pk is None
        super().save(*args, **kwargs)
        # حساب الإجماليات بعد الحفظ فقط
        if not is_new or self.pk:
            self.calculate_totals()
            if self.total_observations != 0 or self.total_score != 0:
                # حفظ مرة أخرى لتحديث الإجماليات
                super().save(update_fields=['total_observations', 'total_score', 'percentage'])


class EmployeeObservation(models.Model):
    """ملاحظة لتقييم موظف"""
    evaluation = models.ForeignKey(EmployeeEvaluation, on_delete=models.CASCADE, related_name='details', verbose_name='التقييم')
    criterion = models.ForeignKey(EvaluationCriterion, on_delete=models.CASCADE, verbose_name='المعيار')
    observations_count = models.IntegerField(default=0, verbose_name='عدد الملاحظات')
    description = models.TextField(blank=True, verbose_name='وصف الملاحظات')
    
    class Meta:
        ordering = ['criterion__order']
        unique_together = ['evaluation', 'criterion']
        verbose_name = 'ملاحظة تقييم الموظف'
        verbose_name_plural = 'ملاحظات تقييم الموظف'
    
    def __str__(self):
        return f"{self.criterion.name}: {self.observations_count} ملاحظة"
    
    def get_score(self):
        max_score = self.criterion.max_observations
        return max(0, max_score - self.observations_count)
    
    def get_percentage(self):
        max_score = self.criterion.max_observations
        if max_score > 0:
            return (self.get_score() / max_score) * 100
        return 0


class EmployeeObservationImage(models.Model):
    """صورة مرفقة مع ملاحظة موظف"""
    observation = models.ForeignKey(EmployeeObservation, on_delete=models.CASCADE, related_name='images', verbose_name='الملاحظة')
    image = models.ImageField(upload_to='employee_observations/%Y/%m/%d/', verbose_name='الصورة')
    caption = models.CharField(max_length=200, blank=True, verbose_name='وصف الصورة')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'صورة ملاحظة الموظف'
        verbose_name_plural = 'صور ملاحظات الموظف'
    
    def __str__(self):
        return f"صورة لـ {self.observation}"