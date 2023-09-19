# Generated by Django 4.0.3 on 2023-09-19 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0022_alter_complaint_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint',
            name='status',
            field=models.CharField(choices=[('Solved', 'Solved'), ('Unsolved', 'Unsolved'), ('In-Progress', 'In-Progress')], default='Unsolved', max_length=100),
        ),
    ]
