from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.decorators.cache import cache_control
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
import re
#from .models import Item

# Create your views here.

#function for register
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        elif len(username) < 4:
            error_message = "Username must be at least 4 characters long."
            messages.error(request, error_message)
            return redirect('/')
        if not is_valid_email(email):
            error_message = "Invalid email address."
            messages.error(request, error_message)
            return redirect('/')
        elif not any(char.isupper() for char in password) or not any(char.islower() for char in password):
            error_message = "Password must contain both uppercase and lowercase letters."
            messages.error(request, error_message)
            return redirect('/')
        else:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            messages.success(request, 'Account created successfully')
            return redirect('login')
    return render(request, 'register.html')

#function for email vlidtion
def is_valid_email(email):
    # Regular expression for validating an email address
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(email_regex, email)
#function for login
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_login(request):
     #if already loggedin redirect to home
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_logout(request):
    logout(request)
    request.session.flush()
    return redirect('login')
#function for homepage
@login_required
@never_cache
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    return render(request, 'home.html',)
@method_decorator(never_cache, name='dispatch')
class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'