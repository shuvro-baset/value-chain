from django.db import models
from django.utils.translation import gettext, gettext_lazy as _
from django.utils.safestring import mark_safe

from django.contrib.auth.models import AbstractUser

class UniUser(AbstractUser):
    USER_TYPES = (
        ('Stock User', 'Stock User'),
        ('Production User', 'Production User'),
        ('Sales User', 'Sales User'),
        ('Purchase User', 'Purchase User'),
    )
    user_type = models.CharField(choices=USER_TYPES, max_length=200, default=USER_TYPES[0], help_text=mark_safe('<h2 style="color: #008CBA;">Set user type if user is customer or sales.</h2>'))
    phone_number = models.CharField(max_length=15, null=True, blank=True)