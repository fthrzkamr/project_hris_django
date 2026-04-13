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
    from django.db.models import Q
    from django.core.paginator import Paginator
    
    today = timezone.now().date()
    current_year = today.year
    
    search_query = request.GET.get('q', '').strip()
    
    # Ambil semua karyawan aktif (Kecuali Admin/Superuser)
    employees = Employee.objects.filter(is_active=True).exclude(user__is_superuser=True).order_by('full_name')
    
    if search_query:
        employees = employees.filter(
            Q(full_name__icontains=search_query) | 
            Q(npp__icontains=search_query) |
            Q(department__name__icontains=search_query)
        )
    
    # Ambil saldo untuk tahun ini
    balances = LeaveBalance.objects.filter(year=current_year).select_related('employee')
    balance_dict = {b.employee_id: b for b in balances}
    
    one_year_ago = today - timezone.timedelta(days=365)
    eligible_types = ['tetap', 'kontrak', 'pkwt', 'pkwtt']
    
    emp_data = []
    for emp in employees:
        is_eligible = (
            emp.employment_type in eligible_types and 
            emp.join_date and emp.join_date <= one_year_ago
        )
        
        # Hitung durasi masa kerja
        tenure_str = "—"
        if emp.join_date:
            delta_days = (today - emp.join_date).days
            years  = delta_days // 365
            months = (delta_days % 365) // 30
            if years > 0 and months > 0:
                tenure_str = f"{years} Thn {months} Bln"
            elif years > 0:
                tenure_str = f"{years} Tahun"
            else:
                tenure_str = f"{months} Bulan"
        
        emp_data.append({
            'employee': emp,
            'balance': balance_dict.get(emp.id),
            'is_eligible': is_eligible,
            'tenure': tenure_str,
        })
        
    per_page = request.GET.get('per_page', '10')
    try:
        per_page = int(per_page)
    except ValueError:
        per_page = 10
        
    paginator = Paginator(emp_data, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
        
    return render(request, 'leaves/balance_list.html', {
        'page_obj': page_obj, 
        'current_year': current_year,
        'search_query': search_query,
        'per_page': per_page,
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
        ).exclude(user__is_superuser=True)
        
        count = 0
        for emp in employees:
            balance, created = LeaveBalance.objects.get_or_create(
                employee=emp,
                year=current_year,
                defaults={'total_balance': 12, 'used_balance': 0}
            )
            if not created:
                balance.total_balance = 12
                balance.used_balance = 0
                balance.save()
            count += 1
            
        messages.success(request, f'Berhasil mereset jatah cuti untuk {count} karyawan yang memenuhi kriteria.')
    return redirect('leave_balance_list')

@hr_or_admin_required
def leave_balance_create(request):
    employees = Employee.objects.filter(is_active=True).exclude(user__is_superuser=True).order_by('full_name')
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
    return render(request, 'leaves/balance_confirm_delete.html', {'balance': balance})

# --- Self Service (Employee Side) ---
from django.contrib.auth.decorators import login_required
from .models import LeaveType

@login_required
def leave_history(request):
    employee = getattr(request.user, 'employee', None)
    if not employee:
        messages.error(request, 'Profil karyawan tidak ditemukan untuk akun ini.')
        return redirect('dashboard')
    
    from django.utils import timezone
    current_year = timezone.now().year
    
    leaves = LeaveRequest.objects.filter(employee=employee).select_related('leave_type').order_by('-created_at')
    balance = LeaveBalance.objects.filter(employee=employee, year=current_year).first()
    
    context = {
        'leaves': leaves,
        'balance': balance,
        'current_year': current_year,
    }
    return render(request, 'leaves/history.html', context)

@login_required
def leave_apply(request):
    employee = getattr(request.user, 'employee', None)
    if not employee:
        messages.error(request, 'Hanya karyawan yang bisa mengajukan cuti.')
        return redirect('dashboard')

    leave_types = LeaveType.objects.filter(is_active=True).order_by('name')
    
    if request.method == 'POST':
        leave_type_id = request.POST.get('leave_type')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        reason = request.POST.get('reason')
        attachment = request.FILES.get('attachment')
        
        # Hitung durasi (sederhana tanpa memotong libur untuk sementara)
        from datetime import datetime
        d1 = datetime.strptime(start_date, '%Y-%m-%d')
        d2 = datetime.strptime(end_date, '%Y-%m-%d')
        duration = (d2 - d1).days + 1
        
        if duration <= 0:
            messages.error(request, 'Tanggal selesai harus setelah tanggal mulai.')
        else:
            LeaveRequest.objects.create(
                employee=employee,
                leave_type_id=leave_type_id,
                start_date=start_date,
                end_date=end_date,
                duration_days=duration,
                reason=reason,
                attachment=attachment
            )
            messages.success(request, 'Pengajuan cuti berhasil dikirim dan menunggu approval.')
            return redirect('leave_history')

    return render(request, 'leaves/apply_form.html', {'leave_types': leave_types})
