from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseForbidden


# =========================
# Helper: cek role (Group)
# =========================
def role_required(role_name):
    def check(user):
        # Superuser punya akses ke semua fitur
        if user.is_superuser:
            return True
        return user.is_authenticated and user.groups.filter(name=role_name).exists()
    return user_passes_test(check, login_url='/login/')


# =========================
# DASHBOARD UMUM
# =========================
@login_required(login_url='/login/')
def dashboard(request):
    user = request.user

    # pastikan user punya employee
    if not hasattr(user, 'employee'):
        return HttpResponse(
            f"""
            <html>
            <head><title>Employee Not Found</title></head>
            <body style="font-family: Arial; text-align: center; padding-top: 100px;">
                <h1 style="color: #e74c3c;">⚠️ Employee Profile Tidak Ditemukan</h1>
                <p>User <strong>{user.username}</strong> belum terhubung dengan data Employee.</p>
                <p>Silakan hubungi HR atau buat data Employee terlebih dahulu.</p>
                <br>
                <a href="/admin/" style="padding: 10px 20px; background: #3498db; color: white; text-decoration: none; border-radius: 4px;">Ke Admin Panel</a>
                <a href="/logout/" style="padding: 10px 20px; background: #95a5a6; color: white; text-decoration: none; border-radius: 4px; margin-left: 10px;">Logout</a>
            </body>
            </html>
            """
        )

    # SUPERUSER BISA AKSES SEMUA, TIDAK DIPAKSA KE ADMIN LAGI
    # if user.is_superuser:
    #     return redirect('/admin/')

    employee = user.employee
    group = user.groups.first()

    # Redirect ke dashboard sesuai role
    if user.is_superuser:
        return render(request, 'core/dashboard.html', {'role': 'Administrator'})

    if user.groups.filter(name='direktur').exists():
        return redirect('dashboard_direktur')
    elif user.groups.filter(name='manager').exists():
        return redirect('dashboard_manager')
    elif user.groups.filter(name='asisten_manager').exists():
        return redirect('dashboard_asisten_manager')
    elif user.groups.filter(name='leader').exists():
        return redirect('dashboard_leader')
    elif user.groups.filter(name='karyawan').exists():
        return redirect('dashboard_karyawan')

    # Jika belum ada role, tampilkan info dasar
    context = {
        "npp": employee.npp,
        "full_name": employee.full_name,
        "role": group.name if group else "-",
    }

    return HttpResponse(
        f"""
        <html>
        <head><title>Dashboard</title></head>
        <body style="font-family: Arial; padding: 20px;">
            <h2>Dashboard</h2>
            <p>NPP: {context['npp']}</p>
            <p>Nama: {context['full_name']}</p>
            <p>Role: {context['role']}</p>
            <br>
            <p style="color: #e67e22;">⚠️ Role belum ditentukan. Hubungi admin untuk assign role.</p>
            <br>
            <a href="/logout/" style="padding: 10px 20px; background: #e74c3c; color: white; text-decoration: none; border-radius: 4px;">Logout</a>
        </body>
        </html>
        """
    )


# =========================
# DASHBOARD PER ROLE
# =========================

@role_required('direktur')
def dashboard_direktur(request):
    context = {
        'role': 'direktur'
    }
    return render(request, 'core/dashboard.html', context)


@role_required('manager')
def dashboard_manager(request):
    context = {
        'role': 'manager'
    }
    return render(request, 'core/dashboard.html', context)


@role_required('asisten_manager')
def dashboard_asisten_manager(request):
    context = {
        'role': 'asisten_manager'
    }
    return render(request, 'core/dashboard.html', context)


@role_required('leader')
def dashboard_leader(request):
    context = {
        'role': 'leader'
    }
    return render(request, 'core/dashboard.html', context)


@role_required('karyawan')
def dashboard_karyawan(request):
    context = {
        'role': 'karyawan'
    }
    return render(request, 'core/dashboard.html', context)

