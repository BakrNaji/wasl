from . import views
from django.urls import path


urlpatterns = [
    path('invreq/<int:project_id>/', views.invreq, name='invreq'),
    path('promoreq/<int:project_id>/', views.promoreq, name='promoreq'),
    
]