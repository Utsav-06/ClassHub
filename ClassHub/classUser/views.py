from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import JsonResponse
from collections import defaultdict
from django.template import loader
from .models import *


def temp(request):
    user = request.user

    if request.method == "POST":
        auth_logout(request)
        return redirect("welcome")

    user_info = get_object_or_404(UserProfile, user=request.user)
    recent_tasks = Task.objects.filter(user=user).order_by("-due_date")
    pending_assignments = Assignment.objects.filter(user=user, status="pending")
    recent_materials = Material.objects.filter(user=user).order_by("-date_added")
    upcoming_reminder = Reminder.objects.filter(
        user=user,
    ).order_by("R_date", "R_time")
    expenses = Expense.objects.filter(user=user).order_by("-date")

    total_tasks = Task.objects.filter(user=user).count()
    total_assignments = Assignment.objects.filter(user=user).count()
    total_materials = Material.objects.filter(user=user).count()
    total_reminders = Reminder.objects.filter(user=user).count()
    total_expenses = Expense.objects.filter(user=user).count()

    context = {
        "user": user,
        "user_info": user_info,
        "total_tasks": total_tasks,
        "total_assignments": total_assignments,
        "total_materials": total_materials,
        "total_reminders": total_reminders,
        "total_expenses": total_expenses,
        "recent_tasks": recent_tasks,
        "pending_assignments": pending_assignments,
        "recent_materials": recent_materials,
        "upcoming_reminder": upcoming_reminder,
        "expenses": expenses,
    }
    return render(request, "Temp.html", context)


# -----------------------------------------------------------------------------------------------------------#


def welcome(request):
    template = loader.get_template("User-Login-Logout/Welcome.html")
    return HttpResponse(template.render())


def main(request):
    user = request.user

    user_info = get_object_or_404(UserProfile, user=request.user)
    recent_tasks = Task.objects.filter(user=user).order_by("-due_date")
    pending_assignments = Assignment.objects.filter(user=user, status="pending")
    recent_materials = Material.objects.filter(user=user).order_by("-date_added")
    upcoming_reminder = Reminder.objects.filter(
        user=user,
    ).order_by("R_date", "R_time")
    expenses = Expense.objects.filter(user=user).order_by("-date")

    total_tasks = Task.objects.filter(user=user).count()
    total_assignments = Assignment.objects.filter(user=user).count()
    total_materials = Material.objects.filter(user=user).count()
    total_reminders = Reminder.objects.filter(user=user).count()
    total_expenses = Expense.objects.filter(user=user).count()

    context = {
        "user": user,
        "user_info": user_info,
        "total_tasks": total_tasks,
        "total_assignments": total_assignments,
        "total_materials": total_materials,
        "total_reminders": total_reminders,
        "total_expenses": total_expenses,
        "recent_tasks": recent_tasks,
        "pending_assignments": pending_assignments,
        "recent_materials": recent_materials,
        "upcoming_reminder": upcoming_reminder,
        "expenses": expenses,
    }

    return render(request, "User-Login-Logout/Main.html", context)


# -----------------------------------------------------------------------------------------------------------#
# User Login, Signup, Logout & Profile:
def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect("main")
        else:
            return render(
                request,
                "User-Login-Logout/Login.html",
                {"error": "Invalid login credentials"},
            )

    return render(request, "User-Login-Logout/Login.html")


def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        enrollment_no = request.POST["enrollmentNo"]
        password = request.POST["password"]

        user = User.objects.create_user(
            username=username, email=email, first_name=first_name, last_name=last_name
        )
        user.set_password(password)
        user_profile = UserProfile.objects.create(
            user=user,
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            Enrollment_No=enrollment_no,
        )

        user.save()
        user_profile.save()

        auth_login(request, user)

        return redirect("main")

    return render(request, "User-Login-Logout/Sign_up.html")


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
    if request.method == "POST":
        profile_info = get_object_or_404(UserProfile, user=request.user)
        task_info = Task.objects.get(user=request.user)
        assignment_info = Assignment.objects.get(user=request.user)
        material_info = Material.objects.get(user=request.user)
        reminder_info = Reminder.objects.get(user=request.user)
        expense_info = Expense.objects.get(user=request.user)

        profile_info.delete()
        task_info.delete()
        assignment_info.delete()
        material_info.delete()
        reminder_info.delete()
        expense_info.delete()


# -----------------------------------------------------------------------------------------------------------#
# Task Model


@login_required(login_url="/login")
def Add_Task(request):
    task_info = Task()
    task_info.user = request.user

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        priority = request.POST.get("priority")

        if title:
            task_info.title = title

        if description:
            task_info.description = description

        if priority:
            task_info.priority = True

        task_info.save()
        return redirect("list_task")

    return render(request, "Task/Add_task.html")


@login_required(login_url="/Login")
def List_Task(request):
    task_info = Task()
    task_info.user = request.user
    task_list = Task.objects.filter(user=request.user)

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        priority = request.POST.get("priority")

        if title:
            task_info.title = title

        if description:
            task_info.description = description

        if priority:
            task_info.priority = True

        task_info.save()

    return render(
        request,
        "Task/Task_list.html",
        context={"task_list": task_list},
    )


@login_required(login_url="/Login")
def Edit_Task(request, pk):
    task_info = Task.objects.get(Task_id=pk)

    if request.method == "POST":
        title = request.POST.get("title", "")
        description = request.POST.get("description", "")
        due_date = request.POST.get("due_date", "")
        priority = request.POST.get("priority", "")

        if title:
            task_info.title = title

        if description:
            task_info.description = description

        if due_date:
            task_info.due_date = due_date

        if priority:
            task_info.priority = priority

        task_info.save()
        return redirect("list_task")

    return render(request, "Task/Edit_Task.html", context={"task_info": task_info})


@login_required(login_url="/Login")
def Delete_Task(request, pk):
    task_info = Task.objects.get(Task_id=pk)

    if request.method == "POST":
        task_info.delete()
        return redirect("list_task")

    return render(request, "Task/delete_task.html", {"task": task_info})


# -----------------------------------------------------------------------------------------------------------#
# Assignment Model


@login_required(login_url="/Login")
def Add_Assignment(request):
    Assi_info = Assignment()
    Assi_info.user = request.user
    if request.method == "POST":
        subject = request.POST.get("subject", "")
        title = request.POST.get("title", "")
        description = request.POST.get("description", "")
        due_date = request.POST.get("due_date", "")
        Assignment_files = request.FILES.get("Assignment_files", None)
        status = request.POST.get("status", "")
        print(description)
        print(title)

        if subject:
            Assi_info.subject = subject

        if title:
            Assi_info.title = title

        if description:
            Assi_info.description = description

        if due_date:
            Assi_info.due_date = due_date

        if Assignment_files:
            Assi_info.Assignment_files = Assignment_files

        if status:
            Assi_info.status = status

        Assi_info.save()
        return redirect("list_assignment")

    return render(request, "Assignment/Add_assignment.html")


@login_required(login_url="/Login")
def List_Assignment(request):
    Assignments = Assignment.objects.all()

    return render(
        request,
        "Assignment/Assignment_list.html",
        context={"Assignments": Assignments},
    )


@login_required(login_url="/Login")
def Edit_Assignment(request, pk):
    Assi_info = Assignment.objects.get(Assignment_id=pk)

    if request.method == "POST":
        subject = request.POST.get("subject", "")
        title = request.POST.get("title", "")
        description = request.POST.get("description", "")
        due_date = request.POST.get("due_date", "")
        Assignment_files = request.FILES.get("Assignment_files", None)
        status = request.POST.get("status", "")
        print(description)
        print(title)

        if subject:
            Assi_info.subject = subject

        if title:
            Assi_info.title = title

        if description:
            Assi_info.description = description

        if due_date:
            Assi_info.due_date = due_date

        if Assignment_files:
            Assi_info.Assignment_files = Assignment_files

        if status:
            Assi_info.status = status

        Assi_info.save()
        return redirect("list_assignment")

    return render(
        request, "Assignment/Edit_Assignment.html", context={"Assi_info": Assi_info}
    )


@login_required(login_url="/Login")
def Delete_Assignment(request, pk):
    assignment_info = get_object_or_404(Assignment, Assignment_id=pk)
    if request.method == "POST":
        assignment_info.delete()
        return redirect("list_assignment")
    return render(
        request,
        "Assignment/Delete_Assignment.html",
        {"assignment_info": assignment_info},
    )


# -----------------------------------------------------------------------------------------------------------#
# Material Model


@login_required(login_url="/Login")
def Add_Material(request):
    material_info = Material(user=request.user)
    material_info.user = request.user
    if request.method == "POST":
        subject = request.POST.get("subject", "")
        title = request.POST.get("title", "")
        description = request.POST.get("description", "")
        Assignment_files = request.FILES.get("Assignment_files", None)

        if subject:
            material_info.subject = subject

        if title:
            material_info.title = title

        if description:
            material_info.description = description

        if "Assignment_files" in request.FILES:
            material_info.Assignment_files = Assignment_files

        material_info.save()
        return redirect("list_materials")

    return render(
        request, "Material/Add_Materials.html", {"material_info": material_info}
    )


@login_required(login_url="/Login")
def List_Material(request):
    material_info = Material.objects.filter(user=request.user)

    materials_by_subject = defaultdict(list)
    for material in material_info:
        materials_by_subject[material.subject].append(material)

    materials_by_subject = dict(materials_by_subject)

    return render(
        request,
        "Material/Material_List.html",
        context={"materials_by_subject": materials_by_subject},
    )


@login_required(login_url="/Login")
def Edit_Material(request, pk):
    material_info = Material.objects.get(Material_id=pk)

    if request.method == "POST":
        title = request.POST.get("title", "")
        description = request.POST.get("description", "")
        Assignment_files = request.FILES.get("Assignment_files", None)

        if title:
            material_info.title = title

        if description:
            material_info.description = description

        if Assignment_files:
            material_info.Assignment_files = Assignment_files

        material_info.save()
        return redirect("list_materials")

    return render(
        request, "Material/Edit_Material.html", context={"material_info": material_info}
    )


@login_required(login_url="/Login")
def Delete_Material(request, pk):
    material_info = get_object_or_404(Material, Material_id=pk)
    if request.method == "POST":
        material_info.delete()
        return redirect("list_materials")
    return render(
        request,
        "Material/Delete_Material.html",
        {"material_info": material_info},
    )


# -----------------------------------------------------------------------------------------------------------#
# Reminder Model


@login_required(login_url="/Login")
def Set_Reminder(request):
    Rem_info = Reminder()
    Rem_info.user = request.user
    if request.method == "POST":
        title = request.POST.get("title", "")
        description = request.POST.get("description", "")
        R_date = request.POST.get("R_date", "")
        R_time = request.POST.get("R_time", "")
        Location = request.POST.get("Location", "")

        if title:
            Rem_info.title = title

        if description:
            Rem_info.description = description

        if R_date:
            Rem_info.R_date = R_date

        if R_time:
            Rem_info.R_time = R_time

        if Location:
            Rem_info.Location = Location

        Rem_info.save()
        return redirect("list_reminder")

    return render(request, "Reminder/Set_Reminder.html")


@login_required(login_url="/Login")
def List_Reminder(request):
    reminders = Reminder.objects.all()
    return render(request, "Reminder/Reminder_List.html", {"reminders": reminders})


@login_required(login_url="/Login")
def Edit_Reminder(request, pk):
    Rem_info = Reminder.objects.get(Reminder_id=pk)

    if request.method == "POST":
        title = request.POST.get("title", "")
        description = request.POST.get("description", "")
        R_date = request.POST.get("R_date", "")
        R_time = request.POST.get("R_time", "")
        Location = request.POST.get("Location", "")

        if title:
            Rem_info.title = title

        if description:
            Rem_info.description = description

        if R_date:
            Rem_info.R_date = R_date

        if R_time:
            Rem_info.R_time = R_time

        if Location:
            Rem_info.Location = Location

        Rem_info.save()
        return redirect("list_reminder")

    return render(
        request, "Reminder/Edit_Reminder.html", context={"Rem_info": Rem_info}
    )


@login_required(login_url="/Login")
def Delete_Reminder(request, pk):
    Rem_info = get_object_or_404(Reminder, Reminder_id=pk)
    if request.method == "POST":
        Rem_info.delete()
        return redirect("list_reminder")
    return render(
        request,
        "Reminder/Delete_Reminder.html",
        {"Rem_info": Rem_info},
    )


# -----------------------------------------------------------------------------------------------------------#
# Expense Model


@login_required(login_url="/Login")
def Add_Expense(request):
    expense = Expense()
    expense.user = request.user

    if request.method == "POST":
        title = request.POST.get("title")
        amount = request.POST.get("amount")
        Location = request.POST.get("Location")

        if title:
            expense.title = title

        if amount:
            expense.amount = amount

        if Location:
            expense.Location = Location

        expense.save()
        return redirect("list_expense")

    return render(request, "Expense/Add_Expense.html")


@login_required(login_url="/Login")
def List_Expense(request):
    expense_list = Expense.objects.filter(user=request.user)

    total = sum(expense.amount for expense in expense_list)
    return render(
        request,
        "Expense/Expense_List.html",
        {"expense_list": expense_list, "total": total},
    )


@login_required(login_url="/Login")
def Delete_Expense(request, pk):
    expense = get_object_or_404(Expense, Expense_id=pk, user=request.user)

    if request.method == "POST":
        expense.delete()
        return redirect("list_expense")

    return render(request, "Expense/Delete_Expense.html", {"expense": expense})
