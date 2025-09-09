from django.shortcuts import render # type: ignore

def login_view(request):
    return render(request, 'login.html')

def dashboard_view(request):
    return render(request, 'base_dashboard.html')
