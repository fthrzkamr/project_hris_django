from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.core.paginator import Paginator
from .models import Department


def hr_or_admin_required(view_func):
    """Decorator: hanya superuser, direktur, manager, hr yang bisa akses."""
    @login_required(login_url='/login/')
    def wrapper(request, *args, **kwargs):
        user = request.user
        if user.is_superuser:
            return view_func(request, *args, **kwargs)
        allowed = ['direktur', 'manager', 'hr']
        if user.groups.filter(name__in=allowed).exists():
            return view_func(request, *args, **kwargs)
        messages.error(request, 'Anda tidak memiliki akses ke halaman ini.')
        return redirect('/')
    return wrapper


@hr_or_admin_required
def department_list(request):
    query    = request.GET.get('q', '')
    per_page = request.GET.get('per_page', '5')
    try:
        per_page = int(per_page)
        if per_page not in [5, 10, 25, 50, 100]:
            per_page = 5
    except ValueError:
        per_page = 5

    departments = Department.objects.annotate(
        employee_count=Count('employee')
    )
    if query:
        departments = departments.filter(name__icontains=query)
    departments = departments.order_by('name')

    paginator = Paginator(departments, per_page)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'departments/list.html', {
        'page_obj':   page_obj,
        'departments': page_obj,          # agar loop template tetap bisa pakai nama ini
        'total_count': paginator.count,
        'query':      query,
        'per_page':   per_page,
        'paginator':  paginator,
    })



@hr_or_admin_required
def department_create(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if not name:
            messages.error(request, 'Nama departemen tidak boleh kosong.')
        elif Department.objects.filter(name__iexact=name).exists():
            messages.error(request, f'Departemen "{name}" sudah ada.')
        else:
            Department.objects.create(name=name)
            messages.success(request, f'Departemen "{name}" berhasil ditambahkan.')
            return redirect('department_list')
    return render(request, 'departments/form.html', {'action': 'Tambah'})


@hr_or_admin_required
def department_edit(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if not name:
            messages.error(request, 'Nama departemen tidak boleh kosong.')
        elif Department.objects.filter(name__iexact=name).exclude(pk=pk).exists():
            messages.error(request, f'Departemen "{name}" sudah ada.')
        else:
            department.name = name
            department.save()
            messages.success(request, f'Departemen berhasil diperbarui menjadi "{name}".')
            return redirect('department_list')
    return render(request, 'departments/form.html', {
        'action': 'Edit',
        'department': department,
    })


@hr_or_admin_required
def department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        name = department.name
        department.delete()
        messages.success(request, f'Departemen "{name}" berhasil dihapus.')
        return redirect('department_list')
    return render(request, 'departments/confirm_delete.html', {
        'department': department,
    })
