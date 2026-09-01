from django.urls import path

from .views import (
    tutor_profile,
    tutor_list,
)


urlpatterns = [

    # Tutor profile
    path(
        'profile/',
        tutor_profile,
        name='tutor_profile'
    ),

    # Tutor list
    path(
        'list/',
        tutor_list,
        name='tutor_list'
    ),

]