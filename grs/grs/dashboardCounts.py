from grievances.models import Complaint

def complaintCounts():

    # Count of complaints per category for dashboard

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

    return count_complaints