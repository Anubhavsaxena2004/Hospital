from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Administrator'),
        ('DOCTOR', 'Doctor'),
        ('NURSE', 'Nurse'),
        ('RECEPTIONIST', 'Receptionist'),
        ('LAB_TECH', 'Lab Technician'),
        ('PHARMACIST', 'Pharmacist'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    department = models.CharField(max_length=100, blank=True)
    specialization = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    is_on_duty = models.BooleanField(default=False)
    
    # Add related_name to resolve reverse accessor conflicts
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

class Patient(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    emergency_contact = models.CharField(max_length=15)
    blood_group = models.CharField(max_length=5)
    medical_history = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('SCHEDULED', 'Scheduled'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
        ('MISSED', 'Missed'),
    )
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'DOCTOR'})
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SCHEDULED')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Bed(models.Model):
    WARD_CHOICES = (
        ('ICU', 'Intensive Care Unit'),
        ('GENERAL', 'General Ward'),
        ('EMERGENCY', 'Emergency Ward'),
        ('PRIVATE', 'Private Room'),
    )
    bed_number = models.CharField(max_length=10, unique=True)
    ward = models.CharField(max_length=20, choices=WARD_CHOICES)
    is_occupied = models.BooleanField(default=False)
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True)
    last_cleaned = models.DateTimeField(auto_now=True)

class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'DOCTOR'})
    diagnosis = models.TextField()
    treatment = models.TextField()
    prescription = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class LabTest(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    test_name = models.CharField(max_length=100)
    test_type = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    result = models.TextField(blank=True)
    technician = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'LAB_TECH'})
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

class Medicine(models.Model):
    name = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    expiry_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

class Billing(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('PARTIAL', 'Partially Paid'),
    )
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    insurance_claim = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class EmergencyAlert(models.Model):
    PRIORITY_CHOICES = (
        ('HIGH', 'High'),
        ('MEDIUM', 'Medium'),
        ('LOW', 'Low'),
    )
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    description = models.TextField()
    status = models.CharField(max_length=20, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
