from django.contrib import admin
from .models import Investor , Favorite , InvestmentRequest, InvestorRatingComment, Report
from .models import Investor, Project
from django.db import models
from datetime import datetime

class InvestorAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_projects_count')
    
    
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
admin.site.register(Project)
admin.site.register(Favorite)
admin.site.register(InvestmentRequest, InvestmentRequestAdmin)
admin.site.register(InvestorRatingComment)
admin.site.register(Report)

