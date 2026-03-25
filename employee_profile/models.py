from django.db import models
from employees.models import Employee

class EmployeeProfile(models.Model):
    employee = models.OneToOneField(
        Employee,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    phone_number = models.CharField(max_length=20, blank=True)
    email_personal = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=10,
        choices=[
            ('L', 'Laki-laki'),
            ('P', 'Perempuan'),
        ],
        blank=True
    )
    photo = models.ImageField(upload_to='profile/', blank=True, null=True)

    def __str__(self):
        return f"Profile - {self.employee.full_name}"
