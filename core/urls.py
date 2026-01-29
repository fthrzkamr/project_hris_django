from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('direktur/', views.dashboard_direktur),
    path('manager/', views.dashboard_manager),
    path('asisten-manager/', views.dashboard_asisten_manager),
    path('leader/', views.dashboard_leader),
    path('karyawan/', views.dashboard_karyawan),
]
