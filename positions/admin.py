from django.contrib import admin
from .models import Position

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display  = ('name', 'is_active')
    list_filter   = ('is_active',)
    search_fields = ('name',)
