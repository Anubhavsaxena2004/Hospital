from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import (
    Patient, Appointment, Bed, MedicalRecord,
    LabTest, Medicine, Billing, EmergencyAlert
)
from .serializers import (
    UserSerializer, PatientSerializer, AppointmentSerializer,
    BedSerializer, MedicalRecordSerializer, LabTestSerializer,
    MedicineSerializer, BillingSerializer, EmergencyAlertSerializer
)
from django.utils import timezone

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'ADMIN':
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        patients = Patient.objects.filter(
            first_name__icontains=query
        ) | Patient.objects.filter(
            last_name__icontains=query
        )
        serializer = self.get_serializer(patients, many=True)
        return Response(serializer.data)

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'DOCTOR':
            return Appointment.objects.filter(doctor=self.request.user)
        return Appointment.objects.all()

    @action(detail=False, methods=['get'])
    def today(self, request):
        today = timezone.now().date()
        appointments = self.get_queryset().filter(date=today)
        serializer = self.get_serializer(appointments, many=True)
        return Response(serializer.data)

class BedViewSet(viewsets.ModelViewSet):
    queryset = Bed.objects.all()
    serializer_class = BedSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def available(self, request):
        available_beds = Bed.objects.filter(is_occupied=False)
        serializer = self.get_serializer(available_beds, many=True)
        return Response(serializer.data)

class MedicalRecordViewSet(viewsets.ModelViewSet):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'DOCTOR':
            return MedicalRecord.objects.filter(doctor=self.request.user)
        return MedicalRecord.objects.all()

class LabTestViewSet(viewsets.ModelViewSet):
    queryset = LabTest.objects.all()
    serializer_class = LabTestSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        lab_test = self.get_object()
        lab_test.status = 'COMPLETED'
        lab_test.completed_at = timezone.now()
        lab_test.result = request.data.get('result', '')
        lab_test.save()
        return Response(self.get_serializer(lab_test).data)

class MedicineViewSet(viewsets.ModelViewSet):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        low_stock = Medicine.objects.filter(quantity__lt=10)
        serializer = self.get_serializer(low_stock, many=True)
        return Response(serializer.data)

class BillingViewSet(viewsets.ModelViewSet):
    queryset = Billing.objects.all()
    serializer_class = BillingSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def make_payment(self, request, pk=None):
        billing = self.get_object()
        amount = float(request.data.get('amount', 0))
        billing.paid_amount += amount
        if billing.paid_amount >= billing.total_amount:
            billing.status = 'PAID'
        else:
            billing.status = 'PARTIAL'
        billing.save()
        return Response(self.get_serializer(billing).data)

class EmergencyAlertViewSet(viewsets.ModelViewSet):
    queryset = EmergencyAlert.objects.all()
    serializer_class = EmergencyAlertSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        alert = self.get_object()
        alert.status = 'RESOLVED'
        alert.resolved_at = timezone.now()
        alert.save()
        return Response(self.get_serializer(alert).data)
