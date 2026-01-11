from django.contrib import admin
from .models import Owner, ProjectCategory, Project, Photo , ProjectStatus

admin.site.register(Owner)
# Removed per request: ProjectCategory, Photo, ProjectStatus, Project will remain unregistered



# from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.models import AnonymousUser
from .models import Message 
from django.contrib import admin
from .models import Message 
from django.utils.html import format_html

class MessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'display_conversation']  
    list_display_links = ['name']  

    def display_conversation(self, obj):
        # احصل على جميع رسائل المستخدم مرتبة بترتيب الزمن
        user_messages = Message.objects.filter(name=obj.name, admin_response__isnull=False).order_by('timestamp')
        
        conversation_html = "<div>"  # بداية القالب
        previous_user = None  # متغير لتتبع اسم المستخدم السابق
        for message in user_messages:
            # فقط إذا كان اسم المستخدم الحالي يختلف عن السابق نقوم بإضافته إلى القالب
            if message.name != previous_user:
                conversation_html += f"<div><strong>Name:</strong> {message.name}</div>"
                previous_user = message.name  # تحديث اسم المستخدم السابق ليكون الحالي
            # إضافة كل رسالة ورد للقالب
            conversation_html += f"<div><strong>User:</strong> {message.body}</div>"
            conversation_html += f"<div><strong>Admin:</strong> {message.admin_response}</div><hr>"
        conversation_html += "</div>"  # نهاية القالب
        
        return format_html(conversation_html)

    display_conversation.short_description = "Conversation"  # تعيين عنوان القالب في الإدارة

admin.site.register(Message, MessageAdmin)

# ==================== إدارة نظام التقييم ====================

from .models import (EvaluationCriterion, DepartmentEvaluation, EvaluationObservation, 
                     ObservationImage, EmployeeEvaluation, EmployeeObservation, EmployeeObservationImage)

@admin.register(EvaluationCriterion)
class EvaluationCriterionAdmin(admin.ModelAdmin):
    list_display = ('order', 'name', 'max_observations', 'is_active')
    list_display_links = ('name',)
    list_editable = ('max_observations', 'is_active', 'order')
    ordering = ('order',)


class ObservationImageInline(admin.TabularInline):
    model = ObservationImage
    extra = 1
    fields = ('image', 'caption')


class EvaluationObservationInline(admin.TabularInline):
    model = EvaluationObservation
    extra = 1
    fields = ('criterion', 'observations_count', 'description')


@admin.register(DepartmentEvaluation)
class DepartmentEvaluationAdmin(admin.ModelAdmin):
    list_display = ('department', 'month', 'get_branch', 'get_percentage_display', 'total_observations', 'total_score', 'evaluator')
    list_filter = ('month', 'department__branch', 'department')
    search_fields = ('department__name', 'notes')
    readonly_fields = ('total_observations', 'total_score', 'max_possible_score', 'percentage', 'created_at', 'updated_at', 'get_details_table')
    inlines = [EvaluationObservationInline]
    date_hierarchy = 'month'
    fieldsets = (
        ('معلومات أساسية', {
            'fields': ('department', 'month', 'evaluator')
        }),
        ('النتائج', {
            'fields': ('total_observations', 'total_score', 'max_possible_score', 'percentage')
        }),
        ('ملاحظات', {
            'fields': ('notes',)
        }),
        ('تفاصيل', {
            'fields': ('get_details_table',)
        }),
        ('التواريخ', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def get_branch(self, obj):
        return obj.department.branch.name if obj.department.branch else '-'
    get_branch.short_description = 'الفرع'
    
    def get_percentage_display(self, obj):
        try:
            color = 'red' if obj.percentage < 60 else 'orange' if obj.percentage < 80 else 'green'
            return format_html('<span style="color: {}; font-weight: bold;">{:.1f}%</span>', color, obj.percentage)
        except:
            return '-'
    get_percentage_display.short_description = 'النسبة'
    
    def get_details_table(self, obj):
        if not obj.pk:
            return "احفظ التقييم أولاً"
        
        try:
            details = obj.details.all()
            if not details.exists():
                return "لا توجد تفاصيل بعد"
            
            html = '<table style="width:100%; border-collapse: collapse; border: 1px solid #ddd;">'
            html += '<tr style="background: #417690; color: white;"><th style="padding: 8px; border: 1px solid #ddd;">المعيار</th><th style="padding: 8px; border: 1px solid #ddd;">الحد الأقصى</th><th style="padding: 8px; border: 1px solid #ddd;">الملاحظات</th><th style="padding: 8px; border: 1px solid #ddd;">النقاط</th><th style="padding: 8px; border: 1px solid #ddd;">النسبة</th><th style="padding: 8px; border: 1px solid #ddd;">الصور</th></tr>'
            
            for detail in details:
                images_count = detail.images.count()
                score = detail.get_score()
                percentage = detail.get_percentage()
                color = 'red' if percentage < 60 else 'orange' if percentage < 80 else 'green'
                html += f'<tr>'
                html += f'<td style="padding: 8px; border: 1px solid #ddd;">{detail.criterion.name}</td>'
                html += f'<td style="padding: 8px; border: 1px solid #ddd; text-align:center">{detail.criterion.max_observations}</td>'
                html += f'<td style="padding: 8px; border: 1px solid #ddd; text-align:center; background:#fff3cd">{detail.observations_count}</td>'
                html += f'<td style="padding: 8px; border: 1px solid #ddd; text-align:center; font-weight:bold">{score}</td>'
                html += f'<td style="padding: 8px; border: 1px solid #ddd; text-align:center; color:{color}; font-weight:bold">{percentage:.1f}%</td>'
                html += f'<td style="padding: 8px; border: 1px solid #ddd; text-align:center">{images_count} صورة</td>'
                html += f'</tr>'
            
            html += '</table>'
            return format_html(html)
        except Exception as e:
            return f"خطأ في عرض التفاصيل: {str(e)}"
    get_details_table.short_description = 'تفاصيل التقييم'


@admin.register(ObservationImage)
class ObservationImageAdmin(admin.ModelAdmin):
    list_display = ('observation', 'caption', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('caption', 'observation__criterion__name')


class EmployeeObservationImageInline(admin.TabularInline):
    model = EmployeeObservationImage
    extra = 1
    fields = ('image', 'caption')


class EmployeeObservationInline(admin.TabularInline):
    model = EmployeeObservation
    extra = 1
    fields = ('criterion', 'observations_count', 'description')


@admin.register(EmployeeEvaluation)
class EmployeeEvaluationAdmin(admin.ModelAdmin):
    list_display = ('employee', 'get_department', 'month', 'get_percentage_display', 'total_observations', 'total_score', 'evaluator')
    list_filter = ('month', 'employee__department')
    search_fields = ('employee__user__username', 'notes')
    readonly_fields = ('total_observations', 'total_score', 'max_possible_score', 'percentage', 'created_at', 'updated_at', 'get_details_table')
    inlines = [EmployeeObservationInline]
    date_hierarchy = 'month'
    fieldsets = (
        ('معلومات أساسية', {
            'fields': ('employee', 'month', 'evaluator')
        }),
        ('النتائج', {
            'fields': ('total_observations', 'total_score', 'max_possible_score', 'percentage')
        }),
        ('ملاحظات', {
            'fields': ('notes',)
        }),
        ('تفاصيل', {
            'fields': ('get_details_table',)
        }),
        ('التواريخ', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def get_department(self, obj):
        return obj.employee.department.name if obj.employee.department else '-'
    get_department.short_description = 'القسم'
    
    def get_percentage_display(self, obj):
        try:
            color = 'red' if obj.percentage < 60 else 'orange' if obj.percentage < 80 else 'green'
            return format_html('<span style="color: {}; font-weight: bold;">{:.1f}%</span>', color, obj.percentage)
        except:
            return '-'
    get_percentage_display.short_description = 'النسبة'
    
    def get_details_table(self, obj):
        if not obj.pk:
            return "احفظ التقييم أولاً"
        
        try:
            details = obj.details.all()
            if not details.exists():
                return "لا توجد تفاصيل بعد"
            
            html = '<table style="width:100%; border-collapse: collapse; border: 1px solid #ddd;">'
            html += '<tr style="background: #417690; color: white;"><th style="padding: 8px; border: 1px solid #ddd;">المعيار</th><th style="padding: 8px; border: 1px solid #ddd;">الحد الأقصى</th><th style="padding: 8px; border: 1px solid #ddd;">الملاحظات</th><th style="padding: 8px; border: 1px solid #ddd;">النقاط</th><th style="padding: 8px; border: 1px solid #ddd;">النسبة</th><th style="padding: 8px; border: 1px solid #ddd;">الصور</th></tr>'
            
            for detail in details:
                images_count = detail.images.count()
                score = detail.get_score()
                percentage = detail.get_percentage()
                color = 'red' if percentage < 60 else 'orange' if percentage < 80 else 'green'
                html += f'<tr>'
                html += f'<td style="padding: 8px; border: 1px solid #ddd;">{detail.criterion.name}</td>'
                html += f'<td style="padding: 8px; border: 1px solid #ddd; text-align:center">{detail.criterion.max_observations}</td>'
                html += f'<td style="padding: 8px; border: 1px solid #ddd; text-align:center; background:#fff3cd">{detail.observations_count}</td>'
                html += f'<td style="padding: 8px; border: 1px solid #ddd; text-align:center; font-weight:bold">{score}</td>'
                html += f'<td style="padding: 8px; border: 1px solid #ddd; text-align:center; color:{color}; font-weight:bold">{percentage:.1f}%</td>'
                html += f'<td style="padding: 8px; border: 1px solid #ddd; text-align:center">{images_count} صورة</td>'
                html += f'</tr>'
            
            html += '</table>'
            return format_html(html)
        except Exception as e:
            return f"خطأ في عرض التفاصيل: {str(e)}"
    get_details_table.short_description = 'تفاصيل التقييم'