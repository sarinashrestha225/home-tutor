from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User

from .forms import RegisterForm, StudentProfileForm
from .models import UserProfile

from bookings.models import Notification


# ==================================================
# CREATE UNIQUE USERNAME
# ==================================================

def generate_unique_username(first_name, last_name):

    first_name = (first_name or '').strip().lower()
    last_name = (last_name or '').strip().lower()

    base_username = (
        first_name + last_name
    ).replace(' ', '')

    if not base_username:
        base_username = 'user'

    username = base_username
    number = 2

    while User.objects.filter(
        username=username
    ).exists():

        username = f'{base_username}{number}'
        number += 1

    return username


# ==================================================
# REGISTER
# ==================================================

def register(request):

    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            first_name = form.cleaned_data.get(
                'first_name',
                ''
            )

            last_name = form.cleaned_data.get(
                'last_name',
                ''
            )

            email = form.cleaned_data.get(
                'email',
                ''
            )

            phone = form.cleaned_data.get(
                'phone',
                ''
            )

            role = form.cleaned_data.get(
                'role'
            )

            password = form.cleaned_data.get(
                'password'
            )


            # ------------------------------------------
            # AUTOMATIC UNIQUE USERNAME
            # ------------------------------------------

            username = generate_unique_username(
                first_name,
                last_name
            )


            # ------------------------------------------
            # CREATE USER
            # ------------------------------------------

            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
            )


            # ------------------------------------------
            # CREATE PROFILE
            # ------------------------------------------

            UserProfile.objects.create(
                user=user,
                role=role,
                phone=phone
            )


            # ------------------------------------------
            # ADMIN NOTIFICATION
            # ------------------------------------------

            admin_users = User.objects.filter(
                is_staff=True,
                is_active=True
            )

            display_name = (
                user.get_full_name()
                or user.username
            )

            for admin_user in admin_users:

                Notification.objects.create(
                    user=admin_user,
                    notification_type='registered',
                    message=(
                        f'New {role} registered: '
                        f'{display_name}.'
                    )
                )


            # ------------------------------------------
            # LOGIN NEW USER
            # ------------------------------------------

            login(
                request,
                user
            )


            # ------------------------------------------
            # REDIRECT BY ROLE
            # ------------------------------------------

            if role == 'tutor':

                return redirect(
                    'tutor_dashboard'
                )

            return redirect(
                'student_dashboard'
            )

    else:

        form = RegisterForm()


    return render(
        request,
        'register.html',
        {
            'form': form
        }
    )


# ==================================================
# LOGIN
# ==================================================

def user_login(request):

    if request.user.is_authenticated:

        # Already logged in
        return redirect('/')


    if request.method == 'POST':

        username = request.POST.get(
            'username',
            ''
        ).strip()

        password = request.POST.get(
            'password',
            ''
        )


        # ------------------------------------------
        # CHECK USERNAME
        # ------------------------------------------

        if not username:

            return render(
                request,
                'login.html',
                {
                    'error': 'Please enter your username.'
                }
            )


        # ------------------------------------------
        # CHECK PASSWORD
        # ------------------------------------------

        if not password:

            return render(
                request,
                'login.html',
                {
                    'error': 'Please enter your password.'
                }
            )


        # ------------------------------------------
        # AUTHENTICATE
        # ------------------------------------------

        user = authenticate(
            request,
            username=username,
            password=password
        )


        if user is None:

            return render(
                request,
                'login.html',
                {
                    'error': (
                        'Invalid username or password.'
                    ),
                    'entered_username': username
                }
            )


        # ------------------------------------------
        # LOGIN
        # ------------------------------------------

        login(
            request,
            user
        )


        # ------------------------------------------
        # GET / CREATE PROFILE
        # ------------------------------------------

        profile, created = (
            UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'role': 'student'
                }
            )
        )


        # ------------------------------------------
        # NEXT URL
        # ------------------------------------------

        next_url = (
            request.POST.get('next')
            or request.GET.get('next')
        )


        # Only allow local URLs
        if (
            next_url
            and next_url.startswith('/')
            and not next_url.startswith('//')
        ):

            return redirect(
                next_url
            )


        # ------------------------------------------
        # TUTOR
        # ------------------------------------------

        if profile.role == 'tutor':

            return redirect(
                'tutor_dashboard'
            )


        # ------------------------------------------
        # STUDENT
        # ------------------------------------------

        return redirect(
            'student_dashboard'
        )


    # ------------------------------------------
    # GET REQUEST
    # ------------------------------------------

    next_url = request.GET.get(
        'next',
        ''
    )

    return render(
        request,
        'login.html',
        {
            'next': next_url
        }
    )


# ==================================================
# LOGOUT
# ==================================================

def user_logout(request):

    logout(request)

    return redirect(
        'home'
    )


# ==================================================
# STUDENT DASHBOARD
# ==================================================

def student_dashboard(request):

    if not request.user.is_authenticated:

        return redirect(
            'login'
        )


    profile, created = (
        UserProfile.objects.get_or_create(
            user=request.user,
            defaults={
                'role': 'student'
            }
        )
    )


    # ------------------------------------------
    # SAVE GPS
    # ------------------------------------------

    if request.method == 'POST':

        latitude = request.POST.get(
            'latitude'
        )

        longitude = request.POST.get(
            'longitude'
        )

        location = request.POST.get(
            'location'
        )


        if latitude and longitude:

            try:

                profile.latitude = float(
                    latitude
                )

                profile.longitude = float(
                    longitude
                )

                if location:
                    profile.location = location

                profile.save()

            except (
                ValueError,
                TypeError
            ):

                pass


    return render(
        request,
        'student_dashboard.html',
        {
            'profile': profile
        }
    )


# ==================================================
# STUDENT PROFILE
# ==================================================

def student_profile(request):

    if not request.user.is_authenticated:

        return redirect(
            'login'
        )


    profile, created = (
        UserProfile.objects.get_or_create(
            user=request.user,
            defaults={
                'role': 'student'
            }
        )
    )


    if request.method == 'POST':

        form = StudentProfileForm(
            request.POST,
            instance=profile
        )

        if form.is_valid():

            form.save()

            return redirect(
                'student_dashboard'
            )

    else:

        form = StudentProfileForm(
            instance=profile
        )


    return render(
        request,
        'student_profile.html',
        {
            'form': form
        }
    )


# ==================================================
# TUTOR DASHBOARD
# ==================================================

def tutor_dashboard(request):

    if not request.user.is_authenticated:

        return redirect(
            'login'
        )


    from tutors.models import TutorProfile


    tutor_profile = TutorProfile.objects.filter(
        user=request.user
    ).first()


    return render(
        request,
        'tutor_dashboard.html',
        {
            'tutor_profile': tutor_profile
        }
    )