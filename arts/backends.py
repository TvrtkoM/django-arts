from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

class UserBackend(ModelBackend):
    def authenticate(self, email=None, password=None):
        try:
            user = User.objects.get(email__exact=email)
        except User.DoesNotExist:
            return None
        else:
            return user if user.check_password(password) else None
