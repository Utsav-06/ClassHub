from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from .views import *

urlpatterns = [
    path("", welcome, name="welcome"),
    path("Login/", login, name="login"),
    path("Sign_up/", signup, name="signup"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("Main/", main, name="main"),
    path("Dashboard/", dashboard, name="dashboard"),
    path("Add_Task/", add_task, name="add_task"),
    path("Task_List/", list_task, name="list_task"),
    path("Task/<int:pk>", Tasks_detail, name="TaskDetail"),
    path("Edit_Task/<int:pk>", edit_task, name="edit_task"),
    path("Profile/", User_Profile, name="userprofile"),
    path("Edit_Profile/", Edit_Profile, name="editprofile"),
    path("Task_delete/<int:pk>/", delete_task, name="delete_task"),
    path("Add_Assignment/", Add_assignment, name="Add_Assignment"),
    path("Assignment_list/", list_assignment, name="Assignment_list"),
    path("edit/<int:pk>/", edit_assignment, name="edit_assignment"),
    # path("delete/<int:assignment_id>/", delete_assignment, name="delete_assignment"),
    # path("Add_Note/", add_note, name="add_note"),
    # path("Note_List/", note_list, name="list_notes"),
    # path("<int:year>/<str:month>", event, name="event"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Path Converters:
#   - int: numbers
#   -  str: strings
#   - path: whole urls /
#   - slud: hyphens-underscore-stuff
#   - UUID: Universally Unique Identifier
