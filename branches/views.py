from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from django.core.paginator import Paginator
from .models import Branch
from companies.models import Company


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
def branch_list(request):
    query    = request.GET.get('q', '')
    per_page = request.GET.get('per_page', '5')
    try:
        per_page = int(per_page)
        if per_page not in [5, 10, 25, 50, 100]:
            per_page = 5
    except ValueError:
        per_page = 5

    branches = Branch.objects.select_related('company').annotate(
        employee_count=Count('employee')
    )
    if query:
        branches = branches.filter(name__icontains=query)
    branches = branches.order_by('company__name', 'name')

    paginator = Paginator(branches, per_page)
    page_obj  = paginator.get_page(request.GET.get('page', 1))

    return render(request, 'branches/list.html', {
        'page_obj':    page_obj,
        'branches':    page_obj,
        'total_count': paginator.count,
        'query':       query,
        'per_page':    per_page,
    })


@hr_or_admin_required
def branch_create(request):
    companies = Company.objects.all().order_by('name')
    if request.method == 'POST':
        name       = request.POST.get('name', '').strip()
        address    = request.POST.get('address', '').strip()
        company_id = request.POST.get('company', '')

        if not name:
            messages.error(request, 'Nama cabang tidak boleh kosong.')
        elif not company_id:
            messages.error(request, 'Perusahaan harus dipilih.')
        elif Branch.objects.filter(name__iexact=name, company_id=company_id).exists():
            messages.error(request, f'Cabang "{name}" sudah ada di perusahaan tersebut.')
        else:
            Branch.objects.create(
                name=name, address=address, company_id=company_id
            )
            messages.success(request, f'Cabang "{name}" berhasil ditambahkan.')
            return redirect('branch_list')

    return render(request, 'branches/form.html', {
        'action': 'Tambah', 'companies': companies,
    })


@hr_or_admin_required
def branch_edit(request, pk):
    branch    = get_object_or_404(Branch, pk=pk)
    companies = Company.objects.all().order_by('name')
    if request.method == 'POST':
        name       = request.POST.get('name', '').strip()
        address    = request.POST.get('address', '').strip()
        company_id = request.POST.get('company', '')

        if not name:
            messages.error(request, 'Nama cabang tidak boleh kosong.')
        elif not company_id:
            messages.error(request, 'Perusahaan harus dipilih.')
        elif Branch.objects.filter(name__iexact=name, company_id=company_id).exclude(pk=pk).exists():
            messages.error(request, f'Cabang "{name}" sudah ada di perusahaan tersebut.')
        else:
            branch.name       = name
            branch.address    = address
            branch.company_id = company_id
            branch.save()
            messages.success(request, f'Cabang "{name}" berhasil diperbarui.')
            return redirect('branch_list')

    return render(request, 'branches/form.html', {
        'action': 'Edit', 'branch': branch, 'companies': companies,
    })


@hr_or_admin_required
def branch_delete(request, pk):
    branch = get_object_or_404(Branch, pk=pk)
    if request.method == 'POST':
        name = branch.name
        branch.delete()
        messages.success(request, f'Cabang "{name}" berhasil dihapus.')
        return redirect('branch_list')
    return render(request, 'branches/confirm_delete.html', {'branch': branch})
