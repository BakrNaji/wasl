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
