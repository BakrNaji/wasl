from django.contrib import admin
from .models import Investor , Favorite , InvestmentRequest, InvestorRatingComment, Report, Evaluation
from .models import Investor, Project, Evaluation
from .models import EvaluationCriterion, EvaluationScore, EvaluationImage
from django.db import models
from datetime import datetime
from django.urls import path
from django.shortcuts import render
from django.contrib import admin
from django.db.models import Avg, Count, StdDev
from django.contrib.admin import AdminSite
from django.utils.html import format_html
from django.utils.safestring import mark_safe

class InvestorAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_projects_count', 'branch', 'department')
    
    
    def get_projects_count(self, obj):
        # obj هنا يمثل كائن المستثمر الحالي
        return len(obj.invested_projects())

    get_projects_count.short_description = 'Number of Invested Projects'


    def invested_projects(self, obj):
        # الحصول على جميع طلبات الاستثمار المرتبطة بالمستثمر
        investment_requests = obj.investmentrequest_set.all()
        # استخدام قائمة التفهيم (list comprehension) للحصول على المشاريع المرتبطة بطلبات الاستثمار
        return [investment_request.project for investment_request in investment_requests]

class InvestmentRequestAdmin(admin.ModelAdmin):
    list_display = ('project_id', 'investor', 'is_allowed')
    list_filter = ('is_allowed',)
    search_fields = ('project_id', 'investor__user__username')
    actions = ['make_allowed']

    def make_allowed(self, request, queryset):
        queryset.update(is_allowed=True)
    make_allowed.short_description = "Mark selected requests as allowed"


admin.site.register(Investor, InvestorAdmin)
# Project removed from admin per request
# Removed from admin per request: Favorite, InvestmentRequest, InvestorRatingComment, Report
 

class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('investor', 'evaluator', 'overall_score', 'status', 'created_at', 'first_image')
    readonly_fields = ('first_image',)
    inlines = []  # will append inline below

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('stats/', self.admin_site.admin_view(self.stats_view), name='evaluation-stats'),
        ]
        return my_urls + urls

    def stats_view(self, request):
        # Only staff allowed via admin_view wrapper
        # Aggregations
        approved_qs = Evaluation.objects.filter(status='approved')

        avg_by_department = list(approved_qs.values('investor__department')
                                 .exclude(investor__department='')
                                 .annotate(avg=Avg('overall_score'), count=Count('id'))
                                 .order_by('-avg'))

        avg_by_branch = list(approved_qs.values('investor__branch')
                             .exclude(investor__branch='')
                             .annotate(avg=Avg('overall_score'), count=Count('id'))
                             .order_by('-avg'))

        # lowest 10 employees by average approved score
        per_investor = approved_qs.values('investor__id', 'investor__user__username', 'investor__department')
        per_investor = per_investor.annotate(avg=Avg('overall_score')).order_by('avg')[:10]

        # departmental std devs (for deviations)
        dept_stats = approved_qs.values('investor__department').exclude(investor__department='')
        dept_stats = dept_stats.annotate(avg=Avg('overall_score'), std=StdDev('overall_score'))
        dept_map = {d['investor__department']: {'avg': d['avg'], 'std': d['std']} for d in dept_stats}

        # compute outliers: investors whose avg deviates > 2*std from dept avg
        all_investor_avgs = approved_qs.values('investor__id', 'investor__user__username', 'investor__department').annotate(avg=Avg('overall_score'))
        outliers = []
        for inv in all_investor_avgs:
            dept = inv.get('investor__department')
            stats = dept_map.get(dept)
            if stats and stats.get('std'):
                try:
                    z = (inv['avg'] - stats['avg']) / stats['std']
                except Exception:
                    z = 0
                if abs(z) >= 2:
                    outliers.append({'investor': inv['investor__user__username'], 'dept': dept, 'avg': inv['avg'], 'z': round(z, 2)})

        # prepare chart data for departments
        chart_labels = [d['investor__department'] for d in avg_by_department]
        chart_data = [float(d['avg'] or 0) for d in avg_by_department]

        context = dict(
            self.admin_site.each_context(request),
            avg_by_department=avg_by_department,
            avg_by_branch=avg_by_branch,
            lowest_employees=list(per_investor),
            outliers=outliers,
            chart_labels=chart_labels,
            chart_data=chart_data,
        )
        return render(request, 'admin/evaluation_stats.html', context)


class EvaluationImageInline(admin.TabularInline):
    model = EvaluationImage
    extra = 0
    readonly_fields = ('thumb',)
    fields = ('thumb', 'image')

    def thumb(self, obj):
        if obj and getattr(obj, 'image', None):
            try:
                return mark_safe(f'<img src="{obj.image.url}" style="max-height:120px; max-width:160px;" />')
            except Exception:
                return '-'
        return '-'
    thumb.short_description = 'صورة'


# attach inline to admin
EvaluationAdmin.inlines = [EvaluationImageInline]

def first_image(self, obj):
    img = obj.images.first()
    if img and getattr(img, 'image', None):
        try:
            return mark_safe(f'<img src="{img.image.url}" style="max-height:60px; max-width:80px;" />')
        except Exception:
            return '-'
    return '-'

first_image.short_description = 'معاينة'
EvaluationAdmin.first_image = first_image


admin.site.register(Evaluation, EvaluationAdmin)
admin.site.register(EvaluationCriterion)
admin.site.register(EvaluationImage)
from .models import Branch, Department
from django import forms

# Inline to show departments within branch (read-only names)
class DepartmentInline(admin.TabularInline):
    model = Department
    extra = 1
    fields = ('name', 'edit_link')
    readonly_fields = ('edit_link',)
    verbose_name = 'القسم'
    verbose_name_plural = 'الأقسام المرتبطة بهذا الفرع'
    can_delete = True
    show_change_link = True
    
    def edit_link(self, obj):
        if obj.pk:
            from django.urls import reverse
            from django.utils.html import format_html
            url = reverse('admin:The_Investor_department_change', args=[obj.pk])
            return format_html('<a href="{}" target="_blank">تعديل الاسم</a>', url)
        return '-'
    edit_link.short_description = 'إجراء'
    
    def get_readonly_fields(self, request, obj=None):
        # إذا كان القسم موجود مسبقاً، اجعل الاسم للقراءة فقط
        if obj and obj.pk:
            return self.readonly_fields + ('name',)
        return self.readonly_fields

# Branch Admin - name editable only in detail page
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_departments_count', 'get_departments_list')
    list_editable = []  # لا يمكن التعديل من القائمة
    inlines = [DepartmentInline]
    search_fields = ('name',)
    fields = ('name',)
    
    def get_departments_count(self, obj):
        return obj.departments.count()
    
    get_departments_count.short_description = 'عدد الأقسام'
    
    def get_departments_list(self, obj):
        departments = obj.departments.all()
        if departments:
            return ', '.join([dept.name for dept in departments])
        return '-'
    
    get_departments_list.short_description = 'الأقسام'

# Department Admin - name and branch editable only in detail page
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'branch', 'edit_action')
    list_editable = []  # لا يمكن التعديل من القائمة
    list_filter = ('branch',)
    search_fields = ('name', 'branch__name')
    fields = ('name', 'branch')
    list_per_page = 50
    
    def edit_action(self, obj):
        from django.urls import reverse
        from django.utils.html import format_html
        url = reverse('admin:The_Investor_department_change', args=[obj.pk])
        return format_html('<a href="{}">تعديل</a>', url)
    
    edit_action.short_description = 'إجراء'
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "branch":
            kwargs["queryset"] = Branch.objects.all().order_by('name')
            kwargs["empty_label"] = "اختر الفرع"
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Branch, BranchAdmin)
admin.site.register(Department, DepartmentAdmin)

