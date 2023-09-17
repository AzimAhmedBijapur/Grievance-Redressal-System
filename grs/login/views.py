from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm  
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import CreateUserForm

def register(request):
    if request.method == 'POST':  
        form = CreateUserForm(request.POST)  
        if form.is_valid():  
            form.save()  
            messages.success(request, 'Account created successfully') 
            return render(request, 'register/register.html', context)   
  
    else:  
        form = CreateUserForm()    
    context = {  
        'form':form  
    }  
    return render(request, 'register/register.html', context)  
