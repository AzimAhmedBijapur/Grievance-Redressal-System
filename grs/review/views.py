from pathlib import Path
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404, HttpResponse
import os
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from grievances.models import Complaint
from django.core.mail import send_mail
from django.db.models import Q
from login.models import CustomUser
from grs.decorators import role_required
import environ
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from grs.dashboardCounts import complaintCounts

env = environ.Env()
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@role_required(allowed_roles=['Review Committee'])
def review(request):
    user = request.user
    count_complaints = complaintCounts()
    return render(request,'review/review.html',context=count_complaints)


@role_required(allowed_roles=['Review Committee'])
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def viewComplaints(request):
    complaints = Complaint.objects.filter( Q(status="Unsolved") | Q(status="In-Progress"))
    complaints = complaints.order_by('severity')
    items_per_page = 10  # Number of items to display per page
    page_number = request.GET.get('page')  # Get the current page number from the URL parameter

    # Set a default page number in case 'page' is not provided
    page_number = page_number if page_number else 1

    paginator = Paginator(complaints, items_per_page)

    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    context = {
        "complaints": page,  # Pass the current page to the template
    }
    if request.method == 'POST':
        ref = request.POST.get('ref')
        complaints = Complaint.objects.filter(id = ref)
        if not complaints:
            messages.error(request,'No such complaints found')
            return redirect(request.get_full_path())
        context = {
        "complaints":complaints
        }
        return render(request,'review/complaintsReview.html',context=context)
    return render(request,'review/complaintsReview.html',context=context)


@role_required(allowed_roles=['Review Committee'])
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def viewDetailComplaints(request,cid):
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
        escalate = request.POST.get('escalatetoho')
        complaint.status = 'In-Progress'

        if severity is not None:
            complaint.severity = severity

        if not duedate == '':
            complaint.due_date = duedate

        if escalate is not None:
            complaint.escalatetoHo = escalate

        try:
            complaint.save()
            messages.success(request, "Complaint updated")
            if escalate == "No" or escalate is None:
                mgmt_users = CustomUser.objects.filter(Q(role="Assessment Committee") 
                                                     | Q(is_superuser=True) 
                                                     | Q(role="Review Committee")).values_list('email',flat=True)
                email_list = list(mgmt_users)
                send_mail(
                subject="Review committee updated the complaint!",
                message = f"""

    Dear Staff,

    This is to inform you that Review committee has updated the following complaint:

    Ref no. : {complaint.id},
    Subject : {complaint.subject},
    Description : {complaint.description},

    Thank you for your attention.\n

    Sincerely,
    grs@mhssce

                            """,
                from_email=env("EMAIL"),
                recipient_list=email_list,
                fail_silently=False,
            )
            # Escalate to head office
            elif escalate == 'Yes':
                mgmt_users = CustomUser.objects.filter(Q(role="HO") | Q(is_superuser=True) | Q(role="Assessment Committee")| Q(role="Review Committee") | Q(email=str(complaint.user))).values_list('email',flat=True)
                email_list = list(mgmt_users)
                send_mail(
                subject="Grievance Escalated to HO",
                message = f"""

    Dear Staff,

    This is to inform you that the following grievance has been sent to HO for Redressal:

    Ref no. : {complaint.id},
    Subject : {complaint.subject},
    Description : {complaint.description},

    Thank you for your attention.\n

    Sincerely,
    grs@mhssce

                            """,
                from_email=env("EMAIL"),
                recipient_list=email_list,
                fail_silently=False,
            )

        except:
            messages.error(request, "Complaint not updated")

        return redirect(request.get_full_path())

    return render(request,'review/complaintDetailsReview.html',context=context)

