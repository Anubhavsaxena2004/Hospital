import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from ..models import Transaction, Bill, Department

logger = logging.getLogger(__name__)

from django.core.cache import cache
from django.db.models import Sum, Q
from datetime import datetime, timedelta

def financial_reports(request):
    cache_key = f'financial_reports_{request.user.id}'
    reports = cache.get(cache_key)
    
    if not reports:
        today = datetime.now().date()
        start_of_month = today.replace(day=1)
        start_of_year = today.replace(month=1, day=1)
        
        try:
            # Get basic financial metrics
            monthly = Bill.objects.filter(
                date_issued__gte=start_of_month
            ).aggregate(total=Sum('amount'))['total'] or 0
            
            yearly = Bill.objects.filter(
                date_issued__gte=start_of_year
            ).aggregate(total=Sum('amount'))['total'] or 0
            
            unpaid = Bill.objects.filter(
                status='pending'
            ).aggregate(total=Sum('amount'))['total'] or 0
            
            # Get top departments by revenue
            top_departments = Department.objects.annotate(
                revenue=Sum('patients__bill__amount')
            ).exclude(revenue=None).order_by('-revenue')[:5]
            
            reports = {
                'monthly': monthly,
                'yearly': yearly,
                'unpaid': unpaid,
                'top_departments': top_departments
            }
            cache.set(cache_key, reports, timeout=3600)  # Cache for 1 hour
            
        except Exception as e:
            logger.error(f"Error generating financial reports: {str(e)}")
            reports = {
                'monthly': 0,
                'yearly': 0,
                'unpaid': 0,
                'top_departments': [],
                'error': str(e)
            }
    
    return render(request, 'hospital/financial_reports.html', {
        'reports': reports,
        'last_updated': datetime.now()
    })

def transaction_list(request):
    transactions = Transaction.objects.all()
    return render(request, 'hospital/transaction_list.html', {'transactions': transactions})

def transaction_detail(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    return render(request, 'hospital/transaction_detail.html', {'transaction': transaction})

from ..forms import TransactionForm

def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.created_by = request.user
            transaction.save()
            
            # Send email receipt if transaction has a patient
            if transaction.patient:
                try:
                    patient_user = transaction.patient.user
                    subject = f'Transaction Receipt - {transaction.reference_number}'
                    html_message = render_to_string(
                        'emails/transaction_receipt.html',
                        {'transaction': transaction}
                    )
                    send_mail(
                        subject,
                        '',
                        settings.DEFAULT_FROM_EMAIL,
                        [patient_user.email],
                        html_message=html_message,
                        fail_silently=False
                    )
                    messages.success(request, 'Transaction created and receipt sent successfully')
                except Exception as e:
                    messages.warning(request, f'Transaction created but email failed: {str(e)}')
            else:
                messages.success(request, 'Transaction created successfully')
            
            return redirect('transaction_detail', pk=transaction.pk)
    else:
        form = TransactionForm()
    return render(request, 'hospital/transaction_form.html', {'form': form})

def transaction_edit(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transaction updated successfully')
            return redirect('transaction_detail', pk=transaction.pk)
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'hospital/transaction_form.html', {
        'form': form,
        'transaction': transaction
    })

def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        transaction.delete()
        messages.success(request, 'Transaction deleted successfully')
        return redirect('transaction_list')
    return render(request, 'hospital/transaction_confirm_delete.html', {'transaction': transaction})

from ..models import Patient
from ..forms import BillForm

def bill_create(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    if request.method == 'POST':
        form = BillForm(request.POST)
        if form.is_valid():
            bill = form.save(commit=False)
            bill.patient = patient
            bill.save()
            messages.success(request, 'Bill created successfully')
            return redirect('patient_detail', pk=patient.pk)
    else:
        form = BillForm(initial={'patient': patient})
    return render(request, 'hospital/bill_form.html', {
        'form': form,
        'patient': patient
    })

def bill_detail(request, pk):
    bill = get_object_or_404(Bill, pk=pk)
    return render(request, 'hospital/bill_detail.html', {'bill': bill})

from ..forms import DocumentForm

def document_upload(request, transaction_id):
    transaction = get_object_or_404(Transaction, pk=transaction_id)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.transaction = transaction
            if transaction.patient:
                document.patient = transaction.patient
            document.uploaded_by = request.user
            document.save()
            messages.success(request, 'Document uploaded successfully!')
            
            # Always redirect to transaction detail instead of patient detail
            return redirect('transaction_detail', pk=transaction.pk)
    else:
        form = DocumentForm()
    return render(request, 'hospital/document_upload.html', {
        'form': form,
        'transaction': transaction
    })
