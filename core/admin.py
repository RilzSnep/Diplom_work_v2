from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Course, Material, Test, TestResult

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'role', 'is_active']
    list_filter = ['role']
    search_fields = ['username']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(Course)
admin.site.register(Material)
admin.site.register(Test)
admin.site.register(TestResult)