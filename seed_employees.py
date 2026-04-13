"""
Run: python manage.py shell < seed_employees.py
"""
import os, django, datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from employees.models import Employee
from departments.models import Department
from positions.models import Position
from branches.models import Branch
from companies.models import Company

# Buat data master jika belum ada
company, _ = Company.objects.get_or_create(name="PT Solusi Digital Nusantara")
dept_it, _  = Department.objects.get_or_create(name="Technology", defaults={"company": company})
dept_hr, _  = Department.objects.get_or_create(name="Human Resources", defaults={"company": company})
dept_fin, _ = Department.objects.get_or_create(name="Finance", defaults={"company": company})
dept_ops, _ = Department.objects.get_or_create(name="Operations", defaults={"company": company})
dept_mkt, _ = Department.objects.get_or_create(name="Marketing", defaults={"company": company})

pos_dev, _    = Position.objects.get_or_create(name="Software Engineer")
pos_pm, _     = Position.objects.get_or_create(name="Project Manager")
pos_hr, _     = Position.objects.get_or_create(name="HR Specialist")
pos_fa, _     = Position.objects.get_or_create(name="Finance Analyst")
pos_ops, _    = Position.objects.get_or_create(name="Operations Manager")
pos_mkt, _    = Position.objects.get_or_create(name="Marketing Executive")
pos_qa, _     = Position.objects.get_or_create(name="QA Engineer")
pos_data, _   = Position.objects.get_or_create(name="Data Analyst")
pos_devops, _ = Position.objects.get_or_create(name="DevOps Engineer")
pos_ui, _     = Position.objects.get_or_create(name="UI/UX Designer")

branch_jkt, _ = Branch.objects.get_or_create(name="Jakarta Pusat", defaults={"company": company})
branch_bdg, _ = Branch.objects.get_or_create(name="Bandung", defaults={"company": company})
branch_sby, _ = Branch.objects.get_or_create(name="Surabaya", defaults={"company": company})

employees_data = [
    dict(
        npp="26031501", full_name="Arif Budi Santoso", nickname="Arif", gender="L",
        birth_place="Jakarta", birth_date=datetime.date(1993, 8, 15),
        email="arif.budi@company.id", phone="08123456001",
        address="Jl. Merdeka No. 10, Menteng", kota="Jakarta Pusat", provinsi="DKI Jakarta",
        religion="islam", marital_status="kawin", blood_type="O", nationality="WNI",
        nik="3171234500001", npwp="12.345.678.9-001.000",
        last_education="s1", education_major="Teknik Informatika", education_school="Universitas Indonesia", graduation_year="2016",
        bpjs_kesehatan="0001234567001", bpjs_ketenagakerjaan="A001234001",
        bank_name="BCA", bank_account_no="1234500001", bank_account_name="Arif Budi Santoso",
        company=company, department=dept_it, position=pos_dev, branch=branch_jkt,
        employment_type="tetap", join_date=datetime.date(2020, 3, 1), is_active=True,
    ),
    dict(
        npp="26031502", full_name="Dewi Rahmawati", nickname="Dewi", gender="P",
        birth_place="Bandung", birth_date=datetime.date(1995, 4, 22),
        email="dewi.rahmawati@company.id", phone="08123456002",
        address="Jl. Sudirman No. 5, Bandung", kota="Bandung", provinsi="Jawa Barat",
        religion="islam", marital_status="belum_kawin", blood_type="A", nationality="WNI",
        nik="3271234500002", last_education="s2", education_major="Manajemen SDM", education_school="Universitas Padjadjaran", graduation_year="2020",
        bpjs_kesehatan="0001234567002", bpjs_ketenagakerjaan="A001234002",
        bank_name="BNI", bank_account_no="1234500002", bank_account_name="Dewi Rahmawati",
        company=company, department=dept_hr, position=pos_hr, branch=branch_bdg,
        employment_type="tetap", join_date=datetime.date(2021, 6, 15), is_active=True,
    ),
    dict(
        npp="26031503", full_name="Rizky Firmansyah", nickname="Rizky", gender="L",
        birth_place="Surabaya", birth_date=datetime.date(1990, 11, 5),
        email="rizky.firmansyah@company.id", phone="08123456003",
        address="Jl. Ahmad Yani No. 20, Surabaya", kota="Surabaya", provinsi="Jawa Timur",
        religion="islam", marital_status="kawin", blood_type="B", nationality="WNI",
        nik="3571234500003", last_education="s1", education_major="Manajemen", education_school="Universitas Airlangga", graduation_year="2012",
        bpjs_kesehatan="0001234567003", bpjs_ketenagakerjaan="A001234003",
        bank_name="Mandiri", bank_account_no="1234500003", bank_account_name="Rizky Firmansyah",
        company=company, department=dept_ops, position=pos_ops, branch=branch_sby,
        employment_type="tetap", join_date=datetime.date(2019, 1, 10), is_active=True,
    ),
    dict(
        npp="26031504", full_name="Siti Nurhaliza", nickname="Siti", gender="P",
        birth_place="Yogyakarta", birth_date=datetime.date(1997, 7, 18),
        email="siti.nurhaliza@company.id", phone="08123456004",
        address="Jl. Malioboro Blok C No. 3, Yogyakarta", kota="Yogyakarta", provinsi="DI Yogyakarta",
        religion="islam", marital_status="belum_kawin", blood_type="AB", nationality="WNI",
        nik="3401234500004", last_education="d3", education_major="Akuntansi", education_school="STIE YKPN", graduation_year="2019",
        bpjs_kesehatan="0001234567004", bpjs_ketenagakerjaan="A001234004",
        bank_name="BRI", bank_account_no="1234500004", bank_account_name="Siti Nurhaliza",
        company=company, department=dept_fin, position=pos_fa, branch=branch_jkt,
        employment_type="kontrak", join_date=datetime.date(2023, 3, 1), is_active=True,
    ),
    dict(
        npp="26031505", full_name="Budi Prasetyo", nickname="Budi", gender="L",
        birth_place="Semarang", birth_date=datetime.date(1988, 2, 25),
        email="budi.prasetyo@company.id", phone="08123456005",
        address="Jl. Pandanaran No. 7, Semarang", kota="Semarang", provinsi="Jawa Tengah",
        religion="kristen", marital_status="kawin", blood_type="O", nationality="WNI",
        nik="3371234500005", last_education="s1", education_major="Sistem Informasi", education_school="Universitas Diponegoro", graduation_year="2010",
        bpjs_kesehatan="0001234567005", bpjs_ketenagakerjaan="A001234005",
        bank_name="BCA", bank_account_no="1234500005", bank_account_name="Budi Prasetyo",
        company=company, department=dept_it, position=pos_devops, branch=branch_jkt,
        employment_type="tetap", join_date=datetime.date(2018, 7, 20), is_active=True,
    ),
    dict(
        npp="26031506", full_name="Annisa Putri Handayani", nickname="Annisa", gender="P",
        birth_place="Medan", birth_date=datetime.date(1998, 9, 30),
        email="annisa.putri@company.id", phone="08123456006",
        address="Jl. Imam Bonjol No. 55, Medan", kota="Medan", provinsi="Sumatera Utara",
        religion="islam", marital_status="belum_kawin", blood_type="A", nationality="WNI",
        nik="1271234500006", last_education="s1", education_major="Desain Komunikasi Visual", education_school="Universitas Sumatera Utara", graduation_year="2020",
        bpjs_kesehatan="0001234567006", bpjs_ketenagakerjaan="A001234006",
        bank_name="BNI", bank_account_no="1234500006", bank_account_name="Annisa Putri Handayani",
        company=company, department=dept_it, position=pos_ui, branch=branch_jkt,
        employment_type="kontrak", join_date=datetime.date(2024, 1, 15), is_active=True,
    ),
    dict(
        npp="26031507", full_name="Hendra Wijaya", nickname="Hendra", gender="L",
        birth_place="Jakarta", birth_date=datetime.date(1992, 3, 12),
        email="hendra.wijaya@company.id", phone="08123456007",
        address="Jl. Gatot Subroto Kav. 8, Jakarta", kota="Jakarta Selatan", provinsi="DKI Jakarta",
        religion="buddha", marital_status="kawin", blood_type="B", nationality="WNI",
        nik="3174234500007", last_education="s1", education_major="Ilmu Komputer", education_school="Binus University", graduation_year="2014",
        bpjs_kesehatan="0001234567007", bpjs_ketenagakerjaan="A001234007",
        bank_name="Mandiri", bank_account_no="1234500007", bank_account_name="Hendra Wijaya",
        company=company, department=dept_it, position=pos_pm, branch=branch_jkt,
        employment_type="tetap", join_date=datetime.date(2017, 5, 3), is_active=True,
    ),
    dict(
        npp="26031508", full_name="Maya Indah Permatasari", nickname="Maya", gender="P",
        birth_place="Bandung", birth_date=datetime.date(1996, 12, 8),
        email="maya.indah@company.id", phone="08123456008",
        address="Jl. Setiabudi No. 12, Bandung", kota="Bandung", provinsi="Jawa Barat",
        religion="islam", marital_status="belum_kawin", blood_type="O", nationality="WNI",
        nik="3273234500008", last_education="s1", education_major="Statistika", education_school="Institut Teknologi Bandung", graduation_year="2018",
        bpjs_kesehatan="0001234567008", bpjs_ketenagakerjaan="A001234008",
        bank_name="BCA", bank_account_no="1234500008", bank_account_name="Maya Indah Permatasari",
        company=company, department=dept_it, position=pos_data, branch=branch_bdg,
        employment_type="tetap", join_date=datetime.date(2022, 2, 1), is_active=True,
    ),
    dict(
        npp="26031509", full_name="Fajar Nugroho", nickname="Fajar", gender="L",
        birth_place="Solo", birth_date=datetime.date(1994, 6, 17),
        email="fajar.nugroho@company.id", phone="08123456009",
        address="Jl. Slamet Riyadi No. 33, Solo", kota="Solo", provinsi="Jawa Tengah",
        religion="islam", marital_status="kawin", blood_type="A", nationality="WNI",
        nik="3372234500009", last_education="s1", education_major="Marketing", education_school="Universitas Sebelas Maret", graduation_year="2016",
        bpjs_kesehatan="0001234567009", bpjs_ketenagakerjaan="A001234009",
        bank_name="BRI", bank_account_no="1234500009", bank_account_name="Fajar Nugroho",
        company=company, department=dept_mkt, position=pos_mkt, branch=branch_sby,
        employment_type="pkwt", join_date=datetime.date(2023, 8, 1), is_active=True,
    ),
    dict(
        npp="26031510", full_name="Rahma Aulia Sari", nickname="Rahma", gender="P",
        birth_place="Makassar", birth_date=datetime.date(1999, 1, 28),
        email="rahma.aulia@company.id", phone="08123456010",
        address="Jl. Perintis Kemerdekaan No. 45, Makassar", kota="Makassar", provinsi="Sulawesi Selatan",
        religion="islam", marital_status="belum_kawin", blood_type="AB", nationality="WNI",
        nik="7371234500010", last_education="s1", education_major="Teknik Informatika", education_school="Universitas Hasanuddin", graduation_year="2021",
        bpjs_kesehatan="0001234567010", bpjs_ketenagakerjaan="A001234010",
        bank_name="BNI", bank_account_no="1234500010", bank_account_name="Rahma Aulia Sari",
        company=company, department=dept_it, position=pos_qa, branch=branch_jkt,
        employment_type="pkwt", join_date=datetime.date(2024, 6, 1), is_active=True,
    ),
]

created = 0
skipped = 0
for data in employees_data:
    npp = data.get("npp")
    if Employee.objects.filter(npp=npp).exists():
        print(f"  SKIP: {data['full_name']} (NPP {npp} sudah ada)")
        skipped += 1
    else:
        Employee.objects.create(**data)
        print(f"  OK: {data['full_name']} ({npp})")
        created += 1

print(f"\nSelesai! {created} karyawan berhasil ditambahkan, {skipped} dilewati.")
