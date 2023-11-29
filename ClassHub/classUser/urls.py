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
    # Task
    path("Add_Task/", add_task, name="add_task"),
    path("Task_List/", list_task, name="list_task"),
    path("Task/<int:pk>", Tasks_detail, name="TaskDetail"),
    path("Edit_Task/<int:pk>", edit_task, name="edit_task"),
    path("Task_delete/<int:pk>/", delete_task, name="delete_task"),
    # ---------------------------------------------------------------------
    # Profile
    path("Profile/", User_Profile, name="userprofile"),
    path("Edit_Profile/", Edit_Profile, name="editprofile"),
    # ---------------------------------------------------------------------
    # Assignment
    path("Add_Assignment/", Add_assignment, name="Add_Assignment"),
    path("Assignment_list/", list_assignment, name="Assignment_list"),
    path("Edit_Assignment/<int:pk>", edit_assignment, name="edit_assignment"),
    path("Assignment_delete/<int:pk>/", delete_assignment, name="delete_assignment"),
    # ---------------------------------------------------------------------
    # Note
    path("Add_Note/", add_note, name="add_note"),
    path("Note_List/", note_list, name="list_notes"),
    path("Edit_Note/<int:pk>", edit_Note, name="edit_Note"),
    path("Note_delete/<int:pk>/", delete_Note, name="delete_Note"),
    # ---------------------------------------------------------------------
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Path Converters:
#   - int: numbers
#   -  str: strings
#   - path: whole urls /
#   - slud: hyphens-underscore-stuff
#   - UUID: Universally Unique Identifier
