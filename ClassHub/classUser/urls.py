from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from .views import *

urlpatterns = [
    path("temp/", temp, name="temp"),
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
    path("Edit_Task/<int:pk>", Edit_Task, name="edit_task"),
    path("Delete_Task/<int:pk>/", Delete_Task, name="delete_task"),
    # ---------------------------------------------------------------------
    # Assignment
    path("Add_Assignment/", Add_Assignment, name="add_assignment"),
    path("List_Assignments/", List_Assignment, name="list_assignment"),
    path("Edit_Assignment/<int:pk>", Edit_Assignment, name="edit_assignment"),
    path("Delete_Assignment/<int:pk>/", Delete_Assignment, name="delete_assignment"),
    # ---------------------------------------------------------------------
    # Material
    path("Add_Material/", Add_Material, name="add_material"),
    path("List_Materials/", List_Material, name="list_materials"),
    path("Edit_Material/<int:pk>", Edit_Material, name="edit_material"),
    path("Delete_Material/<int:pk>/", Delete_Material, name="delete_material"),
    # ---------------------------------------------------------------------
    # Reminder
    path("Set_Reminder/", Set_Reminder, name="set_reminder"),
    path("List_Reminder/", List_Reminder, name="list_reminder"),
    path("Edit_Reminder/<int:pk>", Edit_Reminder, name="edit_reminder"),
    path("Delete_Reminder/<int:pk>/", Delete_Reminder, name="delete_reminder"),
    # ---------------------------------------------------------------------
    # Expense
    path("Add_Expense", Add_Expense, name="add_expense"),
    path("List_Expense/", List_Expense, name="list_expense"),
    path("Delete_Expense/<int:pk>", Delete_Expense, name="delete_expense"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Path Converters:
#   - int: numbers
#   - str: strings
#   - path: whole urls /
#   - slud: hyphens-underscore-stuff
#   - UUID: Universally Unique Identifier
