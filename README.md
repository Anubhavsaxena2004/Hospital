# Hospital Management System

A comprehensive hospital management system built with Django and React.

## Features

### 1. Overview / Summary Panel
- Total Patients (Admitted, Discharged, OPD)
- Available vs Occupied Beds
- Staff On Duty (Doctors/Nurses)
- Emergency Alerts
- Revenue (Daily/Monthly)
- Appointments Today
- Operation Theatres in Use

### 2. Patient Management
- Patient List (Searchable)
- Patient Details Card (History, Diagnosis, Medications)
- New Patient Admission Form
- Discharge Summary Tracker
- Inpatient / Outpatient Filter

### 3. Appointment Management
- Upcoming Appointments
- Schedule New Appointment
- Doctor Availability
- Missed / Cancelled Appointments

### 4. Doctor & Staff Panel
- Staff Directory (Doctors, Nurses, Admin)
- Shift Schedules
- Attendance & Leaves
- Add/Edit Staff Info

### 5. Bed & Ward Management
- Bed Occupancy Status (Live Map)
- ICU / General / Emergency Ward Status
- Bed Allotment Requests
- Cleaning & Maintenance Tracker

### 6. Emergency & Alerts
- Real-Time Emergency Alerts
- Ambulance Tracker
- Priority Patient Highlight
- Critical Condition Monitor

### 7. Lab & Reports
- Pending Lab Tests
- Upload / Download Reports
- Radiology / Pathology Dashboard
- Test Scheduling

### 8. Pharmacy & Inventory
- Available Medicines List
- Prescription Fulfillment
- Medicine Stock Level
- Restock Alerts
- Expiry Management

### 9. Billing & Finance
- Patient Billing Status
- Generate Invoice
- Insurance Claims Status
- Daily/Monthly Revenue Chart

### 10. Analytics & Insights
- Disease Trends
- Readmission Rates
- Department-wise Load
- Staff Performance Metrics

### 11. Notifications & Communication
- Internal Chat (Doctor ↔ Nurse)
- Announcements
- Emergency Notifications
- Appointment Reminders

### 12. Settings & Access Control
- Role-Based Access (Doctor, Admin, Receptionist)
- Theme / Language Switch
- Profile Settings
- Log History

## Setup Instructions

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

## API Documentation

The API is available at `/api/` with the following endpoints:

- `/api/users/` - User management
- `/api/patients/` - Patient management
- `/api/appointments/` - Appointment management
- `/api/beds/` - Bed management
- `/api/medical-records/` - Medical records
- `/api/lab-tests/` - Lab tests
- `/api/medicines/` - Medicine inventory
- `/api/billing/` - Billing management
- `/api/emergency-alerts/` - Emergency alerts

## Security

- JWT Authentication
- Role-based access control
- CORS protection
- Secure password hashing
- CSRF protection

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 