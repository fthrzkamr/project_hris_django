from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from companies.models import Company
from departments.models import Department
from positions.models import Position
from branches.models import Branch


class Employee(models.Model):

    GENDER_CHOICES = [('L', 'Laki-laki'), ('P', 'Perempuan')]
    RELIGION_CHOICES = [
        ('islam', 'Islam'), ('kristen', 'Kristen Protestan'),
        ('katolik', 'Katolik'), ('hindu', 'Hindu'),
        ('buddha', 'Buddha'), ('konghucu', 'Konghucu'), ('lainnya', 'Lainnya'),
    ]
    MARITAL_CHOICES = [
        ('belum_kawin', 'Belum Kawin'), ('kawin', 'Kawin'),
        ('cerai_hidup', 'Cerai Hidup'), ('cerai_mati', 'Cerai Mati'),
    ]
    BLOOD_CHOICES = [('A','A'),('B','B'),('AB','AB'),('O','O'),('?','Tidak Diketahui')]
    EDUCATION_CHOICES = [
        ('sd','SD'), ('smp','SMP'), ('sma','SMA/SMK'),
        ('d1','D1'), ('d2','D2'), ('d3','D3'), ('d4','D4'),
        ('s1','S1'), ('s2','S2'), ('s3','S3'),
    ]
    EMPLOYMENT_TYPE_CHOICES = [
        ('tetap','Karyawan Tetap'), ('kontrak','Karyawan Kontrak'),
        ('magang','Magang / Intern'), ('paruh_waktu','Paruh Waktu'),
        ('pkwt','PKWT'), ('pkwtt','PKWTT'),
    ]
    BPJS_KESEHATAN_TYPE_CHOICES = [
        ('1','Kelas 1'), ('2','Kelas 2'), ('3','Kelas 3'), ('non','Tidak Ada'),
    ]
    EMERGENCY_RELATION_CHOICES = [
        ('suami','Suami'), ('istri','Istri'), ('ayah','Ayah'), ('ibu','Ibu'),
        ('kakak','Kakak'), ('adik','Adik'), ('anak','Anak'), ('lainnya','Lainnya'),
    ]

    # ─── Akun & NPP ──────────────────────────────────────────────
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )
    npp       = models.CharField(max_length=20, unique=True, verbose_name='NPP')
    photo     = models.ImageField(upload_to='employees/photos/', blank=True, null=True)

    # ─── Identitas Pribadi ────────────────────────────────────────
    full_name    = models.CharField(max_length=150, verbose_name='Nama Lengkap')
    nickname     = models.CharField(max_length=50, blank=True, verbose_name='Nama Panggilan')
    gender       = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    birth_place  = models.CharField(max_length=100, blank=True, verbose_name='Tempat Lahir')
    birth_date   = models.DateField(null=True, blank=True, verbose_name='Tanggal Lahir')
    religion     = models.CharField(max_length=20, choices=RELIGION_CHOICES, blank=True)
    marital_status = models.CharField(max_length=20, choices=MARITAL_CHOICES, blank=True)
    blood_type   = models.CharField(max_length=3, choices=BLOOD_CHOICES, blank=True)
    nationality  = models.CharField(max_length=50, blank=True, default='WNI')
    nik          = models.CharField(max_length=20, blank=True, verbose_name='NIK / KTP')

    # ─── Kontak ───────────────────────────────────────────────────
    email   = models.EmailField(blank=True, null=True)
    phone   = models.CharField(max_length=20, blank=True, null=True)

    # ─── Alamat ───────────────────────────────────────────────────
    address      = models.TextField(blank=True, verbose_name='Alamat Lengkap')
    rt_rw        = models.CharField(max_length=10, blank=True, verbose_name='RT/RW')
    kelurahan    = models.CharField(max_length=100, blank=True)
    kecamatan    = models.CharField(max_length=100, blank=True)
    kota         = models.CharField(max_length=100, blank=True, verbose_name='Kota/Kabupaten')
    provinsi     = models.CharField(max_length=100, blank=True)
    kode_pos     = models.CharField(max_length=10, blank=True)

    # ─── Data Keluarga ────────────────────────────────────────────
    father_name = models.CharField(max_length=100, blank=True, verbose_name='Nama Ayah')
    mother_name = models.CharField(max_length=100, blank=True, verbose_name='Nama Ibu')

    # ─── Kontak Darurat ───────────────────────────────────────────
    emergency_name     = models.CharField(max_length=100, blank=True, verbose_name='Nama Kontak Darurat')
    emergency_phone    = models.CharField(max_length=20, blank=True, verbose_name='Telepon Darurat')
    emergency_relation = models.CharField(
        max_length=20, choices=EMERGENCY_RELATION_CHOICES, blank=True,
        verbose_name='Hubungan Darurat'
    )

    # ─── Pendidikan ───────────────────────────────────────────────
    last_education    = models.CharField(max_length=5, choices=EDUCATION_CHOICES, blank=True)
    education_major   = models.CharField(max_length=150, blank=True, verbose_name='Jurusan')
    education_school  = models.CharField(max_length=200, blank=True, verbose_name='Nama Institusi')
    graduation_year   = models.CharField(max_length=4, blank=True, verbose_name='Tahun Lulus')

    # ─── Dokumen Penting ──────────────────────────────────────────
    npwp                = models.CharField(max_length=30, blank=True, verbose_name='NPWP')
    bpjs_ketenagakerjaan = models.CharField(max_length=30, blank=True, verbose_name='No. BPJS Ketenagakerjaan')
    bpjs_kesehatan       = models.CharField(max_length=30, blank=True, verbose_name='No. BPJS Kesehatan')
    bpjs_kesehatan_type  = models.CharField(
        max_length=5, choices=BPJS_KESEHATAN_TYPE_CHOICES, blank=True, default='non',
        verbose_name='Kelas BPJS Kesehatan'
    )

    # ─── Perbankan ────────────────────────────────────────────────
    bank_name        = models.CharField(max_length=50, blank=True, verbose_name='Nama Bank')
    bank_account_no  = models.CharField(max_length=30, blank=True, verbose_name='No. Rekening')
    bank_account_name = models.CharField(max_length=100, blank=True, verbose_name='Nama di Rekening')

    # ─── Data Kepegawaian ─────────────────────────────────────────
    company         = models.ForeignKey(Company, on_delete=models.PROTECT, null=True, blank=True)
    department      = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    position        = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True)
    branch          = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True)
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE_CHOICES, blank=True)
    join_date       = models.DateField(null=True, blank=True, verbose_name='Tanggal Masuk')
    contract_start  = models.DateField(null=True, blank=True, verbose_name='Mulai Kontrak')
    contract_end    = models.DateField(null=True, blank=True, verbose_name='Selesai Kontrak')
    is_active       = models.BooleanField(default=True)

    class Meta:
        ordering = ['full_name']

    def __str__(self):
        return f"{self.npp} - {self.full_name}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new and not self.user:
            User = get_user_model()
            user, created = User.objects.get_or_create(username=self.npp)
            if created:
                user.first_name = self.full_name.split()[0] if self.full_name else ''
                user.email = self.email or ''
                user.set_password(self.npp)
                user.save()
            self.user = user
            super().save(update_fields=['user'])
