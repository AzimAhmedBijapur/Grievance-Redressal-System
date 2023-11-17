from django.shortcuts import render,loader
from django.http import HttpResponse


# home page 
def home(request):
      return render(request, "assess/home.html")

# new registered grievance
def new_grievance(request):
        return render (request, "assess/new-grievance.html")
    
# view a particular grievance
def view_grievance(request):
        return render(request, "assess/view-grievance.html")