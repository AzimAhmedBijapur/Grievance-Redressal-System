# Generated by Django 4.2.5 on 2023-10-17 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grievances', '0007_alter_complaint_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint',
            name='severity',
            field=models.IntegerField(),
        ),
    ]
