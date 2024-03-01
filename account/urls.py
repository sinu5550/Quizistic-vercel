from django.urls import path
from . import views
from django.contrib.auth import views as auth_views 

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/',views.UserLogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/pass_change/', views.pass_change, name='pass_change'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),


    ######### forgotten password ##############

    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='pass_reset/password_reset_form.html',email_template_name='pass_reset/password_reset_email.html'),name='password_reset'),
 
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='pass_reset/password_reset_done.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='pass_reset/password_reset_confirm.html'),name='password_reset_confirm'),
 
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name='pass_reset/password_reset_complete.html'),name='password_reset_complete')
]