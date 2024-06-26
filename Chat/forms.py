from django import forms
from .models import FeasibilityStudyRequest

class FeasibilityStudyRequestForm(forms.ModelForm):
    class Meta:
        model = FeasibilityStudyRequest
        fields = [
            'project_name', 'description', 'goals', 'target_audience', 
            'competitors', 'resources', 'additional_info', 
            'study_type', 'supporting_documents',
            'pay_name', 'image'
        ]
        
        widgets = {
            'project_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'goals': forms.Textarea(attrs={'class': 'form-control'}),
            'target_audience': forms.Textarea(attrs={'class': 'form-control'}),
            'competitors': forms.Textarea(attrs={'class': 'form-control'}),
            'resources': forms.Textarea(attrs={'class': 'form-control'}),
            'additional_info': forms.Textarea(attrs={'class': 'form-control'}),
            'study_type': forms.Select(attrs={'class': 'form-control'}),
            'supporting_documents': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'pay_name': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'project_name': 'اسم المشروع',
            'description': 'وصف المشروع',
            'goals': 'أهداف المشروع',
            'target_audience': 'الجمهور المستهدف',
            'competitors': 'المنافسين الرئيسيين',
            'resources': 'الموارد المتاحة',
            'additional_info': 'معلومات إضافية',
            'study_type': 'اختر أنواع الدراسات المطلوبة',
            'supporting_documents': 'المستندات الداعمة',
            'pay_name': 'اسم الدفع',
            'image': 'صورة الدفع'
        }


from django import forms
from .models import Chat

class ChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ['text', ]
