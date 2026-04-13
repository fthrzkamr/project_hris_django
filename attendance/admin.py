from django.contrib import admin
from .models import Attendance, AttendanceRule

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'clock_in', 'clock_out', 'status', 'late_minutes_display', 'is_late_excused')
    list_filter = ('date', 'status', 'is_late_excused', 'employee__department')
    search_fields = ('employee__full_name', 'employee__employee_id')
    ordering = ('-date', 'employee')
    
    fieldsets = (
        ('Info Utama', {
            'fields': ('employee', 'date', 'status')
        }),
        ('Waktu Absen', {
            'fields': ('clock_in', 'clock_out')
        }),
        ('Dispensasi Keterlambatan', {
            'fields': ('late_reason', 'late_evidence', 'is_late_excused', 'excused_by'),
            'description': 'Gunakan bagian ini jika karyawan telat dan memiliki alasan yang sah.'
        }),
        ('Catatan Lain', {
            'fields': ('note',)
        }),
    )

    def late_minutes_display(self, obj):
        return f"{obj.late_minutes} Menit" if obj.late_minutes > 0 else "-"
    late_minutes_display.short_description = "Keterlambatan"

@admin.register(AttendanceRule)
class AttendanceRuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_time', 'end_time', 'grace_period', 'allowed_radius', 'office_latitude', 'office_longitude')
    fieldsets = (
        ('Pengaturan Waktu Dasar', {
            'fields': ('name', 'start_time', 'end_time', 'grace_period')
        }),
        ('Pengaturan Jarak & Lokasi (GPS)', {
            'fields': ('office_latitude', 'office_longitude', 'allowed_radius'),
            'description': 'Koordinat titik tengah kantor dan seberapa jauh (dalam meter) karyawan diizinkan absen masuk/pulang.'
        }),
    )
