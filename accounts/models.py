from django.db import models
from django.contrib.auth.models import User
# AbstractUser - Provides built-in fields and methods such as password, first name, last name, is_staff, is_superuser, is_active, etc.
# BaseUserManager - Provides methods to manage user creation

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

