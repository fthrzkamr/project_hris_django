from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    ROLE_CHOICES = (
        ('SUPERADMIN', 'Super Admin'),
        ('HR', 'HR'),
        ('EMPLOYEE', 'Employee'),
    )

    npp = models.CharField(
        max_length=20,
        unique=True,
        help_text="Nomor Pokok Pegawai"
    )

    role = models.CharField(
        max_length=15,
        choices=ROLE_CHOICES,
        default='EMPLOYEE'
    )

    is_active_employee = models.BooleanField(
        default=True,
        help_text="Masih bekerja atau tidak"
    )

    def __str__(self):
        return f"{self.username} ({self.npp})"
