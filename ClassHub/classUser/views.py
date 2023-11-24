from pyexpat.errors import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template import loader
from django.conf import settings
from .models import *
from .forms import *
import os


def dashboard(request):
    template = loader.get_template("Dashboard.html")
    return HttpResponse(template.render())


def welcome(request):
    template = loader.get_template("User-Login-Logout/Welcome.html")
    return HttpResponse(template.render())


# def event(request, year, month):
#     name = "Utsav"

#     # Converting month from name to number
#     month = month.title()
#     month_number = list(calendar.month_name).index(month)
#     month_number = int(month_number)

#     # Calender
#     cal = HTMLCalendar().formatmonth(year, month_number)
#     now = datetime.now()
#     current_year = now.year
#     current_time = now.strftime("%I:%M %p")
#     return render(
#         request,
#         "Event.html",
#         {
#             "name": name,
#             "year": year,
#             "month": month,
#             "month_number": month_number,
#             "cal": cal,
#             "current_year": current_year,
#             "current_time": current_time,
#         },
#     )


# -----------------------------------------------------------------------------------------------------------#
# User Login, Signup, Logout & Profile:
def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        # Authenticate user using either username or email
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect("main")
        else:
            return render(
                request,
                "User-Login-Logout/Login.html",
                {"error": "Invalid credentials"},
            )

    return render(request, "User-Login-Logout/Login.html")


def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        enrollment_no = request.POST["enroll"]
        password = request.POST["password"]

        user = User.objects.create_user(username=username, email=email)
        user.set_password(password)
        user_profile = UserProfile.objects.create(
            user=user, username=username, Enrollment_No=enrollment_no
        )

        user.save()
        user_profile.save()

        auth_login(request, user)

        return redirect("main")

    return render(request, "User-Login-Logout/Sign_up.html")


def main(request):
    if request.method == "POST":
        auth_logout(request)
        return redirect("welcome")

    template = loader.get_template("User-Login-Logout/Main.html")
    return HttpResponse(template.render())


@login_required(login_url="/Login")
def Edit_Profile(request):
    profile_info = get_object_or_404(UserProfile, user=request.user)

    if request.method == "POST":
        username = request.POST.get("username")  # User model
        first_name = request.POST.get("first_name")  # UserProfile model
        last_name = request.POST.get("last_name")  # UserProfile model
        Enrollment_No = request.POST.get("Enrollment_No")  # UserProfile model
        bio = request.POST.get("bio")  # UserProfile model
        profile_pic = request.FILES.get("profile_pic")  # UserProfile model
        birth_date = request.POST.get("birth_date")  # UserProfile model

        if username and username != request.user.username:
            request.user.username = username
            profile_info.username = username
            profile_info.save()
            request.user.save()

        if first_name:
            profile_info.first_name = first_name

        if last_name:
            profile_info.last_name = last_name

        if Enrollment_No:
            profile_info.Enrollment_No = Enrollment_No

        if bio:
            profile_info.bio = bio

        if profile_pic:
            profile_info.profile_pic = profile_pic

        if birth_date:
            profile_info.birth_date = birth_date

        profile_info.save()
        return redirect("userprofile")

    return render(
        request, "Userprofile/Edit_Profile.html", context={"profile_info": profile_info}
    )


@login_required(login_url="/Login")
def User_Profile(request):
    profile_info = get_object_or_404(UserProfile, user=request.user)
    print(profile_info.profile_pic)
    return render(
        request, "Userprofile/Profile.html", context={"profile_info": profile_info}
    )


# -----------------------------------------------------------------------------------------------------------#
# Task Model


@login_required(login_url="/login")
def add_task(request):
    if request.method == "POST":
        title = request.POST.get("title")
        desc = request.POST.get("desc")
        due_date = request.POST.get("due_date")
        priority = request.POST.get("priority")

        task = Task(
            title=title,
            desc=desc,
            due_date=due_date,
            priority=priority,
            user=request.user,
        )
        task.save()
    return render(request, "Task/Add_task.html")


@login_required(login_url="/Login")
def list_task(request):
    task_list = Task.objects.filter(user=request.user)
    return render(request, "Task/Task_list.html", context={"task_list": task_list})


@login_required(login_url="/Login")
def Tasks_detail(request, pk):
    task_list = Task.objects.get(Task_id=pk)
    return render(request, "Task/Task.html", {"task_list": task_list})


@login_required(login_url="/Login")
def edit_task(request, pk):
    task_info = Task.objects.get(Task_id=pk)

    if request.method == "POST":
        title = request.POST.get("title")
        desc = request.POST.get("desc")
        due_date = request.POST.get("due_date")
        priority = request.POST.get("priority")

        if title:
            print(title)
            task_info.title = title

        if desc:
            print(desc)
            task_info.desc = desc

        if due_date:
            print(due_date)
            task_info.due_date = due_date

        if priority:
            print(priority)
            task_info.priority = priority

        task_info.save()
        print(Task)
        return redirect("list_task")

    return render(request, "Task/Edit_Task.html", context={"task_info": task_info})


@login_required(login_url="/Login")
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == "POST":
        task.delete()
        return redirect("list_task")

    return render(request, "Task/delete_task.html", {"task": task})


# -----------------------------------------------------------------------------------------------------------#
# Assignment Model

# @login_required(login_url='/Login')
# def add_assignment(request):
#     submitted = False
#     if request.method == "POST":
#         form = AssignmentForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect("/Assignment")
#     else:
#         form = AssignmentForm()
#         if "submitted" in request.GET:
#             submitted = True

#     return render(request, "Assignment.html", {"form": form})

# @login_required(login_url='/Login')
# def list_assignment(request):
#     Assignments = Assignment.objects.all()
#     return render(request, "Assignment_list.html", context={"Assignments": Assignments})


# def update_assignment(request, assignment_id):
#     assignment = get_object_or_404(Assignment, id=assignment_id)
#     if request.method == "POST":
#         form = AssignmentForm(request.POST, instance=assignment)
#         if form.is_valid():
#             form.save()
#             return redirect("assignment_list")
#     else:
#         form = AssignmentForm(instance=assignment)
#     return render(request, "update_assignment.html", {"form": form})


# def delete_assignment(request, assignment_id):
#     assignment = get_object_or_404(Assignment, id=assignment_id)
#     assignment.delete()
#     return redirect("assignment_list")


# -----------------------------------------------------------------------------------------------------------#
# Note Model

# def add_note(request):
#     submitted = False
#     if request.method == "POST":
#         form = NoteForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect("/Add_Note")
#     else:
#         form = NoteForm()
#         if "submitted" in request.GET:
#             submitted = True

#     return render(request, "Note/Add_Notes.html", {"form": form})


# def note_list(request):
#     Notes = Note.objects.all()
#     return render(request, "Note/Notes_List.html", context={"Notes": Notes})


# -----------------------------------------------------------------------------------------------------------#
# Reminder Model

# def set_reminder(request):
#     if request.method == "POST":
#         # Get the user input (date and time)
#         date_str = request.POST.get("date")
#         time_str = request.POST.get("time")

#         Reminder_datetime = Reminder.objects.create(
#             Rem_date=date_str,
#             Rem_time=time_str,
#         )

#         # Success Response
#         return JsonResponse({"status": "success"})

#     return render(request, "Reminder/Set_Reminder.html")
