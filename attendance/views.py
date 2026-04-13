from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Attendance, AttendanceRule
from employees.models import Employee

@login_required
def attendance_dashboard(request):
    employee = getattr(request.user, 'employee', None)
    if not employee:
        messages.error(request, "Akun Anda belum terhubung dengan data Karyawan.")
        return redirect('employees_list') # Balik ke list atau dashboard sesuai route Anda

    today = timezone.localtime().date()
    attendance = Attendance.objects.filter(employee=employee, date=today).first()
    
    # Ambil aturan jam kerja (buat default jika belum ada)
    rule = AttendanceRule.objects.first()
    if not rule:
        rule = AttendanceRule.objects.create(name="Jam Kerja Kantor", start_time="08:00:00", end_time="17:00:00")

    # Ambil riwayat absen berdasarkan bulan ini (default)
    import datetime
    selected_month = int(request.GET.get('month', today.month))
    selected_year = int(request.GET.get('year', today.year))
    
    history = Attendance.objects.filter(
        employee=employee, 
        date__year=selected_year, 
        date__month=selected_month
    ).order_by('-date')

    context = {
        'employee': employee,
        'attendance': attendance,
        'rule': rule,
        'today': today,
        'history': history,
        'selected_month': selected_month,
        'selected_year': selected_year,
    }
    return render(request, 'attendance/dashboard.html', context)

@login_required
def clock_in(request):
    if request.method == 'POST':
        employee = getattr(request.user, 'employee', None)
        if not employee:
            messages.error(request, "Profil karyawan tidak ditemukan.")
            return redirect('attendance_dashboard')
        
        today = timezone.localtime().date()
        now = timezone.localtime()
        
        # Cek apakah hari ini sudah absen masuk
        if Attendance.objects.filter(employee=employee, date=today).exists():
            messages.warning(request, "Anda sudah melakukan absen masuk hari ini.")
            return redirect('attendance_dashboard')
            
        # Tentukan status (Hadir vs Telat)
        rule = AttendanceRule.objects.first()
        status = 'present'
        if now.time() > rule.start_time:
            # Hitung selisih dalam menit
            import datetime
            ref = datetime.datetime.combine(today, rule.start_time)
            diff = (now.replace(tzinfo=None) - ref).total_seconds() / 60
            if diff > rule.grace_period:
                status = 'late'
        
        late_reason = request.POST.get('late_reason')
        late_evidence = request.FILES.get('late_evidence')

        Attendance.objects.create(
            employee=employee,
            date=today,
            clock_in=now.time(),
            status=status,
            late_reason=late_reason if status == 'late' else None,
            late_evidence=late_evidence if status == 'late' else None,
        )
        messages.success(request, "Berhasil Absen Masuk. Selamat bekerja!")
        
    return redirect('attendance_dashboard')

@login_required
def clock_out(request):
    if request.method == 'POST':
        employee = getattr(request.user, 'employee', None)
        if not employee:
            messages.error(request, "Profil karyawan tidak ditemukan.")
            return redirect('attendance_dashboard')
            
        today = timezone.localtime().date()
        now = timezone.localtime().time()
        
        attendance = Attendance.objects.filter(employee=employee, date=today).first()
        if not attendance:
            messages.error(request, "Anda belum absen masuk hari ini.")
        elif attendance.clock_out:
            messages.warning(request, "Anda sudah absen pulang hari ini.")
        else:
            attendance.clock_out = now
            attendance.save()
            messages.success(request, "Berhasil Absen Pulang. Hati-hati di jalan!")
            
    return redirect('attendance_dashboard')
