from django.contrib import admin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'npp',
        'full_name',
        'company',
        'department',
        'position',
        'branch',
        'is_active',
    )

    list_filter = (
        'company',
        'department',
        'position',
        'branch',
        'is_active',
    )

    search_fields = (
        'npp',
        'full_name',
        'email',
    )

    autocomplete_fields = (
        'user',
        'company',
        'department',
        'position',
        'branch',
    )

    fieldsets = (
        ('Identitas Dasar', {
            'fields': (
                'npp',
                'full_name',
                'email',
                'phone',
            )
        }),
        ('Struktur Organisasi', {
            'fields': (
                'company',
                'department',
                'position',
                'branch',
            )
        }),
        ('Status Kerja', {
            'fields': (
                'join_date',
                'is_active',
            )
        }),
        ('Akun Login (Opsional)', {
            'fields': ('user',),
            'description': 'Link dengan User untuk akses login'
        }),
    )
