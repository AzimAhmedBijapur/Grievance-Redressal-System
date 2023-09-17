# Generated by Django 4.0.3 on 2023-09-17 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0005_alter_customuser_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='full_name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='current_address',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='permanent_address',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]