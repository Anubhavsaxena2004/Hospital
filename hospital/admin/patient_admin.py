from django.contrib import admin
from hospital.models import Patient, Admission, Document

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'age', 'status', 'readmission_risk_level')
    list_filter = ('status', 'readmission_risk_level')
    search_fields = ('first_name', 'last_name')
    readonly_fields = ('readmission_risk_score', 'readmission_risk_level')
    fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name', 'date_of_birth')
        }),
        ('Medical Info', {
            'fields': ('gender', 'blood_group', 'medical_history')
        }),
        ('Readmission Risk', {
            'fields': ('readmission_risk_score', 'readmission_risk_level',
                      'previous_admissions', 'chronic_conditions_count')
        }),
        ('Contact Info', {
            'fields': ('address', 'phone_number', 'emergency_contact')
        })
    )

@admin.register(Admission)
class AdmissionAdmin(admin.ModelAdmin):
    list_display = ('patient', 'admission_date', 'discharge_date', 'duration_days', 'department')
    list_filter = ('department',)
    search_fields = ('patient__first_name', 'patient__last_name')
    date_hierarchy = 'admission_date'
    readonly_fields = ('duration_days',)

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'get_document_type_display', 'uploaded_at', 'uploaded_by')
    list_filter = ('document_type', 'uploaded_at')
    search_fields = ('patient__first_name', 'patient__last_name', 'description')
    readonly_fields = ('file_name', 'uploaded_at')
