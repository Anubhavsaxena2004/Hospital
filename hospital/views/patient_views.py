from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from ..models import Patient, MedicalRecord, Bill, Document

from django.core.paginator import Paginator

def patient_list(request):
    patients = Patient.objects.prefetch_related(
        'medicalrecord_set', 'bill_set'
    ).order_by('-created_at')
    
    paginator = Paginator(patients, 25)  # Show 25 patients per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'hospital/patient_list.html', {
        'page_obj': page_obj,
        'patients': page_obj.object_list  # Maintain backward compatibility
    })

from ..forms import PatientForm

def patient_create(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save()
            messages.success(request, 'Patient created successfully')
            return redirect('patient_detail', pk=patient.pk)
    else:
        form = PatientForm()
    return render(request, 'hospital/patient_form.html', {'form': form})

def patient_detail(request, pk):
    patient = get_object_or_404(
        Patient.objects.prefetch_related(
            'medicalrecord_set',
            'bill_set',
            'appointment_set',
            'document_set'
        ),
        pk=pk
    )
    return render(request, 'hospital/patient_detail.html', {
        'patient': patient
    })

def patient_edit(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, 'Patient updated successfully')
            return redirect('patient_detail', pk=patient.pk)
    else:
        form = PatientForm(instance=patient)
    return render(request, 'hospital/patient_form.html', {'form': form, 'patient': patient})

def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        patient.delete()
        messages.success(request, 'Patient deleted successfully')
        return redirect('patient_list')
    return render(request, 'hospital/patient_confirm_delete.html', {'patient': patient})

from ..forms import MedicalRecordForm

def add_medical_record(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.patient = patient
            record.save()
            messages.success(request, 'Medical record added successfully')
            return redirect('patient_detail', pk=patient.id)
    else:
        form = MedicalRecordForm(initial={'patient': patient})

    return render(request, 'hospital/medical_record_form.html', {
        'form': form,
        'patient': patient  # Pass patient to template
    })

from ..forms import BillForm

def add_bill(request, patient_id):
    try:
        # First validate the patient_id
        if not patient_id or not str(patient_id).isdigit():
            raise ValueError("Invalid patient ID")
            
        patient = get_object_or_404(Patient, pk=patient_id)
        
        if request.method == 'POST':
            form = BillForm(request.POST, patient_id=patient_id)
            if form.is_valid():
                bill = form.save(commit=False)
                bill.patient = patient  # Ensure patient is set
                bill.save()
                messages.success(request, 'Bill created successfully')
                return redirect('patient_detail', pk=patient_id)
        else:
            form = BillForm(initial={'patient': patient}, patient_id=patient_id)
            
    except Patient.DoesNotExist:
        messages.error(request, 'Patient not found')
        return redirect('patient_list')
    except ValueError as e:
        messages.error(request, str(e))
        return redirect('patient_list')
    except Exception as e:
        messages.error(request, f'Error processing bill: {str(e)}')
        # Fallback to patient_list if we can't get patient_id
        return redirect('patient_list')
    
    return render(request, 'hospital/bill_form.html', {
        'form': form,
        'patient': patient
    })

from ..forms import DocumentForm

def upload_document(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.patient = patient
            document.save()
            messages.success(request, 'Document uploaded successfully')
            return redirect('patient_detail', pk=patient_id)
    else:
        form = DocumentForm()
    return render(request, 'hospital/document_upload.html', {
        'form': form,
        'patient': patient
    })
