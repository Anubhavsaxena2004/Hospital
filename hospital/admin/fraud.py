from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Transaction
from ..ml_models.fraud_detection import FraudDetector
from ..views.transaction_actions import verify_transaction, flag_transaction

fraud_detector = FraudDetector()

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'amount', 'date', 'fraud_status', 'fraud_actions')
    list_filter = ('date', 'fraud_status')
    actions = ['mark_as_verified', 'mark_as_fraud']

    def fraud_status(self, obj):
        probability = fraud_detector.predict({
            'amount': obj.amount,
            'procedure_count': obj.procedures.count(),
            'time_since_last_claim': obj.get_time_since_last_claim(),
            'patient_age': obj.patient.age,
            'provider_avg_claim': obj.provider.average_claim_amount()
        })
        return f"{probability*100:.1f}%"

    def fraud_actions(self, obj):
        return format_html(
            '<a class="button" href="{}">Verify</a>&nbsp;'
            '<a class="button" href="{}">Flag</a>',
            reverse('admin:verify_transaction', args=[obj.pk]),
            reverse('admin:flag_transaction', args=[obj.pk])
        )
    fraud_actions.short_description = 'Actions'

    def mark_as_verified(self, request, queryset):
        queryset.update(fraud_status='verified')
    mark_as_verified.short_description = "Mark selected as verified"

    def mark_as_fraud(self, request, queryset):
        queryset.update(fraud_status='fraud')
    mark_as_fraud.short_description = "Mark selected as fraud"
