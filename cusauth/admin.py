from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, ProfileUpdate, Company, Role, UserRole

class UserAdmin(BaseUserAdmin):
    list_display = ["id", "email", "name", "company", "tc", "is_admin"]
    list_filter = ["is_admin", "company"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["name", "tc", "company"]}),
        ("Permissions", {"fields": ["is_admin", "groups", "user_permissions","is_company_admin",]}),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "name", "tc", "company", "password1", "password2", "groups", "user_permissions"],
            },
        ),
    ]
    search_fields = ["email", "name", "company__name"]
    ordering = ["email", "id"]
    filter_horizontal = ["groups", "user_permissions"]

admin.site.register(User, UserAdmin)

@admin.register(ProfileUpdate)
class AdminProfileUpdate(admin.ModelAdmin):
    list_display = ['user', 'Date_of_Birth', 'profile_picture', 'pan_number', 'pan_picture']

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'company_code', 'created_at', 'updated_at']
    search_fields = ['name', 'company_code']
    ordering = ['name', 'created_at']

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'company']
    search_fields = ['name', 'company__name']
    ordering = ['name', 'company__name']

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'can_authenticate']
    search_fields = ['user__email', 'role__name', 'user__company__name']
    ordering = ['user__email', 'role__name']
