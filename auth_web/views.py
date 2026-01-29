from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages


def login_view(request):
    if request.method == 'POST':
        npp = request.POST.get('npp')
        password = request.POST.get('password')

        user = authenticate(request, npp=npp, password=password)

        if user is not None:
            login(request, user)

            # redirect berdasarkan role
            if user.groups.filter(name='direktur').exists():
                return redirect('/direktur/')
            elif user.groups.filter(name='manager').exists():
                return redirect('/manager/')
            elif user.groups.filter(name='asisten_manager').exists():
                return redirect('/asisten-manager/')
            elif user.groups.filter(name='leader').exists():
                return redirect('/leader/')
            elif user.groups.filter(name='karyawan').exists():
                return redirect('/karyawan/')

            return redirect('/')

        messages.error(request, 'NPP atau password salah')

    return render(request, 'auth/login.html')
