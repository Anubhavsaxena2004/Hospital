from django import forms
from .models import Bed, Equipment, Patient, Document, Transaction
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import MedicalRecord, Appointment, Bill, Doctor, MaintenanceRecord, Department
import os

User = get_user_model()

class BedForm(forms.ModelForm):
    class Meta:
        model = Bed
        fields = ['number', 'ward', 'status', 'floor', 'room_number', 'equipment', 'patient', 'notes']
        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'ward': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'floor': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 10
            }),
            'room_number': forms.TextInput(attrs={'class': 'form-control'}),
            'equipment': forms.CheckboxSelectMultiple(),
            'patient': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Enter any special notes about this bed...'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['patient'].queryset = Patient.objects.filter(
            status='active'
        ).order_by('last_name', 'first_name')

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'first_name', 'last_name', 'date_of_birth', 'gender',
            'address', 'phone_number', 'emergency_contact',
            'blood_group', 'medical_history', 'status'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'YYYY-MM-DD',
                'id': 'id_date_of_birth'
            }),
            'medical_history': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control'
            }),
        }

class MedicalRecordForm(forms.ModelForm):
    patient = forms.ModelChoiceField(
        queryset=Patient.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Patient'
    )
    
    class Meta:
        model = MedicalRecord
        fields = ['patient', 'date', 'time', 'diagnosis', 'treatment', 'doctor']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),
            'diagnosis': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Enter diagnosis details...'
            }),
            'treatment': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Enter treatment details...'
            }),
            'doctor': forms.Select(attrs={'class': 'form-select'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['patient'].queryset = Patient.objects.all().order_by('last_name', 'first_name')

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'appointment_date', 'appointment_time', 'status', 'notes', 'department']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-select'}),
            'doctor': forms.Select(attrs={'class': 'form-select'}),
            'appointment_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'Select appointment date',
                'min': timezone.now().strftime('%Y-%m-%d')
            }),
            'appointment_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control',
                'placeholder': 'Select appointment time',
                'min': '08:00',
                'max': '18:00'
            }),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter appointment notes...'
            }),
            'department': forms.Select(attrs={'class': 'form-select'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['department'].queryset = Department.objects.all()

class BillForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        patient_id = kwargs.pop('patient_id', None)
        super().__init__(*args, **kwargs)
        
        if patient_id:
            self.fields['patient'].widget = forms.HiddenInput()
            self.fields['patient'].initial = patient_id
        else:
            self.fields['patient'].widget = forms.Select(attrs={'class': 'form-select'})
            self.fields['patient'].queryset = Patient.objects.all().order_by('last_name', 'first_name')

    class Meta:
        model = Bill
        fields = ['patient', 'amount', 'description', 'status']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            'patient', 'type', 'category', 'department', 
            'amount', 'description', 'status', 'date'
        ]
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-select'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'description': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Enter transaction details...'
            }),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['patient'].queryset = Patient.objects.filter(
                status='active'
            ).order_by('last_name', 'first_name')

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['document_type', 'file', 'description', 'transaction']
        widgets = {
            'transaction': forms.HiddenInput(),
            'document_type': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            ext = os.path.splitext(file.name)[1]
            valid_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.png', '.jpeg']
            if not ext.lower() in valid_extensions:
                raise forms.ValidationError('Unsupported file extension.')
        return file

class MaintenanceRecordForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRecord
        fields = ['bed', 'title', 'description', 'status', 'priority', 'technician', 'notes']
        widgets = {
            'bed': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Describe the maintenance issue...'
            }),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'technician': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Enter any additional notes...'
            }),
        }

    def __init__(self, *args, **kwargs):
        bed_id = kwargs.pop('bed_id', None)
        super().__init__(*args, **kwargs)
        
        if bed_id:
            self.fields['bed'].initial = bed_id
            
        self.fields['technician'].queryset = get_user_model().objects.filter(
            is_staff=True
        ).order_by('last_name', 'first_name')
