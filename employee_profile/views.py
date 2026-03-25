from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import EmployeeProfile
from .forms import EmployeeProfileForm

@login_required
def my_profile(request):
    employee = request.user.employee
    profile, created = EmployeeProfile.objects.get_or_create(
        employee=employee
    )

    context = {
        'employee': employee,
        'profile': profile
    }
    return render(request, 'profile/my_profile.html', context)


@login_required
def edit_profile(request):
    employee = request.user.employee
    profile, created = EmployeeProfile.objects.get_or_create(
        employee=employee
    )

    if request.method == 'POST':
        form = EmployeeProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('my_profile')
    else:
        form = EmployeeProfileForm(instance=profile)

    return render(request, 'profile/edit_profile.html', {'form': form})
