from django.db import models
from django.contrib.auth.models import User


class Subject(models.Model):

    name = models.CharField(
        max_length=100
    )

    def __str__(self):
        return self.name


class TutorProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    qualification = models.CharField(
        max_length=200,
        blank=True
    )

    experience = models.PositiveIntegerField(
        default=0
    )

    classes = models.CharField(
        max_length=100,
        default="Class 2 - Class 10"
    )

    subjects = models.ManyToManyField(
        Subject,
        blank=True
    )

    location = models.CharField(
        max_length=200,
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

    fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    available_time = models.CharField(
        max_length=200,
        blank=True
    )

    is_verified = models.BooleanField(
        default=False
    )

    def __str__(self):
        return (
            self.user.get_full_name()
            or self.user.username
        )


class Review(models.Model):

    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]

    tutor = models.ForeignKey(
        TutorProfile,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tutor_reviews'
    )

    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES
    )

    comment = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = [
            '-created_at'
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    'tutor',
                    'student'
                ],
                name='unique_student_tutor_review'
            )
        ]

    def __str__(self):

        return (
            f"{self.student.username} → "
            f"{self.tutor.user.username} "
            f"({self.rating}/5)"
        )