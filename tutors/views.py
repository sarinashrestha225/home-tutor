from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from math import radians, sin, cos, sqrt, atan2

from .models import TutorProfile, Review
from .forms import TutorProfileForm


# ==================================================
# TUTOR PROFILE
# ==================================================

@login_required
def tutor_profile(request):

    profile, created = TutorProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == 'POST':

        form = TutorProfileForm(
            request.POST,
            instance=profile
        )

        if form.is_valid():

            tutor_profile = form.save(
                commit=False
            )

            tutor_profile.user = request.user

            # ==============================
            # SAVE GPS
            # ==============================

            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')

            if latitude:
                try:
                    tutor_profile.latitude = float(latitude)
                except (ValueError, TypeError):
                    pass

            if longitude:
                try:
                    tutor_profile.longitude = float(longitude)
                except (ValueError, TypeError):
                    pass

            tutor_profile.save()

            form.save_m2m()

            return redirect(
                '/tutor-dashboard/'
            )

    else:

        form = TutorProfileForm(
            instance=profile
        )

    return render(
        request,
        'tutor_profile.html',
        {
            'form': form
        }
    )


# ==================================================
# TUTOR LIST
# NORMAL SEARCH
# CLASS
# SUBJECT
# SEARCH
# DISTANCE
# RATING
# SORT
# ==================================================

def tutor_list(request):

    from accounts.models import UserProfile

    # ==================================================
    # VERIFIED TUTORS
    # ==================================================

    tutors = TutorProfile.objects.filter(
        is_verified=True
    ).distinct()


    # ==================================================
    # GET FILTERS
    # ==================================================

    selected_class = request.GET.get(
        'class',
        ''
    ).strip()

    selected_subject = request.GET.get(
        'subject',
        ''
    ).strip()

    search_query = request.GET.get(
        'search',
        ''
    ).strip()

    sort_by = request.GET.get(
        'sort',
        'distance'
    ).strip()


    # ==================================================
    # CLASS FILTER
    # ==================================================

    if selected_class:

        tutors = tutors.filter(
            classes__icontains=selected_class
        )


    # ==================================================
    # SUBJECT FILTER
    # ==================================================

    if selected_subject:

        tutors = tutors.filter(
            subjects__name__iexact=selected_subject
        )


    # ==================================================
    # SEARCH
    # ==================================================

    if search_query:

        tutors = tutors.filter(

            Q(
                user__first_name__icontains=search_query
            )

            |

            Q(
                user__last_name__icontains=search_query
            )

            |

            Q(
                user__username__icontains=search_query
            )

            |

            Q(
                location__icontains=search_query
            )

            |

            Q(
                qualification__icontains=search_query
            )

        )


    # ==================================================
    # STUDENT PROFILE
    # ==================================================

    student_profile = None

    if request.user.is_authenticated:

        student_profile = UserProfile.objects.filter(
            user=request.user
        ).first()


    # ==================================================
    # STUDENT GPS
    # ==================================================

    student_latitude = None
    student_longitude = None

    if student_profile:

        student_latitude = student_profile.latitude
        student_longitude = student_profile.longitude


    # ==================================================
    # TUTOR DATA
    # ==================================================

    tutor_data = []


    # ==================================================
    # CALCULATE DISTANCE
    # ==================================================

    for tutor in tutors:

        distance = None


        if (
            student_latitude is not None
            and student_longitude is not None
            and tutor.latitude is not None
            and tutor.longitude is not None
        ):

            # Student coordinates
            lat1 = radians(
                float(student_latitude)
            )

            lon1 = radians(
                float(student_longitude)
            )


            # Tutor coordinates
            lat2 = radians(
                float(tutor.latitude)
            )

            lon2 = radians(
                float(tutor.longitude)
            )


            # Difference
            dlat = lat2 - lat1
            dlon = lon2 - lon1


            # Haversine formula
            a = (
                sin(dlat / 2) ** 2
                +
                cos(lat1)
                * cos(lat2)
                * sin(dlon / 2) ** 2
            )


            c = 2 * atan2(
                sqrt(a),
                sqrt(1 - a)
            )


            earth_radius = 6371


            distance = (
                earth_radius * c
            )


        # ==================================================
        # RATING
        # ==================================================

        reviews = Review.objects.filter(
            tutor=tutor
        )

        review_count = reviews.count()

        average_rating = 0


        if review_count > 0:

            total_rating = sum(
                review.rating
                for review in reviews
            )

            average_rating = (
                total_rating /
                review_count
            )


        # ==================================================
        # ADD TUTOR
        # ==================================================

        tutor_data.append(
            {
                'tutor': tutor,

                'distance': distance,

                'average_rating': round(
                    average_rating,
                    1
                ),

                'review_count': review_count,
            }
        )


    # ==================================================
    # SORT
    # ==================================================

    if sort_by == 'rating':

        tutor_data.sort(
            key=lambda item: (
                item['average_rating']
            ),
            reverse=True
        )


    elif sort_by == 'fee_low':

        tutor_data.sort(
            key=lambda item: (
                float(item['tutor'].fee)
            )
        )


    elif sort_by == 'fee_high':

        tutor_data.sort(
            key=lambda item: (
                float(item['tutor'].fee)
            ),
            reverse=True
        )


    elif sort_by == 'distance':

        # Tutors with GPS first
        tutor_data.sort(
            key=lambda item: (
                item['distance']
                if item['distance'] is not None
                else 999999
            )
        )


    return render(
        request,
        'tutor_list.html',
        {
            'tutor_data': tutor_data,

            'selected_class': selected_class,

            'selected_subject': selected_subject,

            'search_query': search_query,

            'sort_by': sort_by,
        }
    )