from . import views
from django.urls import path


urlpatterns = [
    path('', views.index , name='index'),
    path('about', views.about, name='about'),
    path('evaluate/<int:investor_id>/', views.evaluate_investor, name='evaluate_investor'),
    path('investors/', views.investor_list, name='investor_list'),
    path('ajax/departments/<int:branch_id>/', views.ajax_departments, name='ajax_departments'),
    path('ajax/investors/', views.ajax_investors, name='ajax_investors'),
    
    # نظام التقييم الجديد
    path('evaluate-department/', views.evaluate_department, name='evaluate_department'),
    path('evaluate-employee/', views.evaluate_employee, name='evaluate_employee'),
    path('evaluation-reports/', views.evaluation_reports, name='evaluation_reports'),
    path('edit-employee/<int:employee_id>/', views.edit_employee, name='edit_employee'),

    
]