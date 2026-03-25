from django.contrib import admin
from .models import LeaveType, LeaveBalance, LeaveRequest

@admin.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_deduct_annual', 'requires_attachment', 'is_active')

@admin.register(LeaveBalance)
class LeaveBalanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'year', 'total_balance', 'used_balance', 'remaining_balance')
    list_filter = ('year',)
    search_fields = ('employee__full_name', 'employee__npp')

@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_type', 'start_date', 'end_date', 'duration_days', 'status')
    list_filter = ('status', 'leave_type')
    search_fields = ('employee__full_name', 'employee__npp', 'reason')
