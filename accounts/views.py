from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        user = authenticate(
            request,
            username = request.POST['username'],
            password = request.POST['password']
        )
        if user:
            login(request,user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/login.html', {'form': True})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    role = request.user.role
    templates = {
        'ADMIN': 'dashboard/admin.html',
        'DOCTOR': 'dashboard/doctor.html',
        'NURSE': 'dashboard/nurse.html',
        'PATIENT': 'dashboard/patient.html',
    }
    template = templates.get(role, 'dashboard/patient.html')
    return render(request, template, {'user': request.user})