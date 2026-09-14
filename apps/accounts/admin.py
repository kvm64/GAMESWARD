from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Role, RoleGroup, UserStatus


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительно', {'fields': ('patronymic', 'phone', 'avatar', 'bio', 'birth_date')}),
    )


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'context', 'is_system')
    list_filter = ('context', 'is_system')
    search_fields = ('name', 'code')
    ordering = ('context', 'name')


@admin.register(RoleGroup)
class RoleGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    filter_horizontal = ('roles',)


@admin.register(UserStatus)
class UserStatusAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'assigned_at', 'expires_at', 'is_active')
    list_filter = ('is_active', 'role')
    search_fields = ('user__username', 'role__name')
    ordering = ('-assigned_at',)