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
        ('Identitas Pribadi', {
            'fields': (
                'user', 'photo', 'npp', 'nik', 'full_name', 'nickname',
                'gender', 'birth_place', 'birth_date', 'religion',
                'marital_status', 'blood_type', 'nationality',
                'email', 'phone'
            )
        }),
        ('Alamat', {
            'fields': (
                'address', 'rt_rw', 'kelurahan', 'kecamatan',
                'kota', 'provinsi', 'kode_pos'
            )
        }),
        ('Keluarga & Darurat', {
            'fields': (
                'father_name', 'mother_name',
                'emergency_name', 'emergency_phone', 'emergency_relation'
            )
        }),
        ('Pendidikan', {
            'fields': (
                'last_education', 'education_major',
                'education_school', 'graduation_year'
            )
        }),
        ('Dokumen & Bank', {
            'fields': (
                'npwp', 'bpjs_ketenagakerjaan', 'bpjs_kesehatan', 'bpjs_kesehatan_type',
                'bank_name', 'bank_account_no', 'bank_account_name'
            )
        }),
        ('Data Kepegawaian', {
            'fields': (
                'company', 'department', 'position', 'branch',
                'employment_type', 'join_date', 'contract_start', 'contract_end',
                'is_active'
            )
        }),
    )
