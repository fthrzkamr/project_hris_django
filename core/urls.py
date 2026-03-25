from django.urls import path
from .views import *

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('direktur/', dashboard_direktur, name='dashboard_direktur'),
    path('manager/', dashboard_manager, name='dashboard_manager'),
    path('asisten-manager/', dashboard_asisten_manager, name='dashboard_asisten_manager'),
    path('leader/', dashboard_leader, name='dashboard_leader'),
    path('karyawan/', dashboard_karyawan, name='dashboard_karyawan'),
]
