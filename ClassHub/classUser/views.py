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


# def dashboard(request):
#     profile_info = get_object_or_404(UserProfile, user=request.user)

#     return render(
#         request, "Dashboard.html", context={"profile_pic": profile_info.profile_pic}
#     )


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
    profile_info = get_object_or_404(UserProfile, user=request.user)

    if request.method == "POST":
        auth_logout(request)
        return redirect("welcome")

    return render(
        request,
        "User-Login-Logout/Main.html",
        context={"profile_pic": profile_info.profile_pic},
    )


@login_required(login_url="/Login")
def Edit_Profile(request):
    profile_info = get_object_or_404(UserProfile, user=request.user)

    if request.method == "POST":
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        Enrollment_No = request.POST.get("Enrollment_No")
        bio = request.POST.get("bio")
        profile_pic = request.FILES.get("profile_pic")
        birth_date = request.POST.get("birth_date")

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
    return render(
        request, "Userprofile/Profile.html", context={"profile_info": profile_info}
    )


@login_required(login_url="/Login")
def Delete_Profile(request):
    profile_info = get_object_or_404(UserProfile, user=request.user)
    task_info = Task.objects.get(user=request.user)
    assignment_info = Assignment.objects.get(user=request.user)
    note_info = Note.objects.get(user=request.user)
    reminder_info = Reminder.objects.get(user=request.user)
    expense_info = Expense.objects.get(user=request.user)

    profile_info.delete()


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
            task_info.title = title

        if desc:
            task_info.desc = desc

        if due_date:
            task_info.due_date = due_date

        if priority:
            task_info.priority = priority

        task_info.save()
        return redirect("list_task")

    return render(request, "Task/Edit_Task.html", context={"task_info": task_info})


@login_required(login_url="/Login")
def delete_task(request, pk):
    task_info = Task.objects.get(Task_id=pk)

    if request.method == "POST":
        task_info.delete()
        return redirect("list_task")

    return render(request, "Task/delete_task.html", {"task": task_info})


# -----------------------------------------------------------------------------------------------------------#
# Assignment Model


@login_required(login_url="/Login")
def Add_assignment(request):
    assignment = Assignment()
    assignment.user = request.user
    if request.method == "POST":
        subject = request.POST.get("subject")
        title = request.POST.get("title")
        desc = request.POST.get("desc")
        due_date = request.POST.get("due_date")
        Assignment_files = request.FILES["Assignment_files"]
        status = request.POST.get("status")

        assignment.subject = subject
        assignment.title = title

        if desc:
            assignment.desc = desc

        if due_date:
            assignment.due_date = due_date

        if "Assignment_files" in request.FILES:
            assignment.Assignment_files = Assignment_files

        if status:
            assignment.status = status

        assignment.save()

    return render(request, "Assignment/Add_assignment.html")


@login_required(login_url="/Login")
def list_assignment(request):
    Assignments = Assignment.objects.all()

    return render(
        request,
        "Assignment/Assignment_list.html",
        context={"Assignments": Assignments},
    )


@login_required(login_url="/Login")
def edit_assignment(request, pk):
    Assi_info = Assignment.objects.get(Assignment_id=pk)

    if request.method == "POST":
        subject = request.POST.get("subject")
        title = request.POST.get("title")
        desc = request.POST.get("desc")
        due_date = request.POST.get("due_date")
        Assignment_files = request.FILES["Assignment_files"]
        status = request.POST.get("status")

        if subject:
            Assi_info.subject = subject

        if title:
            Assi_info.title = title

        if desc:
            Assi_info.desc = desc

        if due_date:
            Assi_info.due_date = due_date

        if Assignment_files:
            Assi_info.Assignment_files = Assignment_files

        if status:
            Assi_info.status = status

        Assi_info.save()
        return redirect("Assignment_list")

    return render(
        request, "Assignment/Edit_Assignment.html", context={"Assi_info": Assi_info}
    )


@login_required(login_url="/Login")
def delete_assignment(request, pk):
    assignment_info = get_object_or_404(Assignment, Assignment_id=pk)
    if request.method == "POST":
        assignment_info.delete()
        return redirect("Assignment_list")
    return render(
        request,
        "Assignment/Delete_Assignment.html",
        {"assignment_info": assignment_info},
    )


# -----------------------------------------------------------------------------------------------------------#
# Note Model


@login_required(login_url="/Login")
def add_note(request):
    note_info = Note()
    note_info.user = request.user
    if request.method == "POST":
        subject = request.POST.get("subject")
        title = request.POST.get("title")
        desc = request.POST.get("desc")
        due_date = request.POST.get("due_date")
        Assignment_files = request.FILES["Assignment_files"]
        status = request.POST.get("status")

        assignment.subject = subject
        assignment.title = title

        if desc:
            assignment.desc = desc

        if due_date:
            assignment.due_date = due_date

        if "Assignment_files" in request.FILES:
            assignment.Assignment_files = Assignment_files

        if status:
            assignment.status = status

        assignment.save()

    return render(request, "Assignment/Add_assignment.html")

    return render(request, "Note/Add_Notes.html", {"form": form})


@login_required(login_url="/Login")
def note_list(request):
    Notes = Note.objects.all()
    return render(request, "Note/Notes_List.html", context={"Notes": Notes})


@login_required(login_url="/Login")
def edit_assignment(request, pk):
    Assi_info = Assignment.objects.get(Assignment_id=pk)

    if request.method == "POST":
        subject = request.POST.get("subject")
        title = request.POST.get("title")
        desc = request.POST.get("desc")
        due_date = request.POST.get("due_date")
        Assignment_files = request.FILES["Assignment_files"]
        status = request.POST.get("status")

        if subject:
            Assi_info.subject = subject

        if title:
            Assi_info.title = title

        if desc:
            Assi_info.desc = desc

        if due_date:
            Assi_info.due_date = due_date

        if Assignment_files:
            Assi_info.Assignment_files = Assignment_files

        if status:
            Assi_info.status = status

        Assi_info.save()
        return redirect("Assignment_list")

    return render(
        request, "Assignment/Edit_Assignment.html", context={"Assi_info": Assi_info}
    )


@login_required(login_url="/Login")
def delete_assignment(request, pk):
    assignment_info = get_object_or_404(Assignment, Assignment_id=pk)
    if request.method == "POST":
        assignment_info.delete()
        return redirect("Assignment_list")
    return render(
        request,
        "Assignment/Delete_Assignment.html",
        {"assignment_info": assignment_info},
    )


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
