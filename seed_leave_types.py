import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from leaves.models import LeaveType

def seed_leave_types():
    # Menghapus data lama agar bersih dan sesuai permintaan baru
    # LeaveType.objects.all().delete() 
    
    types = [
        {
            'name': 'Cuti Tahunan',
            'is_deduct_annual': True,
            'requires_attachment': False,
            'default_days': None, # Fleksibel, user tentukan sendiri
        },
        {
            'name': 'Cuti Menikah',
            'is_deduct_annual': False,
            'requires_attachment': True,
            'default_days': 3,
        },
        {
            'name': 'Cuti Hamil',
            'is_deduct_annual': False,
            'requires_attachment': True,
            'default_days': 90,
        },
        {
            'name': 'Keluarga Inti Meninggal',
            'is_deduct_annual': False,
            'requires_attachment': False,
            'default_days': 2,
        },
        {
            'name': 'Menikahkan Anak',
            'is_deduct_annual': False,
            'requires_attachment': False,
            'default_days': 2,
        },
        {
            'name': 'Khitanan, Baptisan Anak',
            'is_deduct_annual': False,
            'requires_attachment': False,
            'default_days': 2,
        },
        {
            'name': 'Istri Melahirkan',
            'is_deduct_annual': False,
            'requires_attachment': False,
            'default_days': 4,
        },
        {
            'name': 'Anggota Keluarga Meninggal',
            'is_deduct_annual': False,
            'requires_attachment': False,
            'default_days': 1,
        },
        {
            'name': 'Izin Sakit',
            'is_deduct_annual': False,
            'requires_attachment': True,
            'default_days': None, # Fleksibel sesuai surat dokter
        },
        {
            'name': 'Hutang Cuti',
            'is_deduct_annual': True,
            'requires_attachment': False,
            'default_days': None,
        },
    ]

    count = 0
    for t in types:
        # Update if exists or create new
        obj, created = LeaveType.objects.update_or_create(
            name=t['name'],
            defaults={
                'is_deduct_annual': t['is_deduct_annual'],
                'requires_attachment': t['requires_attachment'],
                'default_days': t['default_days']
            }
        )
        if created:
            count += 1
            print(f"Added: {t['name']}")
        else:
            print(f"Updated: {t['name']}")
    
    print(f"Berhasil menyinkronkan {len(types)} data Master Jenis Cuti.")

if __name__ == '__main__':
    seed_leave_types()
