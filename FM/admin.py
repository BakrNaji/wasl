from django.contrib import admin
from .models import Promotype, PromoRequest, FinancialMovement, FinancialReport

@admin.action(description='Generate daily financial report')
def generate_daily_report(modeladmin, request, queryset):
    report = FinancialReport()
    report.generate_report()
    report.save()

class FinancialMovementAdmin(admin.ModelAdmin):
    list_display = ('statement', 'income', 'outcome', 'date', 'pay_method')
    actions = [generate_daily_report]

class FinancialReportAdmin(admin.ModelAdmin):
    list_display = ('date', 'total_income', 'total_outcome', 'net_income', 'promo_details', 'investment_total_amount')
    readonly_fields = ('date', 'total_income', 'total_outcome', 'net_income', 'promo_projects', 'promo_owners', 'promo_total_amount', 'invested_projects', 'investors', 'investment_total_amount')

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = 'Financial Reports'
        response = super(FinancialReportAdmin, self).changelist_view(request, extra_context)
        return response

    def promo_details(self, obj):
        promo_details = ''
        for promo_request in obj.promo_requests.all():
            if promo_details:
                promo_details += ', '
            promo_details += f'{promo_request.promo_type.promo_name} ({promo_request.project.title}) - {promo_request.owner.user.username}'
        return promo_details

admin.site.register(Promotype)
admin.site.register(PromoRequest)
admin.site.register(FinancialMovement, FinancialMovementAdmin)
admin.site.register(FinancialReport, FinancialReportAdmin)
