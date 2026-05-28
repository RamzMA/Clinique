from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

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
    from patients.models import Patient
    from appointments.models import Appointment
    from accounts.models import User

    role = request.user.role
    today = timezone.now().date()
    context = {'user': request.user}

    if role == 'DOCTOR':
        context.update({
            'patient_count': Patient.objects.count(),
            'upcoming_appointments': Appointment.objects.filter(
                doctor = request.user,
                scheduled_at__gte=timezone.now()
            ).select_related('patient').order_by('scheduled_at')[:5],
            'today_appointments': Appointment.objects.filter(
                doctor = request.user,
                scheduled_at__gte = today
            ).count(),
            'pending_count': Appointment.objects.filter(
                doctor = request.user,
                status = 'PENDING'
            ).count(),
            'recent_patients': Patient.objects.select_related('user').order_by('-created_at')[:5],
        })
    elif role == 'NURSE':
        context.update({
            'patient_count': Patient.objects.count(),
            'today_appointments': Appointment.objects.filter(
                scheduled_at__date = today
            ).count(),
        })
    elif role == 'PATIENT':
        appts = Appointment.objects.filter(
            patient=request.user
        ).select_related('doctor').order_by('-scheduled_at')

        context.update({
            'appointments': appts,
            'appointment_count': appts.count(),
            'next_appointment': appts.filter(
                scheduled_at__gte=timezone.now(),
                status='CONFIRMED'
            ).order_by('scheduled_at').first(),
        })
    elif role == 'ADMIN':
        context.update({
            'user_count': User.objects.count(),
            'patient_count': Patient.objects.count(),
            'doctor_count': User.objects.filter(role='DOCTOR').count(),
            'nurse_count': User.objects.filter(role='NURSE').count(),
        })
        
    templates = {
        'ADMIN': 'dashboard/admin.html',
        'DOCTOR': 'dashboard/doctor.html',
        'NURSE': 'dashboard/nurse.html',
        'PATIENT': 'dashboard/patient.html',
    }

    template = templates.get(role, 'dashboard/patient.html')
    return render(request, template, context)