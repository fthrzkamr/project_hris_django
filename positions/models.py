from django.db import models
from departments.models import Department


class Position(models.Model):
    LEVEL_CHOICES = (
        ('staff', 'Staff'),
        ('supervisor', 'Supervisor'),
        ('manager', 'Manager'),
        ('director', 'Director'),
    )

    name = models.CharField(max_length=100)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='positions'
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} (Lv {self.level})"