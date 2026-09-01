from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from tutors.models import TutorProfile, Review
from tutors.forms import ReviewForm

from .models import Booking, Notification
from .forms import BookingForm


# ==================================================
# SEND TUTOR REQUEST
# ==================================================

@login_required
def send_request(request, tutor_id):

    tutor = get_object_or_404(
        TutorProfile,
        id=tutor_id
    )

    # ------------------------------------------
    # PREVENT DUPLICATE ACTIVE REQUEST
    # ------------------------------------------

    existing_request = Booking.objects.filter(
        student=request.user,
        tutor=tutor,
        status__in=[
            'Pending',
            'Accepted'
        ]
    ).first()

    if existing_request:

        messages.warning(
            request,
            'You already have an active request with this tutor.'
        )

        return redirect(
            'my_requests'
        )

    # ------------------------------------------
    # SHOW FORM
    # ------------------------------------------

    if request.method == 'POST':

        form = BookingForm(
            request.POST
        )

        if form.is_valid():

            booking = form.save(
                commit=False
            )

            booking.student = request.user
            booking.tutor = tutor
            booking.status = 'Pending'

            booking.save()

            student_name = (
                request.user.get_full_name()
                or request.user.username
            )

            tutor_name = (
                tutor.user.get_full_name()
                or tutor.user.username
            )

            # ======================================
            # NOTIFICATION FOR TUTOR
            # ======================================

            Notification.objects.create(
                user=tutor.user,
                booking=booking,
                notification_type='request',
                message=(
                    f'New tutor request from '
                    f'{student_name} for '
                    f'{booking.subject}.'
                )
            )

            # ======================================
            # NOTIFICATION FOR ADMINS
            # ======================================

            admin_users = User.objects.filter(
                is_staff=True,
                is_active=True
            )

            for admin_user in admin_users:

                Notification.objects.create(
                    user=admin_user,
                    booking=booking,
                    notification_type='request',
                    message=(
                        f'New tutor request from '
                        f'{student_name} to '
                        f'{tutor_name}.'
                    )
                )

            messages.success(
                request,
                'Tutor request sent successfully.'
            )

            return redirect(
                'my_requests'
            )

    else:

        form = BookingForm()


    return render(
        request,
        'booking.html',
        {
            'form': form,
            'tutor': tutor
        }
    )


# ==================================================
# STUDENT MY REQUESTS
# ==================================================

@login_required
def my_requests(request):

    requests = Booking.objects.filter(
        student=request.user
    ).order_by(
        '-created_at'
    )

    reviewed_tutor_ids = set(
        Review.objects.filter(
            student=request.user
        ).values_list(
            'tutor_id',
            flat=True
        )
    )

    return render(
        request,
        'my_requests.html',
        {
            'requests': requests,
            'reviewed_tutor_ids': reviewed_tutor_ids,
        }
    )


# ==================================================
# TUTOR REQUESTS
# ==================================================

@login_required
def tutor_requests(request):

    tutor = get_object_or_404(
        TutorProfile,
        user=request.user
    )

    requests = Booking.objects.filter(
        tutor=tutor
    ).order_by(
        '-created_at'
    )

    return render(
        request,
        'tutor_requests.html',
        {
            'requests': requests
        }
    )


# ==================================================
# ACCEPT REQUEST
# ==================================================

@login_required
def accept_request(
    request,
    booking_id
):

    booking = get_object_or_404(
        Booking,
        id=booking_id
    )

    # ------------------------------------------
    # ONLY TUTOR OR ADMIN
    # ------------------------------------------

    if not (
        request.user == booking.tutor.user
        or request.user.is_staff
    ):

        messages.error(
            request,
            'You are not allowed to accept this request.'
        )

        return redirect(
            'notifications'
        )

    # ------------------------------------------
    # ACCEPT
    # ------------------------------------------

    if booking.status == 'Pending':

        booking.status = 'Accepted'

        booking.save(
            update_fields=['status']
        )

        tutor_name = (
            booking.tutor.user.get_full_name()
            or booking.tutor.user.username
        )

        # ------------------------------------------
        # NOTIFY STUDENT
        # ------------------------------------------

        Notification.objects.create(
            user=booking.student,
            booking=booking,
            notification_type='accepted',
            message=(
                f'{tutor_name} accepted '
                f'your tutor request.'
            )
        )

        messages.success(
            request,
            'Tutor request accepted successfully.'
        )

    else:

        messages.info(
            request,
            'This request has already been processed.'
        )

    return redirect(
        'notifications'
    )


# ==================================================
# REJECT REQUEST
# ==================================================

@login_required
def reject_request(
    request,
    booking_id
):

    booking = get_object_or_404(
        Booking,
        id=booking_id
    )

    # ------------------------------------------
    # ONLY TUTOR OR ADMIN
    # ------------------------------------------

    if not (
        request.user == booking.tutor.user
        or request.user.is_staff
    ):

        messages.error(
            request,
            'You are not allowed to reject this request.'
        )

        return redirect(
            'notifications'
        )

    # ------------------------------------------
    # REJECT
    # ------------------------------------------

    if booking.status == 'Pending':

        booking.status = 'Rejected'

        booking.save(
            update_fields=['status']
        )

        tutor_name = (
            booking.tutor.user.get_full_name()
            or booking.tutor.user.username
        )

        # ------------------------------------------
        # NOTIFY STUDENT
        # ------------------------------------------

        Notification.objects.create(
            user=booking.student,
            booking=booking,
            notification_type='rejected',
            message=(
                f'{tutor_name} rejected '
                f'your tutor request.'
            )
        )

        messages.info(
            request,
            'Tutor request rejected.'
        )

    else:

        messages.info(
            request,
            'This request has already been processed.'
        )

    return redirect(
        'notifications'
    )


# ==================================================
# NOTIFICATION LIST
# ==================================================

@login_required
def notifications(request):

    user_notifications = Notification.objects.filter(
        user=request.user
    ).order_by(
        '-created_at'
    )

    return render(
        request,
        'notifications.html',
        {
            'notifications': user_notifications
        }
    )


# ==================================================
# NOTIFICATION DETAIL
# ==================================================

@login_required
def notification_detail(
    request,
    notification_id
):

    notification = get_object_or_404(
        Notification,
        id=notification_id,
        user=request.user
    )

    # ------------------------------------------
    # MARK SINGLE NOTIFICATION AS READ
    # ------------------------------------------

    if not notification.is_read:

        notification.is_read = True

        notification.save(
            update_fields=['is_read']
        )

    booking = notification.booking

    return render(
        request,
        'notification_detail.html',
        {
            'notification': notification,
            'booking': booking,
        }
    )


# ==================================================
# MARK ALL AS READ
# ==================================================

@login_required
def mark_notifications_read(request):

    if request.method == 'POST':

        Notification.objects.filter(
            user=request.user,
            is_read=False
        ).update(
            is_read=True
        )

    return redirect(
        'notifications'
    )


# ==================================================
# ADD REVIEW
# ==================================================

@login_required
def add_review(
    request,
    booking_id
):

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        student=request.user
    )

    # ------------------------------------------
    # CHECK BOOKING STATUS
    # ------------------------------------------

    if booking.status not in [
        'Accepted',
        'Completed'
    ]:

        messages.warning(
            request,
            'You can review the tutor only after the request is accepted.'
        )

        return redirect(
            'my_requests'
        )

    # ------------------------------------------
    # PREVENT DUPLICATE REVIEW
    # ------------------------------------------

    existing_review = Review.objects.filter(
        tutor=booking.tutor,
        student=request.user
    ).first()

    if existing_review:

        messages.info(
            request,
            'You have already reviewed this tutor.'
        )

        return redirect(
            'my_requests'
        )

    # ------------------------------------------
    # REVIEW FORM
    # ------------------------------------------

    if request.method == 'POST':

        form = ReviewForm(
            request.POST
        )

        if form.is_valid():

            review = form.save(
                commit=False
            )

            review.tutor = booking.tutor
            review.student = request.user

            review.save()

            student_name = (
                request.user.get_full_name()
                or request.user.username
            )

            tutor_name = (
                booking.tutor.user.get_full_name()
                or booking.tutor.user.username
            )

            # ------------------------------------------
            # NOTIFY ADMINS
            # ------------------------------------------

            admin_users = User.objects.filter(
                is_staff=True,
                is_active=True
            )

            for admin_user in admin_users:

                Notification.objects.create(
                    user=admin_user,
                    booking=booking,
                    notification_type='review',
                    message=(
                        f'New review submitted by '
                        f'{student_name} for '
                        f'{tutor_name}.'
                    )
                )

            messages.success(
                request,
                'Your review has been submitted successfully.'
            )

            return redirect(
                'my_requests'
            )

    else:

        form = ReviewForm()


    return render(
        request,
        'add_review.html',
        {
            'form': form,
            'booking': booking,
            'tutor': booking.tutor,
        }
    )