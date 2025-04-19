from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.utils import timezone

User = get_user_model()

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    head = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='hospital_department_head'
    )
    location = models.CharField(max_length=100, default='Main Building')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Equipment(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    quantity = models.PositiveIntegerField(default=1)
    department = models.ForeignKey(
        Department, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )

    def __str__(self):
        return self.name

class Doctor(models.Model):
    SPECIALIZATION_CHOICES = [
        ('cardiology', 'Cardiology'),
        ('neurology', 'Neurology'),
        ('pediatrics', 'Pediatrics'),
        ('orthopedics', 'Orthopedics'),
        ('general', 'General Medicine'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='doctor_profile'
    )
    license_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    specialization = models.CharField(
        max_length=50,
        choices=SPECIALIZATION_CHOICES
    )
    years_of_experience = models.PositiveIntegerField(default=0)
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['user__last_name', 'user__first_name']

    def __str__(self):
        return f"Dr. {self.user.get_full_name()} ({self.get_specialization_display()})"

class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('deceased', 'Deceased'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, blank=True)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    emergency_contact = models.CharField(max_length=100)
    emergency_phone = models.CharField(
        max_length=15,
        blank=False,
        null=False,
        default='0000000000',
        help_text="Emergency contact phone number",
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
        ]
    )
    medical_history = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self):
        """Returns the patient's full name."""
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ['last_name', 'first_name']

class Bill(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    date_issued = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='pending'
    )
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_issued']

    def __str__(self):
        return f"Bill #{self.id} - {self.patient} (Status: {self.get_status_display()})"

class Transaction(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('credit', 'Credit Card'),
        ('debit', 'Debit Card'),
        ('insurance', 'Insurance'),
        ('check', 'Check'),
        ('bank_transfer', 'Bank Transfer'),
    ]
    
    TRANSACTION_TYPE_CHOICES = [
        ('payment', 'Payment'),
        ('refund', 'Refund'),
        ('adjustment', 'Adjustment'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('reversed', 'Reversed'),
    ]
    
    CATEGORY_CHOICES = [
        ('consultation', 'Consultation'),
        ('procedure', 'Procedure'),
        ('medication', 'Medication'),
        ('room', 'Room Charge'),
        ('other', 'Other'),
    ]

    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, null=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(null=True, blank=True)
    type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES, default='payment')
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        null=True,
        blank=True
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='consultation')
    description = models.TextField(blank=True)
    reference_number = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Financial Transaction'
        verbose_name_plural = 'Financial Transactions'

    def __str__(self):
        return f"{self.get_type_display()} #{self.id} for {self.patient} ({self.get_status_display()})"

class Bed(models.Model):
    WARD_CHOICES = [
        ('general', 'General Ward'),
        ('private', 'Private Room'),
        ('icu', 'ICU'),
        ('pediatric', 'Pediatric Ward'),
    ]
    
    BED_STATUS_CHOICES = [
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Under Maintenance'),
    ]

    number = models.CharField(max_length=10, unique=True)
    ward = models.CharField(max_length=20, choices=WARD_CHOICES)
    status = models.CharField(max_length=20, choices=BED_STATUS_CHOICES, default='available')
    floor = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    room_number = models.CharField(max_length=10)
    equipment = models.ManyToManyField(Equipment, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Bed {self.number} ({self.get_ward_display()})"

    def get_maintenance_records(self):
        return self.maintenancerecord_set.all().order_by('-created_at')

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='hospital_appointments'
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    appointment_date = models.DateField(null=True, blank=True)
    appointment_time = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled', blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-appointment_date', '-appointment_time']
        unique_together = ('doctor', 'appointment_date', 'appointment_time')

    @property
    def status_color(self):
        status_colors = {
            'scheduled': 'primary',
            'completed': 'success', 
            'cancelled': 'danger',
            'no_show': 'warning'
        }
        return status_colors.get(self.status, 'secondary')

    def __str__(self):
        return f"Appointment for {self.patient} with Dr. {self.doctor.get_full_name()} on {self.appointment_date}"

class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    diagnosis = models.TextField()
    treatment = models.TextField()
    doctor = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='hospital_medical_records'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Record for {self.patient} on {self.date}"

class Document(models.Model):
    DOCUMENT_TYPES = [
        ('prescription', 'Prescription'),
        ('report', 'Medical Report'),
        ('invoice', 'Invoice'),
        ('receipt', 'Receipt'),
        ('discharge', 'Discharge Summary'),
        ('lab', 'Lab Result'),
        ('imaging', 'Imaging Report'),
        ('other', 'Other'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True)
    transaction = models.ForeignKey(
        'Transaction',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='documents'
    )
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    file = models.FileField(upload_to='documents/%Y/%m/%d/')
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Patient Document'
        verbose_name_plural = 'Patient Documents'

    def __str__(self):
        return f"{self.get_document_type_display()} for {self.patient} ({self.created_at.date()})"

class MaintenanceRecord(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    bed = models.ForeignKey(Bed, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    technician = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)
    estimated_duration = models.DurationField(null=True, blank=True)
    actual_duration = models.DurationField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Maintenance Record'
        verbose_name_plural = 'Maintenance Records'

    def __str__(self):
        return f"Maintenance #{self.id} for {self.bed} ({self.get_status_display()})"
