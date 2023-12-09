from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Task)
admin.site.register(UserProfile)
admin.site.register(Assignment)
admin.site.register(Material)
admin.site.register(Expense)
admin.site.register(Reminder)
