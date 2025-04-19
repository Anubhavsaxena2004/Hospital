from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.models import Group
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from .models import Patient, MedicalRecord, Appointment, Bill, Document, Bed, Doctor, Nurse, Admin, Transaction
from .forms import PatientForm, MedicalRecordForm, AppointmentForm, BillForm, DocumentForm, BedForm, TransactionForm,DoctorForm
from django.core.paginator import Paginator
from django.db.models import Sum
from datetime import datetime, timedelta
from django.db.models import Q
from django.db import transaction

@login_required
def dashboard(request):
    # Get basic statistics
    total_patients = Patient.objects.count()
    available_beds = Bed.objects.filter(status='available').count()
    today_appointments = Appointment.objects.filter(appointment_date=timezone.now().date()).count()
    pending_transactions = Transaction.objects.filter(status='pending').count()
    
    # Get recent activities
    recent_activities = []
    
    # Add patient activities
    patient_activities = Patient.objects.all().order_by('-created_at')[:5]
    for patient in patient_activities:
        recent_activities.append({
            'type': 'patient',
            'title': f'Patient {patient.first_name} {patient.last_name}',
            'description': f'Patient record {patient.status}',
            'date': patient.created_at,
            'user': patient.created_by if hasattr(patient, 'created_by') else None,
            'icon': 'user-injured',
            'color': 'primary'
        })
    
    # Add appointment activities
    appointment_activities = Appointment.objects.all().order_by('-created_at')[:5]
    for appointment in appointment_activities:
        recent_activities.append({
            'type': 'appointment',
            'title': f'Appointment for {appointment.patient.first_name} {appointment.patient.last_name}',
            'description': f'Appointment {appointment.status} with Dr. {appointment.doctor.user.first_name}',
            'date': appointment.created_at,
            'user': appointment.created_by if hasattr(appointment, 'created_by') else None,
            'icon': 'calendar-check',
            'color': 'success'
        })
    
    # Add transaction activities
    transaction_activities = Transaction.objects.all().order_by('-created_at')[:5]
    for transaction in transaction_activities:
        recent_activities.append({
            'type': 'transaction',
            'title': f'Transaction {transaction.reference_number}',
            'description': f'{transaction.get_type_display()} of ${transaction.amount} - {transaction.get_status_display()}',
            'date': transaction.created_at,
            'user': transaction.created_by,
            'icon': 'money-bill-wave',
            'color': 'warning'
        })
    
    # Add medical record activities
    medical_record_activities = MedicalRecord.objects.all().order_by('-created_at')[:5]
    for record in medical_record_activities:
        recent_activities.append({
            'type': 'medical_record',
            'title': f'Medical Record for {record.patient.first_name} {record.patient.last_name}',
            'description': f'Treatment record updated',
            'date': record.created_at,
            'user': record.created_by if hasattr(record, 'created_by') else None,
            'icon': 'file-medical',
            'color': 'info'
        })
    
    # Sort all activities by date
    recent_activities.sort(key=lambda x: x['date'], reverse=True)
    
    # Get recent transactions
    recent_transactions = Transaction.objects.all().order_by('-created_at')[:5]
    
    # Get patient admission data for chart
    patient_admissions_data = [65, 59, 80, 81, 56, 55, 40, 65, 59, 80, 81, 56]  # Placeholder data
    
    # Get revenue and expenses data for chart
    revenue_data = [12000, 19000, 15000, 17000, 22000, 20000, 25000, 22000, 30000, 28000, 32000, 35000]  # Placeholder data
    expenses_data = [8000, 12000, 10000, 11000, 15000, 13000, 18000, 16000, 20000, 19000, 22000, 24000]  # Placeholder data
    
    context = {
        'total_patients': total_patients,
        'available_beds': available_beds,
        'today_appointments': today_appointments,
        'pending_transactions': pending_transactions,
        'recent_activities': recent_activities[:5],  # Limit to 5 most recent
        'recent_transactions': recent_transactions,
        'patient_admissions_data': patient_admissions_data,
        'revenue_data': revenue_data,
        'expenses_data': expenses_data,
    }
    
    return render(request, 'hospital/dashboard.html', context)

@login_required
def patient_list(request):
    import logging
    logger = logging.getLogger(__name__)
    
    patients = Patient.objects.all()
    logger.debug(f"Initial patient queryset: {patients.query}")
    
    # Apply search filter
    search_query = request.GET.get('search')
    if search_query:
        patients = patients.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(phone_number__icontains=search_query)
        )
        logger.debug(f"After search filter: {patients.query}")
    
    # Apply status filter
    status_filter = request.GET.get('status')
    if status_filter:
        patients = patients.filter(status=status_filter)
        logger.debug(f"After status filter: {patients.query}")
    
    # Apply blood group filter
    blood_group_filter = request.GET.get('blood_group')
    if blood_group_filter:
        patients = patients.filter(blood_group=blood_group_filter)
        logger.debug(f"After blood group filter: {patients.query}")
    
    # Pagination
    paginator = Paginator(patients, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    logger.debug(f"Final patient count: {patients.count()}")
    logger.debug(f"First 5 patients: {list(patients[:5].values())}")
    
    context = {
        'page_obj': page_obj,
        'patients': page_obj.object_list  # For backward compatibility
    }
    return render(request, 'hospital/patient_list.html', context)

@login_required
def patient_create(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Patient created successfully.')
            return redirect('patient_list')
    else:
        form = PatientForm()
    return render(request, 'hospital/patient_form.html', {'form': form})

@login_required
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    medical_records = MedicalRecord.objects.filter(patient=patient)
    appointments = Appointment.objects.filter(patient=patient)
    bills = Bill.objects.filter(patient=patient)
    documents = Document.objects.filter(patient=patient)
    doctors = Doctor.objects.all()
    
    context = {
        'patient': patient,
        'medical_records': medical_records,
        'appointments': appointments,
        'bills': bills,
        'documents': documents,
        'doctors': doctors,
    }
    return render(request, 'hospital/patient_detail.html', context)

@login_required
def patient_edit(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, 'Patient updated successfully.')
            return redirect('patient_detail', pk=patient.pk)
    else:
        form = PatientForm(instance=patient)
    return render(request, 'hospital/patient_form.html', {'form': form, 'patient': patient})

@login_required
def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        patient.delete()
        messages.success(request, 'Patient deleted successfully.')
        return redirect('patient_list')
    return render(request, 'hospital/patient_confirm_delete.html', {'patient': patient})

@login_required
def add_medical_record(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            medical_record = form.save(commit=False)
            medical_record.patient = patient
            medical_record.save()
            messages.success(request, 'Medical record added successfully.')
            return redirect('patient_detail', pk=patient_id)
    else:
        form = MedicalRecordForm()
    return render(request, 'hospital/medical_record_form.html', {'form': form, 'patient': patient})

@login_required
def appointment_list(request):
    appointments = Appointment.objects.all()
    return render(request, 'hospital/appointment_list.html', {'appointments': appointments})

@login_required
def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Appointment created successfully.')
            return redirect('appointment_list')
    else:
        form = AppointmentForm()
    return render(request, 'hospital/appointment_form.html', {'form': form})

@login_required
def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    return render(request, 'hospital/appointment_detail.html', {'appointment': appointment})

@login_required
def appointment_update(request, pk):
    import logging
    from django.conf import settings
    
    logger = logging.getLogger(__name__)
    appointment = get_object_or_404(Appointment, pk=pk)
    
    # Permission constants
    PERMISSION_DENIED_MSG = 'You do not have permission to edit this appointment.'
    PAST_DATE_MSG = 'Appointment date cannot be in the past.'
    DOCTOR_UNAVAILABLE_MSG = 'The selected doctor is not available at this time.'
    PATIENT_CONFLICT_MSG = 'The patient already has an appointment at this time.'
    UPDATE_SUCCESS_MSG = 'Appointment updated successfully.'
    UPDATE_ERROR_MSG = 'An error occurred while updating the appointment.'
    
    # Check permissions
    if not request.user.is_staff and appointment.created_by != request.user:
        messages.error(request, PERMISSION_DENIED_MSG)
        logger.warning(f"Unauthorized edit attempt by {request.user} on appointment {pk}")
        return redirect('appointment_list')
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            try:
                new_date = form.cleaned_data['appointment_date']
                new_time = form.cleaned_data['appointment_time']
                doctor = form.cleaned_data['doctor']
                patient = form.cleaned_data['patient']
                
                # Validate appointment date is not in the past
                if new_date < timezone.now().date():
                    messages.error(request, PAST_DATE_MSG)
                    logger.warning(f"Past date attempt for appointment {pk}")
                    return render(request, 'hospital/appointment_form.html', {
                        'form': form,
                        'appointment': appointment,
                        'now': timezone.now(),
                        'doctors': Doctor.objects.all()
                    })
                
                # Check doctor availability
                conflicting_doctor_appts = Appointment.objects.filter(
                    doctor=doctor,
                    appointment_date=new_date,
                    appointment_time=new_time
                ).exclude(pk=pk)
                
                if conflicting_doctor_appts.exists():
                    messages.error(request, DOCTOR_UNAVAILABLE_MSG)
                    logger.warning(f"Doctor conflict for appointment {pk}")
                    return render(request, 'hospital/appointment_form.html', {
                        'form': form,
                        'appointment': appointment,
                        'now': timezone.now(),
                        'doctors': Doctor.objects.all()
                    })
                
                # Check patient appointment conflicts
                conflicting_patient_appts = Appointment.objects.filter(
                    patient=patient,
                    appointment_date=new_date,
                    appointment_time=new_time
                ).exclude(pk=pk)
                
                if conflicting_patient_appts.exists():
                    messages.error(request, PATIENT_CONFLICT_MSG)
                    logger.warning(f"Patient conflict for appointment {pk}")
                    return render(request, 'hospital/appointment_form.html', {
                        'form': form,
                        'appointment': appointment,
                        'now': timezone.now(),
                        'doctors': Doctor.objects.all()
                    })
                
                # Save with updated_by tracking
                appointment = form.save(commit=False)
                appointment.updated_by = request.user
                appointment.save()
                
                logger.info(
                    f"Appointment {appointment.id} updated by {request.user.username}. "
                    f"Details - Patient: {appointment.patient}, Doctor: {appointment.doctor}, "
                    f"Date: {appointment.appointment_date}, Time: {appointment.appointment_time}"
                )
                messages.success(request, UPDATE_SUCCESS_MSG)
                return redirect('appointment_detail', pk=appointment.pk)
                
            except Exception as e:
                logger.error(
                    f"Error updating appointment {pk}: {str(e)}",
                    exc_info=settings.DEBUG
                )
                messages.error(request, UPDATE_ERROR_MSG)
                return render(request, 'hospital/appointment_form.html', {
                    'form': form,
                    'appointment': appointment,
                    'now': timezone.now(),
                    'doctors': Doctor.objects.all()
                })
    else:
        form = AppointmentForm(instance=appointment)
        
    return render(request, 'hospital/appointment_form.html', {
        'form': form,
        'appointment': appointment,
        'now': timezone.now(),
        'doctors': Doctor.objects.all()
    })

@login_required
def add_bill(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    if request.method == 'POST':
        form = BillForm(request.POST)
        if form.is_valid():
            bill = form.save(commit=False)
            bill.patient = patient
            bill.save()
            messages.success(request, 'Bill added successfully.')
            return redirect('patient_detail', pk=patient_id)
    else:
        form = BillForm()
    return render(request, 'hospital/add_bill.html', {'form': form, 'patient': patient})

@login_required
def bill_detail(request, pk):
    bill = get_object_or_404(Bill, pk=pk)
    return render(request, 'hospital/bill_detail.html', {'bill': bill})

@login_required
def upload_document(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.patient = patient
            document.save()
            messages.success(request, 'Document uploaded successfully.')
            return redirect('patient_detail', pk=patient_id)
    else:
        form = DocumentForm()
    return render(request, 'hospital/upload_document.html', {'form': form, 'patient': patient})

@login_required
def bed_list(request):
    beds = Bed.objects.all()
    return render(request, 'hospital/bed_list.html', {'beds': beds})

@login_required
def bed_detail(request, pk):
    bed = get_object_or_404(Bed, pk=pk)
    return render(request, 'hospital/bed_detail.html', {'bed': bed})

@login_required
def bed_create(request):
    if request.method == 'POST':
        form = BedForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bed created successfully.')
            return redirect('bed_list')
    else:
        form = BedForm()
    return render(request, 'hospital/bed_form.html', {'form': form})

@login_required
def bed_edit(request, pk):
    bed = get_object_or_404(Bed, pk=pk)
    if request.method == 'POST':
        form = BedForm(request.POST, instance=bed)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bed updated successfully.')
            return redirect('bed_detail', pk=bed.pk)
    else:
        form = BedForm(instance=bed)
    return render(request, 'hospital/bed_form.html', {'form': form, 'bed': bed})

@login_required
def bed_delete(request, pk):
    bed = get_object_or_404(Bed, pk=pk)
    if request.method == 'POST':
        bed.delete()
        messages.success(request, 'Bed deleted successfully.')
        return redirect('bed_list')
    return render(request, 'hospital/bed_confirm_delete.html', {'bed': bed})

def register(request):
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        is_doctor = request.POST.get('role') == 'DOCTOR'
        
        if user_form.is_valid():
            user = user_form.save(commit=False)
            
            # Handle doctor registration
            if is_doctor:
                try:
                    with transaction.atomic():
                        # Save user with staff privileges and doctor data
                        user.is_staff = True
                        user.phone_number = request.POST.get('phone_number')
                        user.address = request.POST.get('address')
                        user.specialization = request.POST.get('specialization')
                        user.save()
                        
                        # Create doctor profile using data from both forms
                        doctor = Doctor(
                            user=user,
                            specialization=user.specialization,
                            phone_number=user.phone_number,
                            address=user.address,
                            medical_license=request.POST.get('medical_license'),
                            years_of_experience=request.POST.get('years_experience')
                        )
                        doctor.save()
                        
                        # Add user to doctors group
                        doctors_group, created = Group.objects.get_or_create(name='Doctors')
                        user.groups.add(doctors_group)
                        
                        messages.success(request, 'Doctor registration successful!')
                        login(request, user)
                        return redirect('dashboard')
                except Exception as e:
                    messages.error(request, f'Doctor registration failed: {str(e)}')
                    return render(request, 'registration/register.html', {
                        'form': user_form,
                        'is_doctor': True
                    })
            else:
                # Regular user registration
                try:
                    user.save()
                    messages.success(request, 'Registration successful!')
                    login(request, user)
                    return redirect('dashboard')
                except Exception as e:
                    messages.error(request, f'Registration failed: {str(e)}')
                    return render(request, 'registration/register.html', {
                        'form': user_form,
                        'is_doctor': False
                    })
    else:
        user_form = RegistrationForm()
    
    return render(request, 'registration/register.html', {
        'form': user_form,
        'is_doctor': False
    })

@login_required
def financial_reports(request):
    # Get filter parameters
    report_type = request.GET.get('report_type', 'revenue')
    date_range = request.GET.get('date_range', 'this_month')
    department = request.GET.get('department', '')

    # Calculate date range
    today = timezone.now().date()
    if date_range == 'today':
        start_date = today
        end_date = today
    elif date_range == 'yesterday':
        start_date = today - timedelta(days=1)
        end_date = start_date
    elif date_range == 'this_week':
        start_date = today - timedelta(days=today.weekday())
        end_date = today
    elif date_range == 'last_week':
        start_date = today - timedelta(days=today.weekday() + 7)
        end_date = start_date + timedelta(days=6)
    elif date_range == 'this_month':
        start_date = today.replace(day=1)
        end_date = today
    elif date_range == 'last_month':
        start_date = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
        end_date = today.replace(day=1) - timedelta(days=1)
    elif date_range == 'this_quarter':
        quarter_start = ((today.month - 1) // 3) * 3 + 1
        start_date = today.replace(month=quarter_start, day=1)
        end_date = today
    elif date_range == 'this_year':
        start_date = today.replace(month=1, day=1)
        end_date = today
    else:
        start_date = today - timedelta(days=30)
        end_date = today

    # Get transactions based on filters
    transactions = Transaction.objects.filter(
        date__range=[start_date, end_date]
    )
    if department:
        transactions = transactions.filter(department=department)

    # Calculate summary statistics
    total_revenue = transactions.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = transactions.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    net_profit = total_revenue - total_expenses
    pending_payments = transactions.filter(status='pending').aggregate(Sum('amount'))['amount__sum'] or 0

    # Paginate transactions
    paginator = Paginator(transactions.order_by('-date'), 10)
    page = request.GET.get('page')
    transactions = paginator.get_page(page)

    context = {
        'total_revenue': total_revenue,
        'total_expenses': total_expenses,
        'net_profit': net_profit,
        'pending_payments': pending_payments,
        'transactions': transactions,
        'report_type': report_type,
        'date_range': date_range,
        'department': department,
        'start_date': start_date,
        'end_date': end_date,
    }

    return render(request, 'hospital/financial_reports.html', context)

@login_required
def transaction_list(request):
    """View for listing all financial transactions with filtering and pagination."""
    # Get filter parameters
    transaction_type = request.GET.get('type', '')
    status = request.GET.get('status', '')
    department = request.GET.get('department', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    search_query = request.GET.get('q', '')

    # Start with all transactions
    transactions = Transaction.objects.all()

    # Apply filters
    if transaction_type:
        transactions = transactions.filter(type=transaction_type)
    if status:
        transactions = transactions.filter(status=status)
    if department:
        transactions = transactions.filter(department=department)
    if date_from:
        transactions = transactions.filter(date__gte=date_from)
    if date_to:
        transactions = transactions.filter(date__lte=date_to)
    if search_query:
        transactions = transactions.filter(
            Q(description__icontains=search_query) |
            Q(reference_number__icontains=search_query)
        )

    # Paginate results
    paginator = Paginator(transactions.order_by('-date'), 10)
    page = request.GET.get('page')
    transactions = paginator.get_page(page)

    context = {
        'transactions': transactions,
        'transaction_types': Transaction.TRANSACTION_TYPES,
        'status_choices': Transaction.STATUS_CHOICES,
        'department_choices': Transaction.DEPARTMENT_CHOICES,
        'filter_type': transaction_type,
        'filter_status': status,
        'filter_department': department,
        'filter_date_from': date_from,
        'filter_date_to': date_to,
        'search_query': search_query,
    }

    return render(request, 'hospital/transaction_list.html', context)

@login_required
def transaction_detail(request, pk):
    """View for displaying detailed information about a specific transaction."""
    transaction = get_object_or_404(Transaction, pk=pk)
    
    context = {
        'transaction': transaction,
    }
    
    return render(request, 'hospital/transaction_detail.html', context)

@login_required
def transaction_create(request):
    """View for creating a new financial transaction."""
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.created_by = request.user
            transaction.save()
            messages.success(request, 'Transaction created successfully.')
            return redirect('transaction_detail', pk=transaction.pk)
    else:
        form = TransactionForm()
    
    context = {
        'form': form,
        'title': 'New Transaction',
        'button_text': 'Create Transaction',
    }
    
    return render(request, 'hospital/transaction_form.html', context)

@login_required
def transaction_edit(request, pk):
    """View for editing an existing financial transaction."""
    transaction = get_object_or_404(Transaction, pk=pk)
    
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transaction updated successfully.')
            return redirect('transaction_detail', pk=transaction.pk)
    else:
        form = TransactionForm(instance=transaction)
    
    context = {
        'form': form,
        'transaction': transaction,
        'title': 'Edit Transaction',
        'button_text': 'Update Transaction',
    }
    
    return render(request, 'hospital/transaction_form.html', context)

@login_required
def transaction_delete(request, pk):
    """View for confirming and deleting a financial transaction."""
    transaction = get_object_or_404(Transaction, pk=pk)
    
    if request.method == 'POST':
        transaction.delete()
        messages.success(request, 'Transaction deleted successfully.')
        return redirect('transaction_list')
    
    context = {
        'transaction': transaction,
    }
    
    return render(request, 'hospital/transaction_confirm_delete.html', context)

@login_required
def history(request):
    """View for displaying system history and activities."""
    # Get filter parameters
    activity_type = request.GET.get('type', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    user = request.GET.get('user', '')
    
    # Start with all activities
    activities = []
    
    # Add patient activities
    patient_activities = Patient.objects.all().order_by('-updated_at')
    for patient in patient_activities:
        activities.append({
            'type': 'patient',
            'title': f'Patient {patient.first_name} {patient.last_name}',
            'description': f'Patient record {patient.status}',
            'date': patient.updated_at,
            'user': patient.created_by if hasattr(patient, 'created_by') else None,
            'icon': 'user-injured',
            'color': patient.status_color
        })
    
    # Add appointment activities
    appointment_activities = Appointment.objects.all().order_by('-updated_at')
    for appointment in appointment_activities:
        activities.append({
            'type': 'appointment',
            'title': f'Appointment for {appointment.patient.first_name} {appointment.patient.last_name}',
            'description': f'Appointment {appointment.status} with Dr. {appointment.doctor.user.first_name}',
            'date': appointment.updated_at,
            'user': appointment.created_by if hasattr(appointment, 'created_by') else None,
            'icon': 'calendar-check',
            'color': appointment.status_color
        })
    
    # Add transaction activities
    transaction_activities = Transaction.objects.all().order_by('-updated_at')
    for transaction in transaction_activities:
        activities.append({
            'type': 'transaction',
            'title': f'Transaction {transaction.reference_number}',
            'description': f'{transaction.get_type_display()} of ${transaction.amount} - {transaction.get_status_display()}',
            'date': transaction.updated_at,
            'user': transaction.created_by,
            'icon': 'money-bill-wave',
            'color': transaction.status_color
        })
    
    # Add medical record activities
    medical_record_activities = MedicalRecord.objects.all().order_by('-updated_at')
    for record in medical_record_activities:
        activities.append({
            'type': 'medical_record',
            'title': f'Medical Record for {record.patient.first_name} {record.patient.last_name}',
            'description': f'Treatment record updated',
            'date': record.updated_at,
            'user': record.created_by if hasattr(record, 'created_by') else None,
            'icon': 'file-medical',
            'color': 'primary'
        })
    
    # Sort all activities by date
    activities.sort(key=lambda x: x['date'], reverse=True)
    
    # Apply filters
    if activity_type:
        activities = [a for a in activities if a['type'] == activity_type]
    if date_from:
        activities = [a for a in activities if a['date'].date() >= datetime.strptime(date_from, '%Y-%m-%d').date()]
    if date_to:
        activities = [a for a in activities if a['date'].date() <= datetime.strptime(date_to, '%Y-%m-%d').date()]
    if user:
        activities = [a for a in activities if a['user'] and a['user'].username == user]
    
    # Paginate results
    paginator = Paginator(activities, 20)
    page = request.GET.get('page')
    activities = paginator.get_page(page)
    
    context = {
        'activities': activities,
        'activity_types': [
            ('patient', 'Patient'),
            ('appointment', 'Appointment'),
            ('transaction', 'Transaction'),
            ('medical_record', 'Medical Record'),
        ],
        'filter_type': activity_type,
        'filter_date_from': date_from,
        'filter_date_to': date_to,
        'filter_user': user,
    }
    
    return render(request, 'hospital/history.html', context)

@login_required
def medical_record_list(request):
    # Get filter parameters
    activity_type = request.GET.get('type', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    user = request.GET.get('user', '')

    # Get all medical records
    records = MedicalRecord.objects.all().select_related('patient', 'doctor')

    # Apply filters
    if activity_type:
        # Since there's no record_type field, we'll filter by diagnosis or treatment
        records = records.filter(diagnosis__icontains=activity_type)
    if start_date:
        records = records.filter(created_at__gte=start_date)
    if end_date:
        records = records.filter(created_at__lte=end_date)
    if user:
        records = records.filter(doctor__username__icontains=user)

    # Sort by date
    records = records.order_by('-created_at')

    # Paginate results
    paginator = Paginator(records, 10)
    page = request.GET.get('page')
    records = paginator.get_page(page)

    # Define record types for the filter dropdown
    record_types = [
        ('general', 'General'),
        ('emergency', 'Emergency'),
        ('follow_up', 'Follow-up'),
        ('consultation', 'Consultation'),
        ('surgery', 'Surgery'),
    ]

    # Get all patients for the dropdown
    patients = Patient.objects.all().order_by('first_name', 'last_name')

    context = {
        'records': records,
        'record_types': record_types,
        'activity_type': activity_type,
        'start_date': start_date,
        'end_date': end_date,
        'user': user,
        'patients': patients,
    }

    return render(request, 'hospital/medical_record_list.html', context) 