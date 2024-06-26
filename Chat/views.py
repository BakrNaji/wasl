# # from django.shortcuts import render

# # # Create your views here.
# # from django.shortcuts import render

# # def payment_page(request):
# #     return render(request, 'pages/payment.html')

# from django.shortcuts import render
# from .models import  FeasibilityStudyRequest, FeasibilityStudy

# def services(request):
#     user_projects = Project.objects.filter(user=request.user).prefetch_related('feasibility_studies')

#     user_requests = FeasibilityStudyRequest.objects.filter(user=request.user)
    
#     # جلب تفاصيل دراسة الجدوى إذا كانت is_allowed=True
#     feasibility_details = {}
#     for request in user_requests:
#         if request.is_allowed:
#             feasibility_details[request.id] = FeasibilityStudy.objects.filter(project_name=request.project_name).first()

#     return render(request, 'pages/services.html', {
#         'user_requests': user_requests,
#         'feasibility_details': feasibility_details
#     })
