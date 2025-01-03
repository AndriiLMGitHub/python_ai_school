from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from app.models import Task


class CustomUser(AbstractUser):
    FORMS = (
        ('7', '7 клас'),
        ('8', '8 клас'),
        ('9', '9 клас'),
    )
    username = None
    email = models.EmailField(_("Email address"), unique=True)
    is_leader = models.BooleanField(_("Leader"), default=False)
    form_pupil = models.CharField(
        _("Form"),
        max_length=10,
        choices=FORMS,
        # default="7"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        'first_name',
        'last_name',
        'form_pupil',
    ]

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Profile(models.Model):
    SEX = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    sex = models.CharField(
        _("Sex"),
        max_length=128,
        blank=True,
        null=True,
        choices=SEX
    )
    birth_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    image = models.FileField(upload_to="profiles/", null=True, blank=True)
    bio = models.TextField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Profile for {self.user.email}"
