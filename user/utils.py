from django.contrib.auth.hashers import make_password, check_password
from .models import User

def hash_user_password(password):
    hashed_password = make_password(password)
    return hashed_password

def verify_user_password(password, hashed_password):
    return check_password(password, hashed_password)
