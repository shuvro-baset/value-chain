from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(UniUser)
class UniUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'user_type']

