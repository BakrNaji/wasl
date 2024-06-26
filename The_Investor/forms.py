# from django import forms
# from The_Investor.models import InvestmentRequest

# class RatingCommentForm(forms.ModelForm):
#     investor_identifier = forms.IntegerField(widget=forms.HiddenInput())  # إضافة حقل غير مرئي لمعرف المستثمر

#     class Meta:
#         model = InvestmentRequest
#         fields = ['rating', 'comment']  # استخدام حقول المشروع المتاحة فقط
#         labels = {
#             'rating': 'التقييم',
#             'comment': 'التعليق',
#         }

#     def clean(self):
#         cleaned_data = super().clean()
#         investor_identifier = cleaned_data.get("investor_identifier")
        
#         # Check if the investor already submitted a rating/comment for this project
#         if InvestmentRequest.objects.filter(investor_identifier=investor_identifier).exists():
#             raise forms.ValidationError("لقد قمت بالفعل بتقديم تقييم أو تعليق.")


from django import forms
from The_Investor.models import Investor, Project

from django.shortcuts import get_object_or_404
from The_Investor.models import InvestorRatingComment


# class RatingCommentForm(forms.ModelForm):
#     class Meta:
#         model = InvestorRatingComment
#         fields = ['rating', 'comment']
#         labels = {
#             'rating': 'التقييم',
#             'comment': 'التعليق',
#         }


from django import forms
from The_Investor.models import InvestorRatingComment

# class RatingCommentForm(forms.ModelForm):
#     class Meta:
#         model = InvestorRatingComment
#         fields = ['rating', 'comment']
#         labels = {
#             'rating': 'التقييم',
#             'comment': 'التعليق',
#         }الاخير

# class RatingCommentForm(forms.ModelForm):
#     class Meta:
#         model = InvestorRatingComment
#         fields = ['rating', 'comment']
#         labels = {
#             'rating': 'التقييم',
#             'comment': 'التعليق',
#         }
#         widgets = {
#             'rating': forms.NumberInput(attrs={'min': '1', 'max': '10'}), # نطاق من 1 إلى 10 في الفورم
#         }

# class RatingCommentForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['rating'].disabled = True  # تعطيل حقل التقييم بشكل افتراضي

#     class Meta:
#         model = InvestorRatingComment
#         fields = ['rating', 'comment']
#         labels = {
#             'rating': 'التقييم',
#             'comment': 'التعليق',
#         }
from django import forms
from .models import InvestorRatingComment

class RatingCommentForm(forms.ModelForm):
    class Meta:
        model = InvestorRatingComment
        fields = ['rating', 'comment']
        labels = {
            'rating': 'التقييم',
            'comment': 'التعليق',
        }

