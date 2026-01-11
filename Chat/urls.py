from django.urls import path
from . import views

# Define urlpatterns even if Chat has no public routes yet to avoid include() errors
urlpatterns = []

# Example route (uncomment to enable)
# urlpatterns = [
#     path('services', views.services, name='services'),
# ]