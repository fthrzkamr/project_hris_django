from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Employee
from companies.models import Company
from departments.models import Department
from positions.models import Position
from branches.models import Branch


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


def get_form_context():
    """Shared context untuk form tambah/edit karyawan."""
    return {
        'companies':   Company.objects.all().order_by('name'),
        'departments': Department.objects.all().order_by('name'),
        'positions':   Position.objects.all().order_by('name'),
        'branches':    Branch.objects.all().order_by('name'),
        'gender_choices':       Employee.GENDER_CHOICES,
        'religion_choices':     Employee.RELIGION_CHOICES,
        'marital_choices':      Employee.MARITAL_CHOICES,
        'blood_choices':        Employee.BLOOD_CHOICES,
        'education_choices':    Employee.EDUCATION_CHOICES,
        'employment_choices':   Employee.EMPLOYMENT_TYPE_CHOICES,
        'bpjs_kes_choices':     Employee.BPJS_KESEHATAN_TYPE_CHOICES,
        'emergency_rel_choices':Employee.EMERGENCY_RELATION_CHOICES,
    }


@hr_or_admin_required
def employee_list(request):
    query       = request.GET.get('q', '')
    dept_filter = request.GET.get('dept', '')
    pos_filter  = request.GET.get('pos', '')
    status_filter = request.GET.get('status', '')
    per_page    = request.GET.get('per_page', '10')
    try:
        per_page = int(per_page)
        if per_page not in [10, 25, 50, 100]:
            per_page = 10
    except ValueError:
        per_page = 10

    employees = Employee.objects.exclude(
        user__is_superuser=True
    ).exclude(
        npp='admin'
    ).select_related(
        'company', 'department', 'position', 'branch'
    )
    if query:
        employees = employees.filter(full_name__icontains=query) | \
                    employees.filter(npp__icontains=query)
    if dept_filter:
        employees = employees.filter(department_id=dept_filter)
    if pos_filter:
        employees = employees.filter(position_id=pos_filter)
    if status_filter == 'active':
        employees = employees.filter(is_active=True)
    elif status_filter == 'inactive':
        employees = employees.filter(is_active=False)

    employees = employees.order_by('full_name')
    paginator = Paginator(employees, per_page)
    page_obj  = paginator.get_page(request.GET.get('page', 1))

    return render(request, 'employees/list.html', {
        'page_obj':    page_obj,
        'employees':   page_obj,
        'total_count': paginator.count,
        'query':       query,
        'dept_filter': dept_filter,
        'pos_filter':  pos_filter,
        'status_filter': status_filter,
        'per_page':    per_page,
        'departments': Department.objects.all().order_by('name'),
        'positions':   Position.objects.all().order_by('name'),
    })


@hr_or_admin_required
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'employees/detail.html', {'employee': employee})


class SafeDict(dict):
    def __getitem__(self, key):
        return super().get(key, '')
    def __getattr__(self, key):
        return self.get(key, '')

@hr_or_admin_required
def employee_create(request):
    ctx = get_form_context()
    post_dict = request.POST.dict()
    
    if request.method == 'GET':
        post_dict['npp'] = ''
            
    ctx['post'] = SafeDict(post_dict)
    
    if request.method == 'POST':
        npp       = request.POST.get('npp', '').strip()
        full_name = request.POST.get('full_name', '').strip()

        if not npp:
            from django.utils import timezone
            import random
            yy = timezone.now().strftime('%y')
            
            b_date = request.POST.get('birth_date', '')
            j_date = request.POST.get('join_date', '')
            
            j_m = j_date[5:7] if len(j_date) >= 7 else f"{random.randint(10,99)}"
            b_d = b_date[8:10] if len(b_date) >= 10 else f"{random.randint(10,99)}"
            
            base_npp = f"{yy}{j_m}{b_d}"
            seq = 1
            while True:
                candidate = f"{base_npp}{seq:02d}"
                if not Employee.objects.filter(npp=candidate).exists():
                    npp = candidate
                    break
                seq += 1

        if not npp:
            messages.error(request, 'NPP tidak boleh kosong.')
        elif not full_name:
            messages.error(request, 'Nama lengkap tidak boleh kosong.')
        elif Employee.objects.filter(npp=npp).exists():
            messages.error(request, f'NPP "{npp}" sudah digunakan.')
        else:
            def get(field, default=''):
                return request.POST.get(field, default).strip() or default

            employee = Employee.objects.create(
                npp=npp, full_name=full_name,
                nickname=get('nickname'),
                gender=get('gender'),
                birth_place=get('birth_place'),
                birth_date=request.POST.get('birth_date') or None,
                religion=get('religion'),
                marital_status=get('marital_status'),
                blood_type=get('blood_type'),
                nationality=get('nationality', 'WNI'),
                nik=get('nik'),
                email=get('email') or None,
                phone=get('phone'),
                address=get('address'),
                rt_rw=get('rt_rw'),
                kelurahan=get('kelurahan'),
                kecamatan=get('kecamatan'),
                kota=get('kota'),
                provinsi=get('provinsi'),
                kode_pos=get('kode_pos'),
                father_name=get('father_name'),
                mother_name=get('mother_name'),
                emergency_name=get('emergency_name'),
                emergency_phone=get('emergency_phone'),
                emergency_relation=get('emergency_relation'),
                last_education=get('last_education'),
                education_major=get('education_major'),
                education_school=get('education_school'),
                graduation_year=get('graduation_year'),
                npwp=get('npwp'),
                bpjs_ketenagakerjaan=get('bpjs_ketenagakerjaan'),
                bpjs_kesehatan=get('bpjs_kesehatan'),
                bpjs_kesehatan_type=get('bpjs_kesehatan_type', 'non'),
                bank_name=get('bank_name'),
                bank_account_no=get('bank_account_no'),
                bank_account_name=get('bank_account_name'),
                company_id=request.POST.get('company') or None,
                department_id=request.POST.get('department') or None,
                position_id=request.POST.get('position') or None,
                branch_id=request.POST.get('branch') or None,
                employment_type=get('employment_type'),
                join_date=request.POST.get('join_date') or None,
                contract_start=request.POST.get('contract_start') or None,
                contract_end=request.POST.get('contract_end') or None,
                is_active=request.POST.get('is_active') == 'on',
            )
            if 'photo' in request.FILES:
                employee.photo = request.FILES['photo']
                employee.save(update_fields=['photo'])

            messages.success(request, f'Karyawan "{full_name}" berhasil ditambahkan. Login: {npp} / {npp}')
            return redirect('employee_list')

        ctx.update({'post': request.POST})
    return render(request, 'employees/form.html', {**ctx, 'action': 'Tambah'})


@hr_or_admin_required
def employee_edit(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    ctx = get_form_context()
    ctx['post'] = SafeDict(request.POST.dict())
    
    if request.method == 'POST':
        npp       = request.POST.get('npp', '').strip()
        full_name = request.POST.get('full_name', '').strip()

        if not npp:
            messages.error(request, 'NPP tidak boleh kosong.')
        elif not full_name:
            messages.error(request, 'Nama lengkap tidak boleh kosong.')
        elif Employee.objects.filter(npp=npp).exclude(pk=pk).exists():
            messages.error(request, f'NPP "{npp}" sudah digunakan.')
        else:
            def get(field, default=''):
                return request.POST.get(field, default).strip() or default

            employee.npp           = npp
            employee.full_name     = full_name
            employee.nickname      = get('nickname')
            employee.gender        = get('gender')
            employee.birth_place   = get('birth_place')
            employee.birth_date    = request.POST.get('birth_date') or None
            employee.religion      = get('religion')
            employee.marital_status = get('marital_status')
            employee.blood_type    = get('blood_type')
            employee.nationality   = get('nationality', 'WNI')
            employee.nik           = get('nik')
            employee.email         = get('email') or None
            employee.phone         = get('phone')
            employee.address       = get('address')
            employee.rt_rw         = get('rt_rw')
            employee.kelurahan     = get('kelurahan')
            employee.kecamatan     = get('kecamatan')
            employee.kota          = get('kota')
            employee.provinsi      = get('provinsi')
            employee.kode_pos      = get('kode_pos')
            employee.father_name   = get('father_name')
            employee.mother_name   = get('mother_name')
            employee.emergency_name     = get('emergency_name')
            employee.emergency_phone    = get('emergency_phone')
            employee.emergency_relation = get('emergency_relation')
            employee.last_education     = get('last_education')
            employee.education_major    = get('education_major')
            employee.education_school   = get('education_school')
            employee.graduation_year    = get('graduation_year')
            employee.npwp               = get('npwp')
            employee.bpjs_ketenagakerjaan = get('bpjs_ketenagakerjaan')
            employee.bpjs_kesehatan     = get('bpjs_kesehatan')
            employee.bpjs_kesehatan_type = get('bpjs_kesehatan_type', 'non')
            employee.bank_name          = get('bank_name')
            employee.bank_account_no    = get('bank_account_no')
            employee.bank_account_name  = get('bank_account_name')
            employee.company_id    = request.POST.get('company') or None
            employee.department_id = request.POST.get('department') or None
            employee.position_id   = request.POST.get('position') or None
            employee.branch_id     = request.POST.get('branch') or None
            employee.employment_type = get('employment_type')
            employee.join_date     = request.POST.get('join_date') or None
            employee.contract_start = request.POST.get('contract_start') or None
            employee.contract_end  = request.POST.get('contract_end') or None
            employee.is_active     = request.POST.get('is_active') == 'on'
            if 'photo' in request.FILES:
                employee.photo = request.FILES['photo']
            employee.save()
            messages.success(request, f'Data "{full_name}" berhasil diperbarui.')
            return redirect('employee_list')

        # ctx.update({'post': request.POST})
    return render(request, 'employees/form.html', {**ctx, 'action': 'Edit', 'employee': employee})


@hr_or_admin_required
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        name = employee.full_name
        employee.delete()
        messages.success(request, f'Karyawan "{name}" berhasil dihapus.')
        return redirect('employee_list')
    return render(request, 'employees/confirm_delete.html', {'employee': employee})
