from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (
    register,
    user_login,
    user_logout,
    student_dashboard,
    tutor_dashboard,
    student_profile,
)


urlpatterns = [

    path(
        'register/',
        register,
        name='register'
    ),

    path(
        'login/',
        user_login,
        name='login'
    ),

    path(
        'logout/',
        user_logout,
        name='logout'
    ),

    path(
        'student-dashboard/',
        student_dashboard,
        name='student_dashboard'
    ),

    path(
        'tutor-dashboard/',
        tutor_dashboard,
        name='tutor_dashboard'
    ),

    path(
        'student-profile/',
        student_profile,
        name='student_profile'
    ),

    # ==========================================
    # FORGOT PASSWORD
    # ==========================================

    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='password_reset.html',
            email_template_name='password_reset_email.html',
            subject_template_name='password_reset_subject.txt',
            success_url='/password-reset/done/'
        ),
        name='password_reset'
    ),

    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='password_reset_done.html'
        ),
        name='password_reset_done'
    ),

    path(
        'password-reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='password_reset_confirm.html',
            success_url='/password-reset/complete/'
        ),
        name='password_reset_confirm'
    ),

    path(
        'password-reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
]