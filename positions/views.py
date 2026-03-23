from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from django.core.paginator import Paginator
from .models import Position


def hr_or_admin_required(view_func):
    @login_required(login_url='/login/')
    def wrapper(request, *args, **kwargs):
        user = request.user
        if user.is_superuser:
            return view_func(request, *args, **kwargs)
        if user.groups.filter(name__in=['direktur', 'manager', 'hr']).exists():
            return view_func(request, *args, **kwargs)
        messages.error(request, 'Anda tidak memiliki akses ke halaman ini.')
        return redirect('/')
    return wrapper


@hr_or_admin_required
def position_list(request):
    query    = request.GET.get('q', '')
    per_page = request.GET.get('per_page', '5')
    try:
        per_page = int(per_page)
        if per_page not in [5, 10, 25, 50, 100]:
            per_page = 5
    except ValueError:
        per_page = 5

    positions = Position.objects.annotate(employee_count=Count('employee'))
    if query:
        positions = positions.filter(name__icontains=query)
    positions = positions.order_by('name')

    paginator = Paginator(positions, per_page)
    page_obj  = paginator.get_page(request.GET.get('page', 1))

    return render(request, 'positions/list.html', {
        'page_obj':    page_obj,
        'positions':   page_obj,
        'total_count': paginator.count,
        'query':       query,
        'per_page':    per_page,
    })


@hr_or_admin_required
def position_create(request):
    if request.method == 'POST':
        name      = request.POST.get('name', '').strip()
        is_active = request.POST.get('is_active') == 'on'

        if not name:
            messages.error(request, 'Nama jabatan tidak boleh kosong.')
        elif Position.objects.filter(name__iexact=name).exists():
            messages.error(request, f'Jabatan "{name}" sudah ada.')
        else:
            Position.objects.create(name=name, is_active=is_active)
            messages.success(request, f'Jabatan "{name}" berhasil ditambahkan.')
            return redirect('position_list')

    return render(request, 'positions/form.html', {
        'action': 'Tambah',
    })


@hr_or_admin_required
def position_edit(request, pk):
    position = get_object_or_404(Position, pk=pk)
    if request.method == 'POST':
        name      = request.POST.get('name', '').strip()
        is_active = request.POST.get('is_active') == 'on'

        if not name:
            messages.error(request, 'Nama jabatan tidak boleh kosong.')
        elif Position.objects.filter(name__iexact=name).exclude(pk=pk).exists():
            messages.error(request, f'Jabatan "{name}" sudah ada.')
        else:
            position.name      = name
            position.is_active = is_active
            position.save()
            messages.success(request, f'Jabatan "{name}" berhasil diperbarui.')
            return redirect('position_list')

    return render(request, 'positions/form.html', {
        'action': 'Edit',
        'position': position,
    })


@hr_or_admin_required
def position_delete(request, pk):
    position = get_object_or_404(Position, pk=pk)
    if request.method == 'POST':
        name = position.name
        position.delete()
        messages.success(request, f'Jabatan "{name}" berhasil dihapus.')
        return redirect('position_list')
    return render(request, 'positions/confirm_delete.html', {'position': position})
