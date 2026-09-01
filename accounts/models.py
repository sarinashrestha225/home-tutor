from django.db import models
from django.contrib.auth.models import User


# ==================================================
# USER PROFILE
# ==================================================

class UserProfile(models.Model):

    ROLE_CHOICES = [
        ('student', 'Student / Parent'),
        ('tutor', 'Tutor'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    # ==================================================
    # STUDENT / USER LOCATION
    # ==================================================

    location = models.CharField(
        max_length=255,
        blank=True
    )

    latitude = models.FloatField(
        null=True,
        blank=True
    )

    longitude = models.FloatField(
        null=True,
        blank=True
    )

    def __str__(self):

        return (
            f"{self.user.username} - "
            f"{self.role}"
        )


# ==================================================
# ADMIN PROFILE
# ==================================================

class AdminProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='admin_profile'
    )

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    designation = models.CharField(
        max_length=100,
        default='Administrator'
    )

    def __str__(self):

        return (
            f"{self.user.username} - "
            f"{self.designation}"
        )