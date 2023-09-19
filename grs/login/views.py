from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .forms import CreateUserForm
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from .models import Complaint
from django.http import HttpResponse, Http404
import os
from django.conf import settings

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

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pw')
        role = request.POST.get('role')
        print(role)

        user = authenticate(request, username=username,password= password)

        if user is not None:
            if role == '1':
                login(request,user)
                return redirect('faculty')
        else:
            messages.error(request,'Username or Password is incorrect')

    return render(request,'login/login.html')

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def logoutUser(request):
    request.session.flush()
    logout(request)
    return redirect('index')

def index(request):
    return render(request, 'index.html')


@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def faculty(request):
    return render(request,'faculty/faculty.html')


@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def addComplaint(request):
    print(request)
    if request.method == 'POST':
        category = request.POST.get('category')
        subject = request.POST.get('subject')
        description = request.POST.get('description')
        documents = request.FILES['file-up']

        if category == '1':
            category = 'Management'
        elif category == '2':
            category = 'Students'
        elif category == '2':
            category = 'Infrastructure'
        else:
            category = 'Salary'
        complaint = Complaint.objects.create(
            user=request.user,
            category=category,
            subject=subject,
            description=description,
            documents = documents
        )
        messages.success(request,"Complaint registered successfully")
        return redirect('add/complaint')
    return render(request,'complaints/addComplaint.html')


@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def viewMyComplaints(request):
    context ={}
    context["complaints"] = Complaint.objects.filter(user= request.user)
    return render(request,'complaints/viewMyComplaints.html',context)


