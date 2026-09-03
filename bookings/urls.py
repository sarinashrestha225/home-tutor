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

    path(
        'request/<int:tutor_id>/',
        send_request,
        name='send_request'
    ),

    path(
        'my-requests/',
        my_requests,
        name='my_requests'
    ),

    path(
        'tutor-requests/',
        tutor_requests,
        name='tutor_requests'
    ),

    path(
        'request/<int:booking_id>/accept/',
        accept_request,
        name='accept_request'
    ),

    path(
        'request/<int:booking_id>/reject/',
        reject_request,
        name='reject_request'
    ),

    path(
        'notifications/',
        notifications,
        name='notifications'
    ),

    path(
        'notifications/<int:notification_id>/',
        notification_detail,
        name='notification_detail'
    ),

    path(
        'notifications/read/',
        mark_notifications_read,
        name='mark_notifications_read'
    ),

    path(
        'review/<int:booking_id>/',
        add_review,
        name='add_review'
    ),

]