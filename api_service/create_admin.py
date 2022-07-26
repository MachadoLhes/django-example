from django.contrib.auth.models import User

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@jobsity.com', 'changeMe#4321')
    print("Created superuser admin")
else:
    print("Superuser admin already exists, skipping")