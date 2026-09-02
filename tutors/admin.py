from django.contrib import admin
from django import forms

from .models import TutorProfile, Subject, Review


# ==================================================
# SUBJECT ADMIN
# ==================================================

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
    )

    search_fields = (
        'name',
    )

    ordering = (
        'name',
    )


# ==================================================
# TUTOR PROFILE FORM
# ==================================================

class TutorProfileForm(forms.ModelForm):

    class Meta:
        model = TutorProfile

        fields = [
            'user',
            'qualification',
            'experience',
            'classes',
            'subjects',
            'location',
            'latitude',
            'longitude',
            'fee',
            'available_time',
            'is_verified',
        ]

        widgets = {

            'qualification': forms.TextInput(
                attrs={
                    'class': 'vTextField',
                    'placeholder': 'Example: Bachelor in Science'
                }
            ),

            'experience': forms.NumberInput(
                attrs={
                    'class': 'vIntegerField',
                    'min': 0,
                    'placeholder': 'Years of experience'
                }
            ),

            'classes': forms.TextInput(
                attrs={
                    'class': 'vTextField',
                    'placeholder': 'Example: Class 4, Class 5, Class 6'
                }
            ),

            'subjects': forms.SelectMultiple(
                attrs={
                    'class': 'selectfilter'
                }
            ),

            'location': forms.TextInput(
                attrs={
                    'class': 'vTextField',
                    'placeholder': 'Example: Satungal, Kathmandu'
                }
            ),

            'latitude': forms.NumberInput(
                attrs={
                    'class': 'vTextField',
                    'step': 'any',
                    'placeholder': 'Latitude'
                }
            ),

            'longitude': forms.NumberInput(
                attrs={
                    'class': 'vTextField',
                    'step': 'any',
                    'placeholder': 'Longitude'
                }
            ),

            'fee': forms.NumberInput(
                attrs={
                    'class': 'vTextField',
                    'min': 0,
                    'step': '0.01',
                    'placeholder': 'Fee per hour'
                }
            ),

            'available_time': forms.TextInput(
                attrs={
                    'class': 'vTextField',
                    'placeholder': 'Example: 5 PM - 7 PM'
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['user'].required = True
        self.fields['user'].empty_label = 'Select a user'


# ==================================================
# TUTOR PROFILE ADMIN
# ==================================================

@admin.register(TutorProfile)
class TutorProfileAdmin(admin.ModelAdmin):

    form = TutorProfileForm

    list_display = (
        'user',
        'qualification',
        'experience',
        'fee',
        'is_verified',
    )

    list_filter = (
        'is_verified',
    )

    search_fields = (
        'user__username',
        'user__first_name',
        'user__last_name',
        'user__email',
        'qualification',
        'location',
    )

    ordering = (
        '-id',
    )

    # ==================================================
    # ACCEPT / REJECT ACTIONS
    # ==================================================

    actions = [
        'accept_tutors',
        'reject_tutors',
    ]

    @admin.action(description='Accept selected tutors')
    def accept_tutors(self, request, queryset):

        updated = queryset.update(
            is_verified=True
        )

        self.message_user(
            request,
            f'{updated} tutor(s) accepted successfully.'
        )

    @admin.action(description='Reject selected tutors')
    def reject_tutors(self, request, queryset):

        updated = queryset.update(
            is_verified=False
        )

        self.message_user(
            request,
            f'{updated} tutor(s) rejected.'
        )


# ==================================================
# REVIEW ADMIN
# ==================================================

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = (
        'student',
        'tutor',
        'rating',
        'comment',
    )

    list_filter = (
        'rating',
    )

    search_fields = (
        'student__username',
        'student__first_name',
        'student__last_name',
        'tutor__user__username',
        'tutor__user__first_name',
        'tutor__user__last_name',
        'comment',
    )

    ordering = (
        '-id',
    )