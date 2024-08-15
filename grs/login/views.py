from pathlib import Path
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .forms import CreateUserForm
from .forms import CreateMgmtUserForm
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
import os
from functools import wraps
import pyotp
import re
from django.core.mail import send_mail
from django.shortcuts import HttpResponse
import os
import environ

env = environ.Env()
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Allow access to register page for faculty only after email verification

def otp_verified_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Check if OTP verification is done
        if request.session.get('otp_verified', False):
            return view_func(request, *args, **kwargs)
        else:
            # Redirect to the OTP verification page if not verified
            # Change 'otp_input' to your actual OTP verification URL
            return redirect('otp_verification')

    return _wrapped_view


# Check if user is admin or not
# This is used in decorator for management staff registeration view

def is_admin(user):
    return user.is_authenticated and user.is_staff

# Register faculties

def verify(request):
    if request.method == 'POST':
        totp = pyotp.TOTP(pyotp.random_base32())
        otp = totp.now()
        email_domain = 'mhssce.ac.in'

        entered_email = request.POST.get("email")

        if entered_email.endswith('@' + email_domain) or env('IS_TESTING'):
            # Email matches the specified domain, validate the name part
            name_without_domain = entered_email.split('@')[0]

            # Use a regex to check if the name follows the specified format
            name_pattern = re.compile(r'^[a-zA-Z.]+$')
            # name_pattern = re.compile(r'^[a-zA-Z0-9.]+$')

            if name_pattern.match(name_without_domain) or env('IS_TESTING'):
                # Name follows the specified format, send OTP
                subject = 'Your OTP for GRS Registration'
                message = f'Your OTP is {otp}.'
                from_email = env('EMAIL')
                recipient_list = [entered_email]
                send_mail(subject, message, from_email, recipient_list)
                context = {"otp": otp}
                request.session['otp'] = otp
                return redirect('otp_input')
            else:
                # Name does not follow the specified format, show error
                messages.error(
                    request, 'Invalid email format, only faculties with college domain can register')
                return redirect('otp_verification')
        else:
            # Email does not match the specified domain, show error
            messages.error(
                request, 'Invalid email domain, you can only register with college domain')
            return redirect('otp_verification')

    return render(request, 'register/otp.html')


def otp_input(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp', '')
        stored_otp = request.session.get('otp', '')
        attempts = request.session.get('otp_attempts', 0)

        if entered_otp == stored_otp:
            # OTP is correct, set a flag in the session
            request.session['otp_verified'] = True
            request.session.pop('otp_attempts', None)  # Reset attempts counter
            return redirect('register')
        else:
            # Increment attempts counter
            attempts += 1
            request.session['otp_attempts'] = attempts

            if attempts >= 3:
                # Exceeded maximum attempts, take appropriate action
                messages.error(
                    request, 'Maximum attempts exceeded. Please try again later.')
                # Redirect to an error page or OTP verification page
                return redirect('otp_verification')

            messages.error(
                request, f'Invalid OTP. {3 - attempts} attempts remaining. Please try again.')

    return render(request, 'register/otp_input.html')


@otp_verified_required
def register(request):
    if not request.session.get('otp_verified', False):
        messages.error(request, 'Please verify your OTP first.')
        return redirect('otp_input')
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')
            context = {
                'form': form
            }
            return redirect('login')

    else:
        form = CreateUserForm()
    context = {
        'form': form
    }
    return render(request, 'register/register.html', context)

# Register management staff only by admin

@user_passes_test(is_admin)
def registerManagementStaff(request):
    if request.method == 'POST':
        form = CreateMgmtUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')
            context = {
                'form': form
            }
            return redirect('login')
    else:
        form = CreateMgmtUserForm()
    context = {
        'form': form
    }
    return render(request, 'register/register-mgmt.html', context)

# Login page

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pw')
        role = request.POST.get('role')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Check the role of the authenticated user
            if user.role != role:
                messages.error(request, 'Role incorrect')
            elif user.role == 'Review Committee':
                login(request, user)
                return redirect('review')
            elif user.role == 'Assessment Committee':
                login(request, user)
                return redirect('assessment')
            elif user.role == 'Faculty':
                login(request, user)
                return redirect('faculty')
            elif user.role == 'HO':
                login(request, user)
                return redirect('ho')
        else:
            messages.error(request, 'Username or Password is incorrect')

    return render(request, 'login/login.html')

# Logout

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logoutUser(request):
    request.session.flush()
    logout(request)
    return redirect('index')


def index(request):
    return render(request, 'index.html')

# Download document uploaded by faculty while complaint registeration
# for admin and mgmt staff


