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
        'role',
        'is_active',
    )

    list_filter = (
        'company',
        'department',
        'position',
        'role',
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
        'role',
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
                'role',
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
            'description': 'Isi hanya jika employee membutuhkan akses login'
        }),
    )
