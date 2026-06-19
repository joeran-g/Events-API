from models import db, User

def test_user_password_hashing():
    user = User()
    user.username = 'testuser'
    password = 'secure_password_123'
    user.set_password(password)
        
    assert user.check_password(password) is True
    assert user.check_password('wrong_password') is False
