from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from companies.models import Company
from departments.models import Department
from positions.models import Position
from branches.models import Branch

User = settings.AUTH_USER_MODEL

class Employee(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    # Identitas dasar
    npp = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    # Struktur organisasi
    company = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    branch = models.ForeignKey(
        Branch,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # Status kerja
    join_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.user:
            User = get_user_model()
            user = User.objects.create_user(
                username=self.npp,
                password=self.npp  # password awal
            )
            self.user = user

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.npp} - {self.full_name}"
