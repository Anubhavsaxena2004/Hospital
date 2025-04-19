from django.core.management.base import BaseCommand
from hospital.models import Patient
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Seeds the database with sample patient data'

    def handle(self, *args, **options):
        # Clear existing patients first
        Patient.objects.all().delete()
        
        fake = Faker()
        GENDER_CHOICES = ['M', 'F', 'O']
        BLOOD_GROUPS = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        STATUS_CHOICES = ['active', 'inactive', 'deceased']

        for i in range(20):
            # Generate strictly formatted 10-digit phone numbers
            phone = fake.numerify(text='##########')  # Exactly 10 digits
            emergency_phone = fake.numerify(text='##########')  # Exactly 10 digits
            
            Patient.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=90),
                gender=random.choice(GENDER_CHOICES),
                blood_group=random.choice(BLOOD_GROUPS),
                phone_number=phone,
                address=fake.address(),
                emergency_contact=fake.name(),
                emergency_phone=emergency_phone,
                status=random.choice(STATUS_CHOICES)
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded patient data'))
