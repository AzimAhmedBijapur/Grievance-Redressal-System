# Generated by Django 4.0.3 on 2023-09-19 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0021_complaint_due_date_complaint_report_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint',
            name='status',
            field=models.CharField(blank=True, default='Unsolved', max_length=100, null=True),
        ),
    ]
