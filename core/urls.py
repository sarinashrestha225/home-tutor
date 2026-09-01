from django.urls import path

from .views import (
    home,
    admin_dashboard,
)


urlpatterns = [

    # =========================
    # HOME
    # =========================

    path(
        '',
        home,
        name='home'
    ),


    # =========================
    # CUSTOM ADMIN DASHBOARD
    # =========================

    path(
        'admin-dashboard/',
        admin_dashboard,
        name='admin_dashboard'
    ),

]