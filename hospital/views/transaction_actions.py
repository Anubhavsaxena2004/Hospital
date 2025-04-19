from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from ..models import Transaction

def verify_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    transaction.fraud_status = 'verified'
    transaction.verified_by = request.user
    transaction.save()
    messages.success(request, f'Transaction #{pk} has been verified')
    return redirect('admin:hospital_transaction_changelist')

def flag_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    transaction.fraud_status = 'fraud'
    transaction.verified_by = request.user
    transaction.save()
    messages.warning(request, f'Transaction #{pk} has been flagged as potential fraud')
    return redirect('admin:hospital_transaction_changelist')
