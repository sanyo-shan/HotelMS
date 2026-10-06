from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Register(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField()

    def __str__(self):
        return self.username