from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from employees.views import hr_or_admin_required
from .models import LeaveRequest, LeaveBalance

@hr_or_admin_required
def leave_management_list(request):
    leaves = LeaveRequest.objects.select_related('employee', 'leave_type').order_by('-created_at')
    
    status_filter = request.GET.get('status')
    if status_filter:
        leaves = leaves.filter(status=status_filter)
        
    context = {
        'leaves': leaves,
        'current_status': status_filter,
    }
    return render(request, 'leaves/management_list.html', context)

@hr_or_admin_required
def leave_approve(request, pk):
    leave = get_object_or_404(LeaveRequest, pk=pk)
    if request.method == 'POST':
        if leave.status != 'pending':
            messages.error(request, 'Status cuti tidak bisa diubah karena sudah bukan "Menunggu Approval".')
            return redirect('leave_management_list')
            
        leave.status = 'approved'
        leave.approved_by = getattr(request.user, 'employee', None)
        leave.save()
        
        # Potong saldo cuti tahunan jika jenis cuti tersebut diatur memotong kuota
        if leave.leave_type.is_deduct_annual:
            year = leave.start_date.year
            balance, _ = LeaveBalance.objects.get_or_create(
                employee=leave.employee,
                year=year,
                defaults={'total_balance': 12, 'used_balance': 0}
            )
            balance.used_balance += leave.duration_days
            balance.save()
            
        messages.success(request, f'Cuti {leave.employee.full_name} berhasil Disetujui.')
    return redirect('leave_management_list')

@hr_or_admin_required
def leave_reject(request, pk):
    leave = get_object_or_404(LeaveRequest, pk=pk)
    if request.method == 'POST':
        if leave.status != 'pending':
            messages.error(request, 'Status cuti tidak bisa diubah karena sudah bukan "Menunggu Approval".')
            return redirect('leave_management_list')
            
        leave.status = 'rejected'
        leave.save()
        messages.warning(request, f'Cuti {leave.employee.full_name} telah Ditolak.')
    return redirect('leave_management_list')

# --- Leave Balance CRUD untuk HR ---

from employees.models import Employee

@hr_or_admin_required
def leave_balance_list(request):
    from django.utils import timezone
    current_year = timezone.now().year
    
    # Ambil semua karyawan aktif
    employees = Employee.objects.filter(is_active=True).order_by('full_name')
    
    # Ambil saldo untuk tahun ini
    balances = LeaveBalance.objects.filter(year=current_year).select_related('employee')
    balance_dict = {b.employee_id: b for b in balances}
    
    # Cek eligibilitas tiap karyawan (Hanya untuk tampilan info di tabel)
    one_year_ago = timezone.now().date() - timezone.timedelta(days=365)
    eligible_types = ['tetap', 'kontrak', 'pkwt', 'pkwtt']
    
    emp_data = []
    for emp in employees:
        is_eligible = (
            emp.employment_type in eligible_types and 
            emp.join_date and emp.join_date <= one_year_ago
        )
        emp_data.append({
            'employee': emp,
            'balance': balance_dict.get(emp.id),
            'is_eligible': is_eligible
        })
        
    return render(request, 'leaves/balance_list.html', {
        'emp_data': emp_data, 
        'current_year': current_year
    })

@hr_or_admin_required
def leave_balance_reset_all(request):
    if request.method == 'POST':
        from django.utils import timezone
        current_year = timezone.now().year
        one_year_ago = timezone.now().date() - timezone.timedelta(days=365)
        eligible_types = ['tetap', 'kontrak', 'pkwt', 'pkwtt']
        
        employees = Employee.objects.filter(
            is_active=True,
            employment_type__in=eligible_types,
            join_date__lte=one_year_ago
        )
        
        count = 0
        for emp in employees:
            balance, created = LeaveBalance.objects.get_or_create(
                employee=emp,
                year=current_year,
                defaults={'total_balance': 12, 'used_balance': 0}
            )
            if not created:
                balance.total_balance = 12
                # used_balance biasanya tidak direset paksa ke 0 jika sudah berjalan, 
                # tapi user minta 'reset semua cuti menjadi 12'. Kita asumsikan reset jatah awal.
                balance.save()
            count += 1
            
        messages.success(request, f'Berhasil mereset jatah cuti untuk {count} karyawan yang memenuhi kriteria.')
    return redirect('leave_balance_list')

@hr_or_admin_required
def leave_balance_create(request):
    employees = Employee.objects.filter(is_active=True).order_by('full_name')
    selected_employee_id = request.GET.get('employee_id')
    
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        year = request.POST.get('year')
        total_balance = request.POST.get('total_balance')
        used_balance = request.POST.get('used_balance', 0)
        
        if LeaveBalance.objects.filter(employee_id=employee_id, year=year).exists():
            messages.error(request, f'Saldo cuti untuk karyawan tersebut di tahun {year} sudah ada!')
        else:
            LeaveBalance.objects.create(
                employee_id=employee_id,
                year=year,
                total_balance=total_balance,
                used_balance=used_balance
            )
            messages.success(request, 'Saldo cuti berhasil ditambahkan.')
            return redirect('leave_balance_list')
            
    return render(request, 'leaves/balance_form.html', {
        'employees': employees, 
        'selected_employee_id': selected_employee_id,
        'action': 'Tambah'
    })

@hr_or_admin_required
def leave_balance_edit(request, pk):
    balance = get_object_or_404(LeaveBalance, pk=pk)
    if request.method == 'POST':
        balance.total_balance = request.POST.get('total_balance')
        balance.used_balance = request.POST.get('used_balance')
        balance.save()
        messages.success(request, 'Saldo cuti berhasil diperbarui.')
        return redirect('leave_balance_list')
        
    return render(request, 'leaves/balance_form.html', {'balance': balance, 'action': 'Edit'})

@hr_or_admin_required
def leave_balance_delete(request, pk):
    balance = get_object_or_404(LeaveBalance, pk=pk)
    if request.method == 'POST':
        balance.delete()
        messages.success(request, 'Data saldo cuti berhasil dihapus.')
        return redirect('leave_balance_list')
    # Use generic confirmation or simple form if needed. We'll add a simple confirmation in template.
    return render(request, 'leaves/balance_confirm_delete.html', {'balance': balance})
