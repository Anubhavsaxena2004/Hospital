from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User, Patient, Appointment, Bed,
    MedicalRecord, LabTest, Medicine,
    Billing, EmergencyAlert
)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'department', 'is_on_duty')
    list_filter = ('role', 'department', 'is_on_duty')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Hospital Info', {'fields': ('role', 'department', 'specialization', 'phone_number', 'is_on_duty')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'gender', 'blood_group', 'phone_number')
    list_filter = ('gender', 'blood_group')
    search_fields = ('first_name', 'last_name', 'phone_number')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date', 'time', 'status')
    list_filter = ('status', 'date', 'doctor')
    search_fields = ('patient__first_name', 'patient__last_name', 'doctor__first_name', 'doctor__last_name')

@admin.register(Bed)
class BedAdmin(admin.ModelAdmin):
    list_display = ('bed_number', 'ward', 'is_occupied', 'patient', 'last_cleaned')
    list_filter = ('ward', 'is_occupied')
    search_fields = ('bed_number', 'patient__first_name', 'patient__last_name')

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'created_at')
    list_filter = ('created_at', 'doctor')
    search_fields = ('patient__first_name', 'patient__last_name', 'doctor__first_name', 'doctor__last_name')

@admin.register(LabTest)
class LabTestAdmin(admin.ModelAdmin):
    list_display = ('patient', 'test_name', 'status', 'technician', 'created_at')
    list_filter = ('status', 'test_type', 'created_at')
    search_fields = ('patient__first_name', 'patient__last_name', 'test_name')

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'manufacturer', 'quantity', 'unit_price', 'expiry_date')
    list_filter = ('manufacturer', 'expiry_date')
    search_fields = ('name', 'manufacturer')

@admin.register(Billing)
class BillingAdmin(admin.ModelAdmin):
    list_display = ('patient', 'total_amount', 'paid_amount', 'status', 'insurance_claim')
    list_filter = ('status', 'insurance_claim', 'created_at')
    search_fields = ('patient__first_name', 'patient__last_name')

@admin.register(EmergencyAlert)
class EmergencyAlertAdmin(admin.ModelAdmin):
    list_display = ('patient', 'priority', 'status', 'created_at', 'resolved_at')
    list_filter = ('priority', 'status', 'created_at')
    search_fields = ('patient__first_name', 'patient__last_name', 'description')
