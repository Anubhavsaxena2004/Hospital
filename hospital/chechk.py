import os
import django
import sys
# file for generating password hash
# Add the root folder to the path (the folder where manage.py is located)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital.settings')

# Setup Django
django.setup()

# Now you can safely use Django stuff
from django.contrib.auth.hashers import make_password

new_password = "anubhuti2004"
hashed = make_password(new_password)
print(hashed)