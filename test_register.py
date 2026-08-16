import sys
sys.path.insert(0, 'Backend')
sys.path.insert(0, 'Database_Devops')

from app.database.database import SessionLocal
from app.services.auth_service import AuthService
from app.schemas.user import UserRegister

db = SessionLocal()
try:
    user = UserRegister(
        full_name='Amisha Pandey',
        email='amisha.test999@example.com',
        password='TestPass123!'
    )
    result = AuthService.register(db, user)
    print('SUCCESS! User registered:')
    print('  id:', result.id)
    print('  full_name:', result.full_name)
    print('  email:', result.email)
    print('  role_id:', result.role_id)
    print('  is_active:', result.is_active)
except Exception as e:
    print('Error type:', type(e).__name__)
    print('Error:', e)
    import traceback
    traceback.print_exc()
finally:
    db.close()
