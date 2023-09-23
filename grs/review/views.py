from django.http import Http404
from django.shortcuts import render,redirect
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from login.models import Complaint
from django.contrib import messages

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def reviewDashboard(request):
    user = request.user
    solved_complaints_count = Complaint.objects.filter(status='Solved').count()
    unsolved_complaints_count = Complaint.objects.filter(status='Unsolved').count()
    progress_complaints_count = Complaint.objects.filter(status='In-Progress').count()

    solved_complaints_academic = Complaint.objects.filter(status='Solved',category='Academic').count()
    unsolved_complaints_academic= Complaint.objects.filter(status='Unsolved',category='Academic').count()
    progress_complaints_academic = Complaint.objects.filter(status='In-Progress',category='Academic').count()

    solved_complaints_administrative = Complaint.objects.filter(status='Solved', category='Administrative').count()
    unsolved_complaints_administrative = Complaint.objects.filter(status='Unsolved', category='Administrative').count()
    progress_complaints_administrative = Complaint.objects.filter(status='In-Progress', category='Administrative').count()

    solved_complaints_interpersonal = Complaint.objects.filter(status='Solved', category='Interpersonal').count()
    unsolved_complaints_interpersonal = Complaint.objects.filter(status='Unsolved', category='Interpersonal').count()
    progress_complaints_interpersonal = Complaint.objects.filter(status='In-Progress', category='Interpersonal').count()

    solved_complaints_miscellaneous = Complaint.objects.filter(status='Solved', category='Miscellaneous').count()
    unsolved_complaints_miscellaneous = Complaint.objects.filter(status='Unsolved', category='Miscellaneous').count()
    progress_complaints_miscellaneous = Complaint.objects.filter(status='In-Progress', category='Miscellaneous').count()

    count_complaints = {
    'solved':solved_complaints_count,
    'unsolved':unsolved_complaints_count,
    'progress':progress_complaints_count,
    'solved_academic':solved_complaints_academic,
    'unsolved_academic':unsolved_complaints_academic,
    'progress_academic':progress_complaints_academic,
    'solved_administrative': solved_complaints_administrative,
    'unsolved_administrative': unsolved_complaints_administrative,
    'progress_administrative': progress_complaints_administrative,
    'solved_interpersonal': solved_complaints_interpersonal,
    'unsolved_interpersonal': unsolved_complaints_interpersonal,
    'progress_interpersonal': progress_complaints_interpersonal,
    'solved_miscellaneous': solved_complaints_miscellaneous,
    'unsolved_miscellaneous': unsolved_complaints_miscellaneous,
    'progress_miscellaneous': progress_complaints_miscellaneous,
    }
    return render(request,'review/review.html',context=count_complaints)

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def viewComplaints(request):
    complaints = Complaint.objects.all()
    context = {
        "complaints":complaints
    }
    return render(request,'review/viewComplaints.html',context=context)

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def detailComplaints(request,cid):
    try:
        complaint = Complaint.objects.get(id=cid)
    except Complaint.DoesNotExist:
        raise Http404("Complaint does not exist") 
    context = {
        "complaint":complaint
    }
    if request.method == 'POST':
        severity = request.POST.get('severity')
        duedate = request.POST.get('due-date')
        complaint.severity = severity
        complaint.due_date = duedate
        try:
            complaint.save()
            messages.success(request,"Complaint updated")
        except:
            messages.error(request,"Complaint not updated")
        return redirect(request.get_full_path())  

    return render(request,'review/detailComplaint.html',context=context)