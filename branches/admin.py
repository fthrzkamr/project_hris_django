from django.contrib import admin
from .models import Branch

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'code')
    search_fields = ('name', 'code')
    list_filter = ('company',)
