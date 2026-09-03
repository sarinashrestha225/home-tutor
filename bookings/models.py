from django.db import models
from django.contrib.auth.models import User
from tutors.models import TutorProfile


class Booking(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
        ('Completed', 'Completed'),
    ]

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='student_bookings'
    )

    tutor = models.ForeignKey(
        TutorProfile,
        on_delete=models.CASCADE,
        related_name='tutor_bookings'
    )

    class_name = models.CharField(
        max_length=100
    )

    subject = models.CharField(
        max_length=100
    )

    preferred_time = models.CharField(
        max_length=100
    )

    message = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.student.username} → "
            f"{self.tutor.user.username} "
            f"({self.status})"
        )


class Notification(models.Model):

    NOTIFICATION_TYPES = [
        ('request', 'New Tutor Request'),
        ('accepted', 'Request Accepted'),
        ('rejected', 'Request Rejected'),
        ('registered', 'New Registration'),
        ('review', 'New Review'),
        ('system', 'System Notification'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications'
    )

    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='notifications'
    )

    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES,
        default='system'
    )

    message = models.CharField(
        max_length=255
    )

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.user.username} - "
            f"{self.notification_type}"
        )