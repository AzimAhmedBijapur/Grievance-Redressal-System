# Generated by Django 4.0.3 on 2023-09-19 04:50

from django.db import migrations, models
import login.models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0010_complaint'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint',
            name='documents',
            field=models.FileField(blank=True, null=True, upload_to=login.models.document_upload_to),
        ),
    ]
