from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Company


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
def company_list(request):
    query    = request.GET.get('q', '')
    per_page = request.GET.get('per_page', '5')
    try:
        per_page = int(per_page)
        if per_page not in [5, 10, 25, 50, 100]:
            per_page = 5
    except ValueError:
        per_page = 5

    companies = Company.objects.all()
    if query:
        companies = companies.filter(name__icontains=query)

    paginator = Paginator(companies, per_page)
    page_obj  = paginator.get_page(request.GET.get('page', 1))

    return render(request, 'companies/list.html', {
        'page_obj':    page_obj,
        'companies':   page_obj,
        'total_count': paginator.count,
        'query':       query,
        'per_page':    per_page,
    })


@hr_or_admin_required
def company_create(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()

        if not name:
            messages.error(request, 'Nama perusahaan tidak boleh kosong.')
        elif Company.objects.filter(name__iexact=name).exists():
            messages.error(request, f'Perusahaan "{name}" sudah ada.')
        else:
            Company.objects.create(name=name)
            messages.success(request, f'Perusahaan "{name}" berhasil ditambahkan.')
            return redirect('company_list')

    return render(request, 'companies/form.html', {'action': 'Tambah'})


@hr_or_admin_required
def company_edit(request, pk):
    company = get_object_or_404(Company, pk=pk)
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()

        if not name:
            messages.error(request, 'Nama perusahaan tidak boleh kosong.')
        elif Company.objects.filter(name__iexact=name).exclude(pk=pk).exists():
            messages.error(request, f'Perusahaan "{name}" sudah ada.')
        else:
            company.name = name
            company.save()
            messages.success(request, f'Perusahaan "{name}" berhasil diperbarui.')
            return redirect('company_list')

    return render(request, 'companies/form.html', {
        'action': 'Edit', 'company': company,
    })


@hr_or_admin_required
def company_delete(request, pk):
    company = get_object_or_404(Company, pk=pk)
    if request.method == 'POST':
        name = company.name
        company.delete()
        messages.success(request, f'Perusahaan "{name}" berhasil dihapus.')
        return redirect('company_list')
    return render(request, 'companies/confirm_delete.html', {'company': company})
