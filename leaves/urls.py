from django.urls import path
from . import views

urlpatterns = [
    path('management/', views.leave_management_list, name='leave_management_list'),
    path('management/<int:pk>/approve/', views.leave_approve, name='leave_approve'),
    path('management/<int:pk>/reject/', views.leave_reject, name='leave_reject'),
    
    path('balances/', views.leave_balance_list, name='leave_balance_list'),
    path('balances/create/', views.leave_balance_create, name='leave_balance_create'),
    path('balances/<int:pk>/edit/', views.leave_balance_edit, name='leave_balance_edit'),
    path('balances/<int:pk>/delete/', views.leave_balance_delete, name='leave_balance_delete'),
    path('balances/reset-all/', views.leave_balance_reset_all, name='leave_balance_reset_all'),

    # --- Self Service (Employee Side) ---
    path('history/', views.leave_history, name='leave_history'),
    path('apply/', views.leave_apply, name='leave_apply'),
]
