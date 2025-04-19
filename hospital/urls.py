"""
URL configuration for hospital project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views.fraud_detection import detect_fraud
from django.conf import settings
from django.conf.urls.static import static
from .views.core_views import patient_search_api
from . import views
from .views import appointment_update, appointment_delete
from .views.medical_record_views import medical_record_create, MedicalRecordDetailView
from .views.core_views import test_bill_view
from .views.financial_views import (
    document_upload,
    financial_reports,
    transaction_list,
    transaction_detail,
    transaction_create,
    transaction_edit,
    transaction_delete
)
from .views.bed_views import bed_management, bed_detail, bed_edit, BedDeleteView, bed_create
from .views.maintenance_views import (
    MaintenanceListView,
    MaintenanceDetailView, 
    MaintenanceCreateView,
    MaintenanceUpdateView,
    maintenance_create
)

urlpatterns = [
    path('api/detect-fraud/', detect_fraud, name='detect-fraud'),
    # Admin
    path('admin/', admin.site.urls),
    path('admin/verify-transaction/<int:pk>/', views.verify_transaction, name='verify_transaction'),
    path('admin/flag-transaction/<int:pk>/', views.flag_transaction, name='flag_transaction'),
    
    # API endpoints
    path('api/', include('core.urls')),
    path('api/patients/search/', patient_search_api, name='patient_search_api'),
    
    # Authentication
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.register, name='register'),
    
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Patient URLs
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/create/', views.patient_create, name='patient_create'),
    path('patients/<int:pk>/', views.patient_detail, name='patient_detail'),
    path('patients/<int:pk>/edit/', views.patient_edit, name='patient_edit'),
    path('patients/<int:pk>/delete/', views.patient_delete, name='patient_delete'),
    
    # Medical Records
    path('patients/<int:patient_id>/medical-records/add/', views.add_medical_record, name='add_medical_record'),
    
    # Appointments
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/create/', views.appointment_create, name='appointment_create'),
    path('appointments/<int:pk>/', views.appointment_detail, name='appointment_detail'),
    path('appointments/<int:pk>/edit/', appointment_update, name='appointment_update'),
    path('appointments/<int:pk>/delete/', views.appointment_delete, name='appointment_delete'),
    
    # Billing
    path('patients/<int:patient_id>/bills/add/', views.add_bill, name='add_bill'),
    path('bills/<int:pk>/', views.bill_detail, name='bill_detail'),
    
    # Documents
    path('patients/<int:patient_id>/documents/upload/', views.upload_document, name='upload_document'),
    
    # Beds
    path('beds/', bed_management, name='bed_management'),
    path('beds/list/', bed_management, name='bed_list'),  # Added alias for bed_list
    path('beds/create/', bed_create, name='bed_create'),
    path('beds/<int:pk>/', bed_detail, name='bed_detail'),
    path('beds/<int:pk>/edit/', bed_edit, name='bed_edit'),
    path('beds/<int:pk>/delete/', BedDeleteView.as_view(), name='bed_delete'),
    # Maintenance Records
    path('maintenance/', MaintenanceListView.as_view(), name='maintenance_list'),
    path('maintenance/create/', MaintenanceCreateView.as_view(), name='maintenance_create'),
    path('maintenance/<int:pk>/', MaintenanceDetailView.as_view(), name='maintenance_detail'),
    path('maintenance/<int:pk>/edit/', MaintenanceUpdateView.as_view(), name='maintenance_update'),
    path('beds/<int:bed_id>/maintenance/create/', maintenance_create, name='bed_maintenance_create'),
    
    # Financial Management
    path('financial/reports/', financial_reports, name='financial_reports'),
    path('financial/transactions/', transaction_list, name='transaction_list'),
    path('financial/transactions/<int:pk>/', transaction_detail, name='transaction_detail'),
    path('financial/transactions/create/', transaction_create, name='transaction_create'),
    path('financial/transactions/<int:pk>/edit/', transaction_edit, name='transaction_edit'),
    path('financial/transactions/<int:pk>/delete/', transaction_delete, name='transaction_delete'),
    path('financial/transactions/<int:transaction_id>/documents/upload/', document_upload, name='document_upload'),
    path('history/', views.history, name='history'),
    path('test-bill/', test_bill_view, name='test-bill'),
    path('medical-records/create/', medical_record_create, name='medical_record_create'),
    path('medical-records/<int:pk>/', MedicalRecordDetailView.as_view(), name='medical_record_detail'),
    path('medical-records/', views.medical_record_list, name='medical_record_list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
