from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.db import models
from datetime import date


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(unique=True, max_length=50)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(max_length=254, blank=True)
    Enrollment_No = models.CharField(max_length=20, unique=True, default="")
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to="profile_pics/", blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    Task_id = models.AutoField(primary_key=True, auto_created=True)
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    due_date = models.DateField(default=date.today)
    priority = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}"


class Assignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    Assignment_id = models.AutoField(primary_key=True, auto_created=True)
    subject = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateField(blank=True)
    Assignment_files = models.FileField(
        upload_to="Uploaded_files/Assignment_pdfs/", blank=True
    )
    status = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.title}"


class Material(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    Material_id = models.AutoField(primary_key=True, auto_created=True)
    subject = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date_added = models.DateField(default=date.today)
    Assignment_files = models.FileField(
        upload_to="Uploaded_files/Materials/", blank=True
    )

    def __str__(self):
        return f"{self.title}"


class Reminder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    Reminder_id = models.AutoField(primary_key=True, auto_created=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    R_date = models.DateField(blank=False)
    R_time = models.TimeField(blank=False)
    Location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.title}"


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    Expense_id = models.AutoField(primary_key=True, auto_created=True)
    title = models.CharField(max_length=255)
    amount = models.DecimalField(null=False, max_digits=20, decimal_places=2)
    date = models.DateField(default=date.today)
    time = models.TimeField(default=timezone.now)
    Location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.title}"
