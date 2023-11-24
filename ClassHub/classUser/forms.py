from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import *
from django import forms
from .models import *


# Creating a Task Form
class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = [
            "title",
            "desc",
            "due_date",
            "priority",
        ]


class CustomLoginForm(AuthenticationForm):
    enrollment_number = forms.CharField(
        label="Enrollment Number",
        widget=forms.TextInput(attrs={"autofocus": True}),
    )


# class CustomUserCreationForm(UserCreationForm):
#     class Meta:
#         model = CustomUser
#         fields = [
#             "enrollment_number",
#             "username",
#             "email",
#             "password1",
#         ]



# class AssignmentForm(forms.ModelForm):
#     class Meta:
#         model = Assignment
#         fields = [
#             "subject",
#             "title",
#             "description",
#             "due_date",
#             "status",
#         ]


# class NoteForm(forms.ModelForm):
#     class Meta:
#         model = Note
#         fields = [
#             "Note_id",
#             "title",
#             "content",
#             "category",
#         ]


# class ReminderForm(forms.ModelForm):
#     class Meta:
#         model = Reminder
#         fields = [
#             "Reminder_id",
#             "title",
#             "description",
#             "date",
#             "time",
#         ]


# from django import forms
# from .models import Reminder


# class ReminderForm(forms.ModelForm):
#     class Meta:
#         model = Reminder
#         fields = [
#             "Reminder_id",
#             "title",
#             "description",
#             "Rem_date",
#             "Rem_time",
#         ]
