from django.db import models
from companies.models import Company

class Branch(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="branches"
    )
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name}"
