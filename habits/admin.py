from django.contrib import admin
from .models import Habit, Progress, Badge, UserProfile
# Register your models here.
admin.site.register(Habit)
admin.site.register(Progress)
admin.site.register(Badge)
admin.site.register(UserProfile)
