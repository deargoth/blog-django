from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),

    path('logout/', views.log_out, name='logout'),

    path('register/', views.Register.as_view(), name='register'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'),
         name='password_reset_confirm'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name="registration/password_reset_confirm.html"),
         name="password_reset_confirm"),

    path('password_reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name="registration/password_reset_complete"),
         name="password_reset_complete"),
]
