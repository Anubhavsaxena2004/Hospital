from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.urls import reverse
from django.db.models import Q
from ..models import MedicalRecord, Appointment, Patient
from ..forms import MedicalRecordForm

def medical_record_list(request):
    query = request.GET.get('q', '')
    records = MedicalRecord.objects.select_related(
        'patient',
        'doctor',
        'doctor__doctor_profile'
    )
    
    if query:
        records = records.filter(
            Q(patient__first_name__icontains=query) |
            Q(patient__last_name__icontains=query) |
            Q(diagnosis__icontains=query) |
            Q(treatment__icontains=query)
        )
    
    return render(request, 'hospital/medical_record_list.html', {
        'records': records,
        'search_query': query
    })

def medical_record_create(request):
    appointment_id = request.GET.get('appointment')
    patient_id = request.GET.get('patient')
    
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            try:
                record = form.save(commit=False)
                if appointment_id:
                    record.appointment = get_object_or_404(Appointment, pk=appointment_id)
                record.save()
                messages.success(request, 'Medical record created successfully')
                if appointment_id:
                    return redirect('appointment_detail', pk=appointment_id)
                elif patient_id:
                    return redirect('patient_detail', pk=patient_id)
                return redirect('medical_record_list')
            except Exception as e:
                messages.error(request, f'Error saving record: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below')
    
    initial = {}
    if appointment_id:
        appointment = get_object_or_404(Appointment, pk=appointment_id)
        initial = {
            'patient': appointment.patient,
            'doctor': appointment.doctor,
            'appointment': appointment
        }
    elif patient_id:
        patient = get_object_or_404(Patient, pk=patient_id)
        initial = {
            'patient': patient,
            'doctor': request.user  # Default to current user if doctor not specified
        }
        
    form = MedicalRecordForm(initial=initial)
    
    return render(request, 'hospital/medical_record_form.html', {
        'form': form,
        'appointment_id': appointment_id
    })

class MedicalRecordDetailView(DetailView):
    model = MedicalRecord
    template_name = 'hospital/medical_record_detail.html'
    context_object_name = 'record'
