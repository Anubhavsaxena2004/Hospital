from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Patient, Appointment, Bed, MedicalRecord,
    LabTest, Medicine, Billing, EmergencyAlert
)

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'department', 
                 'specialization', 'phone_number', 'is_on_duty']
        read_only_fields = ['id']

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.get_full_name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.get_full_name', read_only=True)

    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ['created_at']

class BedSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.get_full_name', read_only=True)

    class Meta:
        model = Bed
        fields = '__all__'

class MedicalRecordSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.get_full_name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.get_full_name', read_only=True)

    class Meta:
        model = MedicalRecord
        fields = '__all__'
        read_only_fields = ['created_at']

class LabTestSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.get_full_name', read_only=True)
    technician_name = serializers.CharField(source='technician.get_full_name', read_only=True)

    class Meta:
        model = LabTest
        fields = '__all__'
        read_only_fields = ['created_at', 'completed_at']

class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = '__all__'
        read_only_fields = ['created_at']

class BillingSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.get_full_name', read_only=True)

    class Meta:
        model = Billing
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class EmergencyAlertSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.get_full_name', read_only=True)

    class Meta:
        model = EmergencyAlert
        fields = '__all__'
        read_only_fields = ['created_at', 'resolved_at'] 