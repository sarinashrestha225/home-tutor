from django.contrib import admin
from django.urls import path, include


urlpatterns = [

    path(
        'admin/',
        admin.site.urls
    ),

    path(
        '',
        include('core.urls')
    ),

    path(
        '',
        include('accounts.urls')
    ),

    path(
        'tutor/',
        include('tutors.urls')
    ),

    path(
        'booking/',
        include('bookings.urls')
    ),
]