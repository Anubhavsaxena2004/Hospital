from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from ..models import Appointment, Patient, Doctor

def appointment_list(request):
    appointments = Appointment.objects.select_related(
        'patient', 'doctor', 'department'
    ).order_by('-appointment_date', '-appointment_time')
    
    # Get filter parameters
    date = request.GET.get('date')
    status = request.GET.get('status')
    doctor_id = request.GET.get('doctor')
    
    # Apply filters
    if date:
        appointments = appointments.filter(appointment_date=date)
    if status:
        appointments = appointments.filter(status=status)
    if doctor_id:
        appointments = appointments.filter(doctor_id=doctor_id)
    
    # Get all doctors for filter dropdown
    doctors = Doctor.objects.all()
    
    return render(request, 'hospital/appointment_list.html', {
        'appointments': appointments,
        'doctors': doctors,
        'date': date,
        'status': status,
        'doctor_id': doctor_id
    })

from ..forms import AppointmentForm

def appointment_create(request):
    initial_data = {}
    patient_id = request.GET.get('patient_id')
    doctor_id = request.GET.get('doctor_id')
    
    if patient_id:
        try:
            initial_data['patient'] = Patient.objects.get(pk=patient_id)
        except Patient.DoesNotExist:
            messages.warning(request, 'Patient not found')
    
    if doctor_id:
        try:
            initial_data['doctor'] = Doctor.objects.get(pk=doctor_id)
        except Doctor.DoesNotExist:
            messages.warning(request, 'Doctor not found')

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            try:
                appointment = form.save()
                messages.success(request, 'Appointment created successfully')
                return redirect('appointment_detail', pk=appointment.pk)
            except Exception as e:
                messages.error(request, f'Error saving appointment: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = AppointmentForm(initial=initial_data)
    
    return render(request, 'hospital/appointment_form.html', {
        'form': form
    })

def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment.objects.select_related('patient', 'doctor'), pk=pk)
    return render(request, 'hospital/appointment_detail.html', {'appointment': appointment})

def appointment_update(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Appointment updated successfully')
            return redirect('appointment_detail', pk=appointment.pk)
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'hospital/appointment_form.html', {
        'form': form,
        'appointment': appointment
    })

def appointment_delete(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        appointment.delete()
        messages.success(request, 'Appointment deleted successfully')
        return redirect('appointment_list')
    return render(request, 'hospital/appointment_confirm_delete.html', {
        'appointment': appointment
    })
