from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .forms import CreateUserForm
from .forms import CreateMgmtUserForm
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required,user_passes_test
from .models import Complaint
from django.http import FileResponse, HttpResponse, Http404
import os
from django.conf import settings
from django.contrib.auth import get_user_model  # Import the User model
from django.http import FileResponse
from django.shortcuts import HttpResponse
import os
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password

# Check if user is admin or not
# This is used in decorator for management staff registeration view
def is_admin(user):
    return user.is_authenticated and user.is_staff

# Register faculties
def register(request):
    if request.method == 'POST':  
        form = CreateUserForm(request.POST)  
        if form.is_valid():  
            form.save()  
            messages.success(request, 'Account created successfully') 
            context = {  
            'form':form  
            } 
            return redirect('login')   
  
    else:  
        form = CreateUserForm()    
    context = {  
        'form':form  
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
            'form':form  
            } 
            return redirect('login')   
    else:  
        form = CreateMgmtUserForm()    
    context = {  
        'form':form  
    }  
    return render(request, 'register/register-mgmt.html', context)  

# Login page
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pw')
        role = request.POST.get('role')

        user = authenticate(request, username=username,password= password)

        if user is not None:
            # Check the role of the authenticated user
            if user.role == 'Review Committee':
                login(request, user)
                return redirect('review')
            elif user.role == 'Assessment Committee':
                login(request, user)
                return redirect('assess')
            elif user.role == 'Faculty':
                login(request, user)
                return redirect('faculty')
        else:
            messages.error(request,'Username or Password is incorrect')

    return render(request,'login/login.html')

# Logout
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def logoutUser(request):
    request.session.flush()
    logout(request)
    return redirect('index')

def index(request):
    return render(request, 'index.html')


# Faculty dashboard
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def faculty(request):
    user = request.user
    solved_complaints_count = Complaint.objects.filter(user=user,status='Solved').count()
    unsolved_complaints_count = Complaint.objects.filter(user=user,status='Unsolved').count()
    progress_complaints_count = Complaint.objects.filter(user=user,status='In-Progress').count()
    count_complaints = {
    'solved':solved_complaints_count,
    'unsolved':unsolved_complaints_count,
    'progress':progress_complaints_count
    }
    return render(request,'faculty/faculty.html',context=count_complaints)


# Add complaint - only for faculty
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def addComplaint(request):
    print(request)
    if request.method == 'POST':
        category = request.POST.get('category')
        subject = request.POST.get('subject')
        description = request.POST.get('description')
        documents = request.FILES['file-up']
        complaint = Complaint.objects.create(
            user=request.user,
            category=category,
            subject=subject,
            description=description,
            documents = documents
        )
        messages.success(request,"Complaint registered successfully")
        send_mail(
            subject=subject,
            message=description,
            from_email="whalefry@gmail.com",
            recipient_list=["azeembijapur786@gmail.com"],
            fail_silently=False,
        )
        return redirect('add/complaint')
    return render(request,'complaints/addComplaint.html')


# View complaint - only for faculty
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def viewMyComplaints(request):
    context ={}
    context["complaints"] = Complaint.objects.filter(user= request.user)
    return render(request,'complaints/viewMyComplaints.html',context)


# Download report - only for faculty
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def download_complaint_report(request, filename):
    file_directory = "complaints/reports/"  
    file_path = os.path.join(file_directory, filename)
    if os.path.exists(file_path):
        # If the file exists, serve it for download
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
    else:
        # If the file does not exist, return an error response
        return HttpResponse("File not found", status=404)


# Download document uploaded by faculty while complaint registeration
# for admin and mgmt staff
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def download_complaint_document(request, filename):
    file_directory = "complaints/documents/"  
    file_path = os.path.join(file_directory, filename)
    print(file_path)
    if os.path.exists(file_path):
        # If the file exists, serve it for download
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
    else:
        # If the file does not exist, return an error response
        return HttpResponse("File not found", status=404)