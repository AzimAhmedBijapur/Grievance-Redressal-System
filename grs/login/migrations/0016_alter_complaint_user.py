# Generated by Django 4.0.3 on 2023-09-19 05:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0015_alter_complaint_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
