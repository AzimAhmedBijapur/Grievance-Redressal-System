from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Add your custom fields here
    full_name = models.CharField(max_length=100, blank=True)
    role = models.CharField(max_length=50, choices=[('Review Committee', 'Review Committee'), ('Assessment Committee', 'Assessment Committee'), ('HO', 'HO'),('Faculty','Faculty')])
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], blank=True)
    contact_no = models.CharField(max_length=15, blank=True)
    telephone_no = models.CharField(max_length=15, blank=True)
    current_address = models.CharField(max_length=150, blank=True)
    permanent_address = models.CharField(max_length=150, blank=True)
    educational_qualification = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=50, blank=True)
    designation = models.CharField(max_length=50, blank=True)
    permanent_employee = models.CharField(max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')], blank=True)
    date_of_probation = models.DateField(null=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    payscale = models.CharField(max_length=20, blank=True)
    

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'