from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from .manager import *
import datetime


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(unique=True, max_length=50)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    Enrollment_No = models.CharField(max_length=20, unique=True, default="")
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to="profile_pics/", blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    PRIORITY = [
        ("important", "Important"),
        ("not important", "Not Important"),
    ]
    Task_id = models.AutoField(primary_key=True, auto_created=True)
    title = models.CharField(max_length=50)
    desc = models.TextField(blank=True)
    due_date = models.DateField(blank=True)
    priority = models.CharField(max_length=20, choices=PRIORITY, default="Important")

    def __str__(self):
        return f"{self.title}"


class Assignment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, default="")
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("submitted", "Submitted"),
    ]
    Assignment_id = models.AutoField(primary_key=True, auto_created=True)
    subject = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateField(blank=True)
    Assignment_files = models.FileField(
        upload_to="Uploaded_files/Assignment_pdfs/", blank=True
    )
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default="Pending")

    def __str__(self):
        return f"{self.title}"


class Note(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, default="")
    Note_id = models.AutoField(primary_key=True, auto_created=True)
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    category = models.CharField(max_length=50)
    date_added = models.DateTimeField(default=datetime.datetime.now())
    Assignment_files = models.FileField(upload_to="Uploaded_files/Notes/", blank=True)

    def __str__(self):
        return f"{self.title}"
