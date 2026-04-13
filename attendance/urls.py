from django.urls import path
from . import views

urlpatterns = [
    path('my-attendance/', views.attendance_dashboard, name='attendance_dashboard'),
    path('clock-in/', views.clock_in, name='attendance_clock_in'),
    path('clock-out/', views.clock_out, name='attendance_clock_out'),
]
