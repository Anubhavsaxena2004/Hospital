from django.shortcuts import render, redirect, get_object_or_404, Http404
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone
from core.forms import UserRegistrationForm
from django.db.models import Count, Sum, Q
from django.contrib.admin.models import LogEntry
from ..models import (
    MedicalRecord, Patient, Appointment, Department,
    Bill, Bed, Doctor, Transaction, MaintenanceRecord
)

def dashboard(request):
    # Get quick stats
    total_patients = Patient.objects.count()
    available_beds = Bed.objects.filter(status='available').count()
    today_appointments = Appointment.objects.filter(
        appointment_date=timezone.now().date()
    ).count()
    active_staff = Doctor.objects.count()  # Or use your staff model
    
    def get_recent_activities():
        """Combine recent activities from multiple models"""
        from itertools import chain
        from operator import attrgetter
        
        # Get recent records from different models
        recent_appointments = Appointment.objects.order_by('-created_at')[:5]
        recent_transactions = Transaction.objects.order_by('-date')[:5]
        recent_maintenance = MaintenanceRecord.objects.order_by('-created_at')[:5]
        
        # Format as activity objects
        activities = []
        
        for appt in recent_appointments:
            activities.append({
                'type': 'appointment',
                'id': appt.id,
                'color': getattr(appt, 'status_color', 'primary'),  # Default to 'primary' if status_color missing
                'icon': 'calendar-check',
                'title': f"Appointment for {appt.patient}",
                'subtitle': f"With Dr. {appt.doctor}",
                'status': appt.get_status_display(),
                'date': appt.created_at,
                'url': f"/appointments/{appt.id}"
            })
            
        for tx in recent_transactions:
            activities.append({
                'type': 'transaction', 
                'id': tx.id,
                'color': getattr(tx, 'status_color', 'primary'),  # Default to 'primary' if status_color missing
                'icon': 'money-bill-wave',
                'title': f"{getattr(tx, 'get_type_display', lambda: 'Transaction')()}",
                'subtitle': f"{getattr(tx, 'category', '')}",
                'amount': getattr(tx, 'amount', 0),
                'date': getattr(tx, 'date', timezone.now()),
                'url': f"/transactions/{tx.id}"
            })
            
        for maint in recent_maintenance:
            activities.append({
                'type': 'maintenance',
                'id': maint.id,
                'color': getattr(maint, 'status_color', 'warning'),  # Default to 'warning' if status_color missing
                'icon': 'tools',
                'title': f"Maintenance for Bed {getattr(maint, 'bed.number', '')}",
                'subtitle': getattr(maint, 'title', ''),
                'status': getattr(maint, 'get_status_display', lambda: '')(),
                'date': getattr(maint, 'created_at', timezone.now()),
                'url': f"/maintenance/{maint.id}"
            })
            
        # Sort combined activities by date and limit to 10
        activities.sort(key=lambda x: x['date'], reverse=True)
        return activities[:10]
        
    recent_activities = get_recent_activities()
    
    # Get recent patients (last 5)
    recent_patients = Patient.objects.order_by('-created_at')[:5]
    
    # Get today's appointments
    today_appointments_list = Appointment.objects.filter(
        appointment_date=timezone.now().date()
    ).order_by('appointment_time')[:10]
    
    return render(request, 'hospital/dashboard.html', {
        'total_patients': total_patients,
        'available_beds': available_beds,
        'today_appointments': today_appointments,
        'active_staff': active_staff,
        'recent_activities': recent_activities,
        'recent_patients': recent_patients,
        'today_appointments_list': today_appointments_list
    })

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def history(request):
    # Basic history view placeholder
    return render(request, 'hospital/history.html')

def test_bill_view(request):
    """Test view to verify Bill model fields"""
    from ..models import Bill
    try:
        bill = Bill.objects.create(
            patient_id=1,  # Assuming patient with ID 1 exists
            amount=100.00,
            description='Test bill',
            date_paid=timezone.now().date()
        )
        return JsonResponse({
            'success': True,
            'message': 'Bill created successfully with date_paid',
            'date_paid': str(bill.date_paid)
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

def medical_record_list(request):
    # Add search and filtering functionality
    query = request.GET.get('q', '')
    records = MedicalRecord.objects.all()
    patients = Patient.objects.all()  # Get all patients for the modal
    
    if query:
        records = records.filter(
            Q(patient__name__icontains=query) |
            Q(diagnosis__icontains=query) |
            Q(treatment__icontains=query)
        )
    
    return render(request, 'hospital/medical_record_list.html', {
        'records': records,
        'patients': patients,  # Add patients to context
        'search_query': query
    })

def patient_search(request):
    # Comprehensive patient search
    if request.method == 'GET':
        query = request.GET.get('q', '')
        patients = Patient.objects.all()
        
        if query:
            patients = patients.filter(
                Q(name__icontains=query) |
                Q(medical_number__icontains=query) |
                Q(phone__icontains=query)
            )
        
        return render(request, 'hospital/patient_search.html', {
            'patients': patients,
            'search_query': query
        })
    return redirect('dashboard')

def appointment_list(request):
    # View and manage appointments
    appointments = Appointment.objects.select_related('patient', 'doctor').order_by('-date')
    status_filter = request.GET.get('status', None)
    
    if status_filter:
        appointments = appointments.filter(status=status_filter)
    
    return render(request, 'hospital/appointment_list.html', {
        'appointments': appointments,
        'status_filter': status_filter
    })

def medical_record_detail(request, pk):
    # Detailed medical record view with null checks
    record = get_object_or_404(
        MedicalRecord.objects.select_related('patient', 'doctor'), 
        pk=pk
    )
    
    if not record.patient:
        raise Http404("Patient record not found")
        
    context = {
        'medical_record': record,
        'patient': record.patient,
        'doctor': record.doctor
    }
    
    # Add debug info in development
    if settings.DEBUG:
        context['debug_info'] = {
            'patient_exists': bool(record.patient),
            'patient_id': record.patient.id if record.patient else None,
            'patient_name': f"{record.patient.first_name} {record.patient.last_name}" if record.patient else None
        }
    
    return render(request, 'hospital/medical_record_detail.html', context)

def patient_search_api(request):
    """API endpoint for patient autocomplete search"""
    query = request.GET.get('search', '')
    patients = Patient.objects.filter(
        Q(first_name__icontains=query) | 
        Q(last_name__icontains=query) |
        Q(id__icontains=query)
    )[:10].values('id', 'first_name', 'last_name')
    
    return JsonResponse(list(patients), safe=False)
