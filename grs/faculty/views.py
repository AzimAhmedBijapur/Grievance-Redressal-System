from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from grievances.models import Complaint
from django.http import HttpResponse
import os
from login.models import CustomUser
from django.utils.timezone import now
from django.core.mail import send_mail
from grs.decorators import role_required
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random
from transformers import BertTokenizer, BertForSequenceClassification
from torch.nn.functional import softmax
import torch

# semantic analysis

model_name = 'bert-base-uncased'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name, num_labels=3)


def perform_semantic_analysis(description):
    # Tokenize the description
    tokens = tokenizer(description, return_tensors='pt',
                       truncation=True, padding=True)

    # Make predictions
    with torch.no_grad():
        outputs = model(**tokens)

    # Apply softmax to get probabilities
    probabilities = softmax(outputs.logits, dim=1).squeeze()

    # Choose the severity level with the highest probability
    severity_levels = [1, 2, 3]
    predicted_severity = severity_levels[torch.argmax(probabilities).item()]

    return predicted_severity


def analyze_complaint_severity(description):
    severity = perform_semantic_analysis(description)
    return severity


# otp

def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp_email(email, otp):
    subject = 'OTP Verification'
    message = f'Your OTP for GRS registration is: {otp}'
    from_email = 'grs <whalefry@gmail.com>'  # Use your verified email here
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)

# Faculty dashboard


@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@role_required(allowed_roles=['Faculty'])
def faculty(request):
    user = request.user
    solved_complaints_count = Complaint.objects.filter(
        user=user, status='Solved').count()
    unsolved_complaints_count = Complaint.objects.filter(
        user=user, status='Unsolved').count()
    progress_complaints_count = Complaint.objects.filter(
        user=user, status='In-Progress').count()
    count_complaints = {
        'solved': solved_complaints_count,
        'unsolved': unsolved_complaints_count,
        'progress': progress_complaints_count
    }
    return render(request, 'faculty/faculty.html', context=count_complaints)


# Add complaint - only for faculty
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@role_required(allowed_roles=['Faculty'])
def addComplaint(request):
    print(request.user)
    if request.method == 'POST':
        category = request.POST.get('category')
        subject = request.POST.get('subject')
        description = request.POST.get('description')
        documents = request.FILES['file-up']
        date = now()
        severity = analyze_complaint_severity(description)
        complaint = Complaint.objects.create(
            user=request.user,
            category=category,
            subject=subject,
            description=description,
            documents=documents,
            date=date,
            severity=severity
        )
        messages.success(request, "Complaint registered successfully")
        # Send ack mail to the faculty itself
        send_mail(
            subject="Received Grievance!",
            message=f"""
Dear staff,\n
We have received your grievance about subject *{subject}* and assigned it reference number {complaint.id}.\nYou can check the status of your complaints from the dashboard and download reports when available.\n
\nFor questions or additional information, contact us at grievances@mhssce.ac.in .

Thank you for your feedback.

Sincerely,
grs@mhssce

                        """,
            from_email="whalefry@gmail.com",
            recipient_list=[str(request.user)],
            fail_silently=False,
        )
        # Send ack mail to the admin staff

        mgmt_users = CustomUser.objects.filter(Q(role="Review Committee") | Q(
            role="Assessment Committee") | Q(is_superuser=True)).values_list('email', flat=True)
        email_list = list(mgmt_users)
        send_mail(
            subject="New Grievance Registered!",
            message=f"""

Dear Staff,

This is to inform you that a new grievance has been registered in the system by a faculty member.

Ref no. : {complaint.id},
Subject : {subject},
Description : {description},
By : {request.user.full_name}

Thank you for your attention.\n

Sincerely,
grs@mhssce

                        """,
            from_email="whalefry@gmail.com",
            recipient_list=email_list,
            fail_silently=False,
        )
        return redirect('add/complaint')
    return render(request, 'faculty/addComplaint.html')


# View complaint - only for faculty
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@role_required(allowed_roles=['Faculty'])
def viewMyComplaints(request):
    context = {}
    complaints = Complaint.objects.filter(user=request.user)

    if request.method == 'POST':
        ref = request.POST.get('ref')
        complaints = Complaint.objects.filter(id=ref, user=request.user)
        if not complaints:
            messages.error(request, 'No such complaints found')
            return redirect(request.get_full_path())
        context = {
            "complaints": complaints
        }
        return render(request, 'faculty/viewMyComplaints.html', context=context)

    items_per_page = 10  # Number of items to display per page
    # Get the current page number from the URL parameter
    page_number = request.GET.get('page')

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

    return render(request, 'faculty/viewMyComplaints.html', context)

# View solved complaint - only for faculty


@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@role_required(allowed_roles=['Faculty'])
def viewMySolvedComplaints(request):
    context = {}
    if request.method == 'POST':
        ref = request.POST.get('ref')
        complaints = Complaint.objects.filter(
            id=ref, user=request.user, status="Solved")
        if not complaints:
            messages.error(request, 'No such complaints found')
            return redirect(request.get_full_path())
        context = {
            "complaints": complaints
        }
        return render(request, 'faculty/viewMySolvedComplaints.html', context=context)
    complaints = Complaint.objects.filter(user=request.user, status="Solved")
    items_per_page = 10  # Number of items to display per page
    # Get the current page number from the URL parameter
    page_number = request.GET.get('page')

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
    return render(request, 'faculty/viewMySolvedComplaints.html', context)


# Download report - only for faculty
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@role_required(allowed_roles=['Faculty'])
def download_complaint_report(request, filename):
    file_directory = "/home/grsmhssce/Grievance-Redressal-System/grs/complaints/reports/"
    file_path = os.path.join(file_directory, filename)
    print(file_path)
    if os.path.exists(file_path):
        # If the file exists, serve it for download
        with open(file_path, 'rb') as file:
            response = HttpResponse(
                file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
    else:
        # If the file does not exist, return an error response
        return HttpResponse("File not found", status=404)
