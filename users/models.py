from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    city = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email




from django.db import models
from materials.models import Course, Lesson
from django.contrib.auth import get_user_model

User = get_user_model()

class Payment(models.Model):
    PAYMENT_METHODS = (
        ('cash', 'Cash'),
        ('transfer', 'Bank Transfer'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    course = models.ForeignKey(Course, null=True, blank=True, on_delete=models.SET_NULL)
    lesson = models.ForeignKey(Lesson, null=True, blank=True, on_delete=models.SET_NULL)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)

    def __str__(self):
        return f"{self.user} - {self.amount} - {self.payment_method}"
