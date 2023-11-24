from importlib.abc import Loader
from urllib import request
from django.http import HttpResponse
from django import template
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import *


# @receiver(post_delete, sender=Assignment)
# def delete_assignment_files(sender, instance, **kwargs):
#     # Delete the associated file when the assignment is deleted
#     if instance.Assignment_files:
#         instance.Assignment_files.delete(save=False)
