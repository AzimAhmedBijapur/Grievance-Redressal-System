from pathlib import Path
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404,HttpResponse
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from grievances.models import Complaint
from django.core.mail import send_mail
from django.db.models import Q
import os
from grs.decorators import role_required
from login.models import CustomUser
import environ
from grs.dashboardCounts import complaintCounts
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

env = environ.Env()
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@role_required(allowed_roles=['HO'])
def ho(request):

    user = request.user
    count_complaints = complaintCounts()
    return render(request,'ho/ho.html',context=count_complaints)



@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@role_required(allowed_roles=['HO'])
def viewComplaints(request):
    complaints = Complaint.objects.filter( Q(status="Unsolved") | Q(status="In-Progress"))
    complaints = complaints.order_by('severity')
    context ={}
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
        return render(request,'ho/complaintsHo.html',context=context)
    return render(request,'ho/complaintsHo.html',context=context)


@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@role_required(allowed_roles=['HO'])
def viewDetailComplaints(request,cid):
    try:
        complaint = Complaint.objects.get(id=cid)
    except Complaint.DoesNotExist:
        raise Http404("Complaint does not exist")
    context = {
        "complaint":complaint
    }
    if request.method == 'POST':
        report = request.FILES['report']
        complaint.report = report
        try:
            complaint.save()
            messages.success(request, "Complaint updated")
        except:
            messages.error(request, "Complaint not updated")

        # Send ack mail to the admin staff

        mgmt_users = CustomUser.objects.filter(Q(role="Review Committee") | Q(role="Assessment Committee") | Q(is_superuser=True) | Q(username=complaint.user)).values_list('email',flat=True)
        email_list = list(mgmt_users)
        send_mail(
            subject="Report Upload by HO!",
            message = f"""

Dear Staff,

This is to inform you that a Report has been uploaded by HO for the following complaint:

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

        return redirect(request.get_full_path())

    return render(request,'ho/complaintDetailsHo.html',context=context)
