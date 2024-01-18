from django.urls import path
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from account.views import *
# from django.views.generic import RedirectView
from . import views
# from account.views import (DepositeView,)

# from django_registration.backends.one_step.views import RegistrationView


app_name = "account"

urlpatterns = [
    path('logout',views.logout_view,name='logout'),
	path('signup/', signup, name = 'signup'),
	
    
    path('login/', login_view, name = 'login'),

	path("password-reset/", 
    	PasswordResetView.as_view(template_name='user/password_reset.html'),
    	name="password_reset"),

	path("password-reset/done/", 
		PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'), 
		name="password_reset_done"),

	path("password-reset-confirm/<uidb64>/<token>/", 
		PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html'), 
		name="password_reset_confirm"),

	path("password-reset-complete/", 
		PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'), 
		name="password_reset_complete"),

	path('resendOTP', resend_otp),
	# path('followers', followers),
	# path('following', following),
	# path('notifications', notifications),
	# path('notifications/clear', clear_notifications),
	

  
    path('delete_user/<int:pk>/', views.DeleteUser.as_view(), name="delete_user"),


   
]
