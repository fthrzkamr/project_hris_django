from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseForbidden


# =========================
# Helper: cek role (Group)
# =========================
def role_required(role_name):
    def check(user):
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

    employee = user.employee
    group = user.groups.first()  # sementara 1 role saja

    context = {
        "npp": employee.npp,
        "full_name": employee.full_name,
        "role": group.name if group else "-",
    }

    # sementara pakai text response (frontend belum ada)
    return HttpResponse(
        f"""
        <h2>Dashboard</h2>
        <p>NPP: {context['npp']}</p>
        <p>Nama: {context['full_name']}</p>
        <p>Role: {context['role']}</p>
        """
    )


# =========================
# DASHBOARD PER ROLE
# =========================

@role_required('direktur')
def dashboard_direktur(request):
    return HttpResponse("Dashboard Direktur")


@role_required('manager')
def dashboard_manager(request):
    return HttpResponse("Dashboard Manager")


@role_required('asisten_manager')
def dashboard_asisten_manager(request):
    return HttpResponse("Dashboard Asisten Manager")


@role_required('leader')
def dashboard_leader(request):
    return HttpResponse("Dashboard Leader")


@role_required('karyawan')
def dashboard_karyawan(request):
    return HttpResponse("Dashboard Karyawan")
