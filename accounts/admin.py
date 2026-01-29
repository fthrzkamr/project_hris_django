from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'username',
        'get_npp',
        'get_full_name',
        'get_role',
        'is_active',
        'is_staff'
    )

    readonly_fields = ('get_npp', 'get_full_name', 'get_role')

    fieldsets = (
        ('Info Employee', {
            'fields': ('get_npp', 'get_full_name', 'get_role'),
            'description': 'Informasi dari data Employee'
        }),
    ) + UserAdmin.fieldsets

    def get_npp(self, obj):
        return obj.employee.npp if hasattr(obj, 'employee') else '-'
    get_npp.short_description = 'NPP'

    def get_full_name(self, obj):
        return obj.employee.full_name if hasattr(obj, 'employee') else '-'
    get_full_name.short_description = 'Nama'

    def get_role(self, obj):
        if hasattr(obj, 'employee') and obj.employee.role:
            return obj.employee.role.name
        return '-'
    get_role.short_description = 'Jabatan / Role'
