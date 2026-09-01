from django.shortcuts import render
from django.contrib.auth.models import User

from accounts.models import UserProfile
from bookings.models import Booking, Notification
from tutors.models import TutorProfile, Review


# ==================================================
# HOME
# ==================================================

def home(request):

    return render(
        request,
        'home.html'
    )


# ==================================================
# CUSTOM ADMIN DASHBOARD
# ==================================================

def admin_dashboard(request):

    # --------------------------------------------------
    # LOGIN CHECK
    # --------------------------------------------------

    if not request.user.is_authenticated:
        return render(
            request,
            'home.html'
        )

    # --------------------------------------------------
    # STAFF CHECK
    # --------------------------------------------------

    if not request.user.is_staff:
        return render(
            request,
            'home.html'
        )

    # ==================================================
    # STATISTICS
    # ==================================================

    total_students = UserProfile.objects.filter(
        role='student'
    ).count()

    total_tutors = TutorProfile.objects.count()

    total_bookings = Booking.objects.count()

    pending_bookings = Booking.objects.filter(
        status='Pending'
    ).count()

    accepted_bookings = Booking.objects.filter(
        status='Accepted'
    ).count()

    rejected_bookings = Booking.objects.filter(
        status='Rejected'
    ).count()

    completed_bookings = Booking.objects.filter(
        status='Completed'
    ).count()

    total_reviews = Review.objects.count()

    verified_tutors = TutorProfile.objects.filter(
        is_verified=True
    ).count()

    unverified_tutors = TutorProfile.objects.filter(
        is_verified=False
    ).count()

    # ==================================================
    # ADMIN NOTIFICATIONS
    # ==================================================

    admin_notifications = Notification.objects.filter(
        user=request.user
    ).order_by(
        '-created_at'
    )[:5]

    unread_notifications_count = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).count()

    # ==================================================
    # RENDER DASHBOARD
    # ==================================================

    return render(
        request,
        'admin_dashboard.html',
        {
            'total_students': total_students,
            'total_tutors': total_tutors,
            'total_bookings': total_bookings,

            'pending_bookings': pending_bookings,
            'accepted_bookings': accepted_bookings,
            'rejected_bookings': rejected_bookings,
            'completed_bookings': completed_bookings,

            'total_reviews': total_reviews,

            'verified_tutors': verified_tutors,
            'unverified_tutors': unverified_tutors,

            'admin_notifications': admin_notifications,
            'unread_notifications_count': unread_notifications_count,
        }
    )