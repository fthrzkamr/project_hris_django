from django.db import models
from employees.models import Employee

class LeaveType(models.Model):
    name = models.CharField(max_length=100)
    is_deduct_annual = models.BooleanField(default=True, help_text="Apakah memotong sisa jatah cuti reguler?")
    requires_attachment = models.BooleanField(default=False, help_text="Apakah butuh surat keterangan/bukti?")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class LeaveBalance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leave_balances')
    year = models.IntegerField()
    total_balance = models.IntegerField(default=12, help_text="Total jatah cuti (hari)")
    used_balance = models.IntegerField(default=0, help_text="Jumlah terpakai (hari)")

    class Meta:
        unique_together = ('employee', 'year')

    @property
    def remaining_balance(self):
        return self.total_balance - self.used_balance

    def __str__(self):
        return f"{self.employee.full_name} ({self.year}) - Sisa: {self.remaining_balance}"

class LeaveRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Menunggu Approval'),
        ('approved', 'Disetujui'),
        ('rejected', 'Ditolak'),
        ('cancelled', 'Dibatalkan'),
    )
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leave_requests')
    leave_type = models.ForeignKey(LeaveType, on_delete=models.PROTECT)
    start_date = models.DateField()
    end_date = models.DateField()
    duration_days = models.IntegerField(default=1)
    reason = models.TextField()
    attachment = models.FileField(upload_to='leaves/attachments/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    approved_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_leaves')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.employee.full_name} | {self.leave_type.name} ({self.status})"

