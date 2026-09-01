from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    list_display = [
        'student',
        'tutor',
        'class_name',
        'subject',
        'preferred_time',
        'status',
        'created_at',
    ]

    list_filter = [
        'status',
        'class_name',
        'subject',
    ]

    search_fields = [
        'student__username',
        'tutor__user__username',
        'subject',
    ]