from django.urls import path

from .views import (
    send_request,
    my_requests,
    tutor_requests,
    accept_request,
    reject_request,
    notifications,
    notification_detail,
    mark_notifications_read,
    add_review,
)


urlpatterns = [

    # ==========================================
    # SEND REQUEST
    # ==========================================

    path(
        'request/<int:tutor_id>/',
        send_request,
        name='send_request'
    ),


    # ==========================================
    # STUDENT MY REQUESTS
    # ==========================================

    path(
        'my-requests/',
        my_requests,
        name='my_requests'
    ),


    # ==========================================
    # TUTOR REQUESTS
    # ==========================================

    path(
        'tutor-requests/',
        tutor_requests,
        name='tutor_requests'
    ),


    # ==========================================
    # ACCEPT
    # ==========================================

    path(
        'request/<int:booking_id>/accept/',
        accept_request,
        name='accept_request'
    ),


    # ==========================================
    # REJECT
    # ==========================================

    path(
        'request/<int:booking_id>/reject/',
        reject_request,
        name='reject_request'
    ),


    # ==========================================
    # NOTIFICATION LIST
    # ==========================================

    path(
        'notifications/',
        notifications,
        name='notifications'
    ),


    # ==========================================
    # NOTIFICATION DETAIL
    # ==========================================

    path(
        'notifications/<int:notification_id>/',
        notification_detail,
        name='notification_detail'
    ),


    # ==========================================
    # MARK ALL READ
    # ==========================================

    path(
        'notifications/read/',
        mark_notifications_read,
        name='mark_notifications_read'
    ),


    # ==========================================
    # REVIEW
    # ==========================================

    path(
        'review/<int:booking_id>/',
        add_review,
        name='add_review'
    ),

]