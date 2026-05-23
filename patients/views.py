from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Patient
from accounts.decorators import role_required

#Find patient or all patients
@login_required
@role_required('DOCTOR', 'ADMIN', 'NURSE')
def patient_list(request):
    query = request.GET.get('q','')
    patients = Patient.objects.select_related('user').all()
    
    if query:
        patients = patients.filter(
            user__first_name__icontains=query
        ) | patients.filter(
            user__last_name__icontains=query
        )
    return render(request, 'patients/list.html', {
        'patients': patients,
        'query': query,
    })

#patients appointments and doctors
@login_required
@role_required('DOCTOR', 'NURSE', 'ADMIN')
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    appointments = patient.user.patient_appointments.select_related('doctor').order_by('-scheduled_at')[:5]
    return render(request, 'patients/detail.html', {
        'patient': patient,
        'appointments': appointments,
    })

