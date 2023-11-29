from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from .views import *

urlpatterns = [
    # ---------------------------------------------------------------------
    # User Authentication and welcome page
    path("", welcome, name="welcome"),
    path("Login/", login, name="login"),
    path("Sign_up/", signup, name="signup"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("Main/", main, name="main"),
    # path("Dashboard/", dashboard, name="dashboard"),
    # ---------------------------------------------------------------------
    # Profile
    path("Profile/", User_Profile, name="userprofile"),
    path("Edit_Profile/", Edit_Profile, name="editprofile"),
    # ---------------------------------------------------------------------
    # Task
    path("Add_Task/", Add_Task, name="add_task"),
    path("List_Tasks/", List_Task, name="list_task"),
    path("Task/<int:pk>", Tasks_Detail, name="task_detail"),
    path("Edit_Task/<int:pk>", Edit_Task, name="edit_task"),
    path("Delete_Task/<int:pk>/", Delete_Task, name="delete_task"),
    # ---------------------------------------------------------------------
    # Assignment
    path("Add_Assignment/", Add_Assignment, name="add_assignment"),
    path("List_Assignments/", List_Assignment, name="list_assignment"),
    path("Edit_Assignment/<int:pk>", Edit_Assignment, name="edit_assignment"),
    path("Delete_Assignment/<int:pk>/", Delete_Assignment, name="delete_assignment"),
    # ---------------------------------------------------------------------
    # Note
    path("Add_Note/", Add_Note, name="add_note"),
    path("List_Notes/", List_Note, name="list_notes"),
    path("Edit_Note/<int:pk>", Edit_Note, name="edit_note"),
    path("Delete_Note/<int:pk>/", Delete_Note, name="delete_note"),
    # ---------------------------------------------------------------------
    # Reminder
    # path("Set_Reminder/", add_note, name="add_note"),
    # path("List_Reminder/", note_list, name="list_notes"),
    # path("Edit_Reminder/<int:pk>", edit_Note, name="edit_Note"),
    # path("Delete_Reminder/<int:pk>/", delete_Note, name="delete_Note"),
    # ---------------------------------------------------------------------
    # Expense
    path("Add_Expense", Add_Expense, name="add_expense"),
    path("List_Expense/", List_Expense, name="list_expense"),
    path("Delete_Expense/<int:pk>", Delete_Expense, name="delete_expense"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Path Converters:
#   - int: numbers
#   -  str: strings
#   - path: whole urls /
#   - slud: hyphens-underscore-stuff
#   - UUID: Universally Unique Identifier
