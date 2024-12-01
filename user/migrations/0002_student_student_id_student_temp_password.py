# Generated by Django 5.1.2 on 2024-11-25 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='student_id',
            field=models.CharField(blank=True, editable=False, max_length=5, unique=True),
        ),
        migrations.AddField(
            model_name='student',
            name='temp_password',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]