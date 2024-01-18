from django.shortcuts import render, redirect
from account.forms import SignUpForm
from django.contrib.auth.models import User
from django.contrib import messages
import random
from .models import UserOTP,Wallet, Transaction
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.urls import reverse_lazy
from django.urls import reverse
from .forms import UserPublicDetailsForm,DepositForm
from django.http import  HttpResponse, HttpResponseRedirect
# from main.models import Post

from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import SignupForm, LoginUserForm, PasswordChangingForm, EditUserProfileForm, UserPublicDetailsForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView
# from main.models import Blog, BlogComment
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import UserProfuile

from .models import subscriptions


from django.db.models import Sum

from django.contrib.auth.models import User

import smtplib
from email.message import EmailMessage
from django.views import View
from django.views.generic import (
    
    CreateView, ListView
)
from django.utils.decorators import method_decorator
from decimal import Decimal
import string


from django.template.loader import render_to_string

import tempfile
from io import BytesIO

from io import BytesIO



def logout_view(request):
    """
    Logout
    """
    logout(request)
    messages.success(request, "You are logged out")
    return redirect('/')

def signup(request):
	if request.method == 'POST':
		get_otp = request.POST.get('otp') #213243 #None

		if get_otp:
			get_user = request.POST.get('usr')
			usr = User.objects.get(username=get_user)
			if int(get_otp) == UserOTP.objects.filter(user = usr).last().otp:
				usr.is_active = True
				usr.save()
				messages.success(request, f'Account has been Created For {usr.first_name}')
				return redirect(reverse('account:login'))
				# return redirect('account:login')
			else:
				messages.warning(request, f'You Entered a Wrong OTP')
				return render(request, 'user/login.html', {'otp': True, 'usr': usr})
        # if User.objects.filter(username=username):
        #     messages.error(request, "Username already exist! Try other username")
        #     return redirect('user/signup.html')
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			name = form.cleaned_data.get('name').split(' ')
       
	
			usr = User.objects.get(username=username)
			usr.email = username
			usr.first_name = name[0]
			if len(name) > 1:
				usr.last_name = name[1]
			usr.is_active = False
			usr.save()
			usr_otp = random.randint(100000, 999999)
			UserOTP.objects.create(user = usr, otp = usr_otp)

			mess = f"Hello {usr.first_name},\nYour OTP is {usr_otp}\nThanks!"

			send_mail(
				"Welcome to Badwin - Verify Your Email",
				mess,
				settings.EMAIL_HOST_USER,
				[usr.email],
				fail_silently = False
				)

			return render(request, 'user/signup.html', {'otp': True, 'usr': usr})

		
	else:
		form = SignUpForm()


	return render(request, 'user/signup.html', {'form':form})


def resend_otp(request):
	if request.method == "GET":
		get_usr = request.GET['usr']
		if User.objects.filter(username = get_usr).exists() and not User.objects.get(username = get_usr).is_active:
			usr = User.objects.get(username=get_usr)
			usr_otp = random.randint(100000, 999999)
			UserOTP.objects.create(user = usr, otp = usr_otp)
			mess = f"Hello {usr.first_name},\nYour OTP is {usr_otp}\nThanks!"

			send_mail(
				"Welcome to Badwin - Verify Your Email",
				mess,
				settings.EMAIL_HOST_USER,
				[usr.email],
				fail_silently = False
				)
			return HttpResponse("Resend")

	return HttpResponse("Can't Send ")


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        get_otp = request.POST.get('otp')

        if get_otp:
            get_usr = request.POST.get('usr')
            usr = User.objects.get(username__iexact=get_usr)
            if int(get_otp) == UserOTP.objects.filter(user=usr).last().otp:
                usr.is_active = True
                usr.save()
                login(request, usr)
                return redirect('home')
            else:
                messages.warning(request, 'You Entered a Wrong OTP')
                return render(request, 'user/login.html', {'otp': True, 'usr': usr})

        usrname = request.POST['username']
        passwd = request.POST['password']

        # user = User.objects.filter(username__iexact=usrname).first()
        user = authenticate(request, username=usrname, password=passwd)
        if user is not None:
            login(request, user)
            return redirect('/')
        elif not User.objects.filter(username__iexact=usrname).exists():
            messages.warning(request, 'Please enter a correct username and password. Note that both fields may be case-sensitive.')
            return redirect('account:login')
        elif not User.objects.get(username__iexact=usrname).is_active:
            usr = User.objects.get(username__iexact=usrname)
            usr_otp = random.randint(100000, 999999)
            UserOTP.objects.create(user=usr, otp=usr_otp)
            mess = f"Hello {usr.first_name},\nYour OTP is {usr_otp}\nThanks for shopping with us !"

            send_mail(
                "Welcome to Badwin - Verify Your Email",
                mess,
                settings.EMAIL_HOST_USER,
                [usr.email],
                fail_silently=False
            )
            return render(request, 'user/login.html', {'otp': True, 'usr': usr})
        else:
            messages.warning(request, 'Please enter a correct username and password. Note that both fields may be case-sensitive.')
            return redirect('account:login')

    form = AuthenticationForm()
    return render(request, 'user/login.html', {'form': form})
    









class PasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangingForm
    login_url = 'account:login'
    success_url = reverse_lazy('password_success')


def password_success(request):
    return render(request, "authors/password_change_success.html")


class UpdateUserView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    form_class = EditUserProfileForm
    login_url = 'account:login'
    template_name = "authors/edit_user_profile.html"
    success_url = reverse_lazy('home')
    success_message = "User updated"

    def get_object(slef):
        return slef.request.user

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR,
                             "Please submit the form carefully")
        return redirect('home')


class DeleteUser(LoginRequiredMixin, SuccessMessageMixin, generic.DeleteView):
    model = User
    login_url = 'account:login'
    template_name = 'authors/delete_user_confirm.html'
    success_message = "User has been deleted"
    success_url = reverse_lazy('home')

