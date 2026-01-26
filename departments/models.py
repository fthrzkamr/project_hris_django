from django.db import models
from companies.models import Company

class Department(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name