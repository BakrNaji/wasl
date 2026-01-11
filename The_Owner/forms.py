from django import forms
from .models import *



class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project 
        fields = ['category', 'status' , 'title', 'discripe', 'cost', 'details', 'address', 'image']
        labels = {
            'category': 'تصنيف المشروع',
            'status': 'حالة المشروع',
            'title': 'اسم المشروع',
            'discripe': 'وصف المشروع',
            'cost': 'تكلفة المشروع',
            'details': 'تفاصيل المشروع',
            'address': 'موقع المشروع',
            'image': 'صورة المشروع',


        }
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # استخراج المستخدم من الوسائط إذا تم تمريره
        super(ProjectForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['owner'].initial = user.owner.id  # تحديد قيمة حقل المالك بمعرف المالك للمستخدم الحالي
            self.fields['owner'].widget.attrs['readonly'] = True  # جعل حقل المالك لا يقبل التعديل


            self.fields['category'].required = True
            self.fields['status'].required = True
            self.fields['title'].required = True
            self.fields['discripe'].required = True
            self.fields['cost'].required = True
            self.fields['details'].required = True
            self.fields['address'].required = True
            self.fields['image'].required = True

            self.fields['category'].empty_label = 'يجب إختيار تصنيف مشروعك'
            self.fields['category'].widget.attrs['class'] = 'custom-empty'  # تحديد الكلاس الخاص بـ empty_label
            self.fields['category'].widget.attrs['style'] = 'color: black;'  # لون الخيارات العادية

            self.fields['status'].empty_label = 'يجب تحديد حالة مشروعك'
            self.fields['status'].widget.attrs['class'] = 'custom-empty'  # تحديد الكلاس الخاص بـ empty_label
            self.fields['status'].widget.attrs['style'] = 'color: black;'  # لون الخيارات العادية


########################

# from django import forms
# from .models import Project

# class ProjectForm(forms.ModelForm):
#     class Meta:
#         model = Project 
#         fields = ['category', 'title', 'discripe', 'cost', 'details', 'address', 'image', 'active', 'created']
#         labels = {
#             'discripe': 'الوصف المشروع',
#         }


from django import forms
from .models import Message

# class MessageForm(forms.ModelForm):
#     class Meta:
#         model = Message
#         exclude = ['admin_response']  # استثناء admin_response
      # استثناء admin_response
from django import forms
from .models import Message 

class MessageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and user.is_authenticated:
            self.fields['name'].widget = forms.HiddenInput()
            self.fields['name'].required = False

    class Meta:
        model = Message
        exclude = ['admin_response']

    def clean(self):
        cleaned_data = super().clean()
        user = self.initial.get('user')
        if user and user.is_authenticated:
            cleaned_data['name'] = user.username
        return cleaned_data

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:  # إذا كانت القيمة فارغة
            raise forms.ValidationError("يجب تعبئة هذا الحقل")  # رسالة الخطأ
        return name


from django import forms
from The_Investor.models import Evaluation, EvaluationCriterion, Branch, Department
from django.conf import settings


class EvaluationForm(forms.ModelForm):
    images = forms.FileField(required=False)

    class Meta:
        model = Evaluation
        fields = ['department', 'branch', 'comment']
        labels = {
            'department': 'القسم',
            'branch': 'الفرع',
            'comment': 'ملاحظات',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # branch/department as admin-managed selects
        self.fields['branch'] = forms.ModelChoiceField(queryset=Branch.objects.all(), required=False, empty_label='-- اختر فرع --')
        # set department queryset filtered by selected branch when possible
        dept_qs = Department.objects.all()
        # check bound data first
        selected_branch_id = None
        try:
            if self.data and self.data.get('branch'):
                selected_branch_id = int(self.data.get('branch'))
        except Exception:
            selected_branch_id = None
        # if initial passed or instance has branch, try to use it
        if not selected_branch_id:
            init_branch = self.initial.get('branch') if hasattr(self, 'initial') else None
            if isinstance(init_branch, Branch):
                selected_branch_id = init_branch.id
            elif isinstance(init_branch, int):
                selected_branch_id = init_branch
        if selected_branch_id:
            dept_qs = Department.objects.filter(branch_id=selected_branch_id)
        self.fields['department'] = forms.ModelChoiceField(queryset=dept_qs, required=False, empty_label='-- اختر قسم --')

        # dynamically add fields for active criteria
        criteria = EvaluationCriterion.objects.filter(active=True)
        scale = getattr(settings, 'EVAL_SCALE', 5)
        for c in criteria:
            field_name = f'criterion_{c.id}'
            # use integer inputs between 1 and scale
            self.fields[field_name] = forms.IntegerField(label=c.name, min_value=1, max_value=scale, initial=max(1, scale // 2), required=False)
            # attach criterion id for later processing
            self.fields[field_name].criterion = c

    def save(self, commit=True):
        # override to convert selected Branch/Department to their names (Evaluation model stores strings)
        ev = super().save(commit=False)
        branch_obj = self.cleaned_data.get('branch')
        dept_obj = self.cleaned_data.get('department')
        if branch_obj:
            ev.branch = branch_obj.name
        if dept_obj:
            ev.department = dept_obj.name
        if commit:
            ev.save()
        return ev


# from django import forms
# from .models import ProjectRating

# class ProjectRatingForm(forms.ModelForm):
#     class Meta:
#         model = ProjectRating
#         fields = ['rating', 'comment']  # قم بتضمين حقول التقييم والتعليق من نموذج ProjectRating
#         labels = {
#             'rating': 'التقييم',
#             'comment': 'التعليق',
#         }

# class MessageForm(forms.ModelForm):
#     class Meta:
#         model = Message
#         exclude = ['admin_response']  # استثناء admin_response
        
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         if self.instance and self.instance.name:
#             self.fields['name'].widget = forms.HiddenInput()  # إخفاء حقل الاسم إذا كان المستخدم مسجل دخول

# from django import forms
# from .models import Message

# class MessageForm(forms.ModelForm):
#     class Meta:
#         model = Message
#         exclude = ['admin_response']  # استثناء admin_response
        
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         if self.instance and self.instance.name:
#             self.fields['name'].widget = forms.HiddenInput()  # إخفاء حقل الاسم إذا كان المستخدم مسجل دخول

