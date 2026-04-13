from django.db import models
from employees.models import Employee

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Hadir'),
        ('late', 'Terlambat'),
        ('absent', 'Alpa'),
        ('off', 'Libur'),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    clock_in = models.TimeField(null=True, blank=True)
    clock_out = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='present')
    note = models.TextField(null=True, blank=True)
    
    # Flow Dispensasi Keterlambatan
    late_reason = models.TextField(null=True, blank=True, help_text="Alasan terlambat")
    late_evidence = models.ImageField(upload_to='attendance/evidence/', null=True, blank=True, help_text="Bukti foto/dokumen")
    is_late_excused = models.BooleanField(default=False, help_text="Centang jika alasan telat diterima oleh atasan")
    excused_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='excused_attendances')

    class Meta:
        unique_together = ('employee', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.employee.full_name} - {self.date}"

    @property
    def late_minutes(self):
        if self.clock_in and self.status == 'late':
            rule = AttendanceRule.objects.first()
            if rule:
                import datetime
                # combine with a dummy date to subtract
                dummy_date = datetime.date.today()
                dt_in = datetime.datetime.combine(dummy_date, self.clock_in)
                dt_rule = datetime.datetime.combine(dummy_date, rule.start_time)
                diff = (dt_in - dt_rule).total_seconds() / 60
                if diff > 0:
                    return int(diff)
        return 0

class AttendanceRule(models.Model):
    """Pengaturan Jam Kerja Global"""
    name = models.CharField(max_length=50, default="Jam Kerja Reguler")
    start_time = models.TimeField(default="08:00:00")
    end_time = models.TimeField(default="17:00:00")
    grace_period = models.IntegerField(default=15, help_text="Toleransi keterlambatan (menit)")
    
    # Pengaturan Lokasi / GPS
    office_latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True, help_text="Garis Lintang (Latitude) Kantor Induk")
    office_longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True, help_text="Garis Bujur (Longitude) Kantor Induk")
    allowed_radius = models.IntegerField(default=100, help_text="Maksimal jarak absen dari kantor (dalam meter)")

    def __str__(self):
        return self.name
