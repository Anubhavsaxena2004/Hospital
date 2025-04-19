# Core views
from .core_views import (
    dashboard,
    register,
    history,
    medical_record_list
)

# Patient views
from .patient_views import (
    patient_list,
    patient_create,
    patient_detail,
    patient_edit,
    patient_delete,
    add_medical_record,
    add_bill,
    upload_document
)

# Financial views
from .financial_views import (
    financial_reports,
    transaction_list,
    transaction_detail,
    transaction_create,
    transaction_edit,
    transaction_delete,
    bill_detail
)

# Appointment views
from .appointment_views import (
    appointment_list,
    appointment_create,
    appointment_detail,
    appointment_update,
    appointment_delete
)

# Bed management views
from .bed_views import bed_management

# Transaction actions
from .transaction_actions import (
    verify_transaction,
    flag_transaction
)

# Medical Record views
from .medical_record_views import (
    medical_record_list,
    medical_record_create,
    MedicalRecordDetailView
)

# Fraud detection
from .fraud_detection import detect_fraud
