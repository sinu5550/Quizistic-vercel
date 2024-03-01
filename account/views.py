from typing import Protocol
from django.shortcuts import render,redirect
from . import forms
from . import models
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.utils.safestring import mark_safe
from django.contrib.auth.forms import  PasswordChangeForm
from django.contrib.auth import  update_session_auth_hash
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
# Create your views here.

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Thank you for your email confirmation. Now you can login to your account.")
        return redirect('login')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('home')

def activateEmail(request, user, to_email):
    try:
        validate_email(to_email)
    except ValidationError as e:
        messages.error(request, f'Invalid email address: {to_email}. {e.message}')
        return

    mail_subject = "Activate your user account."
    message = render_to_string("activate_account.html", {
        'user': user,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        success_message = f'Dear <b>{user.first_name}</b>, please go to your email <b>{to_email}</b> inbox and click on the received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.'
        messages.success(request, mark_safe(success_message))
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')

def register(request):
    if request.method == 'POST':
        register_form = forms.RegistrationForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            user = register_form.save(commit=False)
            user.is_active=False
            user.save()
            activateEmail(request, user, register_form.cleaned_data.get('email'))
            return redirect('home')
        else:
            for error in list(register_form.errors.values()):
                messages.error(request, error)
    
    else:
        register_form = forms.RegistrationForm()
    return render(request, 'register.html', {'form' : register_form, 'type' : 'Register'})


class UserLoginView(LoginView):
    template_name = 'register.html'
    def get_success_url(self):
        return reverse_lazy('home')
    def form_valid(self, form):
        messages.success(self.request, 'Logged in Successful')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Logged in information incorrect')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Login'
        return context
    

class UserLogoutView(LogoutView):
    def get_success_url(self):
        return reverse_lazy('home')
    
@login_required
def profile(request):
    if request.method == 'POST':
        profile_form = forms.ChangeUserForm(request.POST, instance = request.user)
        user_account = getattr(request.user, 'account', None)
        profile_pic_form = forms.profilePicForm(request.POST, request.FILES or None,instance=user_account)
        if profile_form.is_valid() and profile_pic_form.is_valid():
            profile_form.save()
            profile_pic_form.instance.user = request.user
            profile_pic_form.save()
            
            messages.success(request, 'Profile Updated Successfully !')
            return redirect('profile')
    
    else:
        profile_form = forms.ChangeUserForm(instance = request.user)
        profile_pic_form = forms.profilePicForm(instance=getattr(request.user, 'account', None))
    return render(request, 'profile.html',{'form' : profile_form , 'profile_pic_form':profile_pic_form})

@login_required
def pass_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password Updated Successfully !')
            update_session_auth_hash(request, form.user)
            return redirect('profile')
    
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'pass_change.html', {'form' : form})