from django.db import models
from django.contrib.auth.models import AbstractUser

class AdministrativeStaff(AbstractUser):
    ROLE_CHOICES = [
        ('review_committee', 'Review Committee'),
        ('assessment_committee', 'Assessment Committee'),
        ('head_office', 'Head Office')
    ]
    roles = models.CharField(max_length=20, choices=ROLE_CHOICES, default='faculty')

    class Meta:
        verbose_name = "Administrative staff"

    def __str__(self):
        return self.username
