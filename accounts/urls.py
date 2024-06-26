from . import views
from django.urls import path
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('signup', views.signup, name='signup'),
    path('profile', views.profile, name='profile'),
      # روابط إعادة تعيين كلمة المرور
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="accounts/password_reset_form.html"), name='reset_password'),
    path('reset_password_done/', auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"), name='password_reset_complete'),
      # روابط تغيير كلمة المرور
    path('owner_method', views.owner_method, name='owner_method'),
    path('inv_method', views.inv_method, name='inv_method'),
    path('change_password',
         auth_views.PasswordChangeView.as_view(
            template_name='accounts/change_password.html'),
         name='change_password'),
    path('password_change_done',
         auth_views.PasswordChangeDoneView.as_view(
            template_name='accounts/password_change_done.html'),
         name='password_change_done'),
]