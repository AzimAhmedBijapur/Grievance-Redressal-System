from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from grievances.models import Complaint
from django.core.mail import send_mail
from django.db.models import Q
from grs.decorators import role_required
from login.models import CustomUser
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@role_required(allowed_roles=['Assessment Committee'])
def assessment(request):
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
    return render(request,'assessment/assessment.html',context=count_complaints)



@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@role_required(allowed_roles=['Assessment Committee'])
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
        return render(request,'assessment/complaintsAssessment.html',context=context)
    return render(request,'assessment/complaintsAssessment.html',context=context)


@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@role_required(allowed_roles=['Assessment Committee'])
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

        mgmt_users = CustomUser.objects.filter(Q(role="Review Committee") | Q(role="Assessment Committee") | Q(is_superuser=True) | Q(username= complaint.user)).values_list('email',flat=True)
        email_list = list(mgmt_users)
        send_mail(
            subject="Report Upload by Assessment Committee!",
            message = f"""

Dear Staff,

This is to inform you that a Report has been uploaded by Assessment Committee for the following complaint:

Ref no. : {complaint.id},
Subject : {complaint.subject},
Description : {complaint.description},

Thank you for your attention.\n

Sincerely,
grs@mhssce

                        """,
            from_email="whalefry@gmail.com",
            recipient_list=email_list,
            fail_silently=False,
        )
            
        return redirect(request.get_full_path())

    return render(request,'assessment/complaintDetailsAssessment.html',context=context)
