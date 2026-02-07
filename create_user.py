import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tourguidepro.settings')
django.setup()

from django.contrib.auth.models import User

try:
    # Try to create new superuser
    user = User.objects.create_superuser(
        username='vs7574258@gmail.com',
        email='vs7574258@gmail.com',
        password='Vikash@4957'
    )
    print(f'✅ Superuser created successfully!')
    print(f'   Username: {user.username}')
    print(f'   Email: {user.email}')
    print(f'   Is Staff: {user.is_staff}')
    print(f'   Is Superuser: {user.is_superuser}')
except User.DoesNotExist:
    print('User does not exist')
except Exception as e:
    print(f'⚠️  Error: {str(e)}')
    if 'already exists' in str(e):
        print('   → This user already exists. Using existing account.')
