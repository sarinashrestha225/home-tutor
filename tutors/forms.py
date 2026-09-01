from django import forms

from .models import TutorProfile, Subject, Review


# ==================================================
# AVAILABLE TIME OPTIONS
# ==================================================

TIME_CHOICES = [

    # -----------------------------
    # MORNING
    # -----------------------------

    ('6 AM - 7 AM', '6 AM - 7 AM'),
    ('7 AM - 8 AM', '7 AM - 8 AM'),
    ('6 AM - 8 AM', '6 AM - 8 AM'),

    # -----------------------------
    # EVENING - 1 HOUR
    # -----------------------------

    ('4 PM - 5 PM', '4 PM - 5 PM'),
    ('5 PM - 6 PM', '5 PM - 6 PM'),
    ('6 PM - 7 PM', '6 PM - 7 PM'),
    ('7 PM - 8 PM', '7 PM - 8 PM'),
    ('8 PM - 9 PM', '8 PM - 9 PM'),

    # -----------------------------
    # EVENING - 2 HOURS
    # -----------------------------

    ('4 PM - 6 PM', '4 PM - 6 PM'),
    ('5 PM - 7 PM', '5 PM - 7 PM'),
    ('6 PM - 8 PM', '6 PM - 8 PM'),
    ('7 PM - 9 PM', '7 PM - 9 PM'),
]


# ==================================================
# TUTOR PROFILE FORM
# ==================================================

class TutorProfileForm(forms.ModelForm):

    # ------------------------------------------
    # CLASSES
    # ------------------------------------------

    CLASSES_CHOICES = [
        ('Class 2', 'Class 2'),
        ('Class 3', 'Class 3'),
        ('Class 4', 'Class 4'),
        ('Class 5', 'Class 5'),
        ('Class 6', 'Class 6'),
        ('Class 7', 'Class 7'),
        ('Class 8', 'Class 8'),
        ('Class 9', 'Class 9'),
        ('Class 10', 'Class 10'),
    ]


    classes = forms.MultipleChoiceField(
        choices=CLASSES_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True
    )


    # ------------------------------------------
    # SUBJECTS
    # ------------------------------------------

    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all().order_by('name'),
        widget=forms.SelectMultiple(
            attrs={
                'class': 'form-select',
                'size': '9'
            }
        ),
        required=True
    )


    # ------------------------------------------
    # AVAILABLE TIME
    # ------------------------------------------

    available_time = forms.MultipleChoiceField(
        choices=TIME_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True
    )


    class Meta:

        model = TutorProfile

        fields = [
            'qualification',
            'experience',
            'classes',
            'subjects',
            'location',
            'latitude',
            'longitude',
            'fee',
            'available_time',
        ]


        widgets = {

            # --------------------------------------
            # QUALIFICATION
            # --------------------------------------

            'qualification': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': (
                        'Example: Bachelor in Computer Science'
                    )
                }
            ),


            # --------------------------------------
            # EXPERIENCE
            # --------------------------------------

            'experience': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Years of experience',
                    'min': 0
                }
            ),


            # --------------------------------------
            # LOCATION
            # --------------------------------------

            'location': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': (
                        'Example: Satungal, Kathmandu'
                    )
                }
            ),


            # --------------------------------------
            # LATITUDE
            # --------------------------------------

            'latitude': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'step': 'any',
                    'readonly': True
                }
            ),


            # --------------------------------------
            # LONGITUDE
            # --------------------------------------

            'longitude': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'step': 'any',
                    'readonly': True
                }
            ),


            # --------------------------------------
            # FEE
            # --------------------------------------

            'fee': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Fee per hour in Rs.',
                    'min': 0,
                    'step': '0.01'
                }
            ),
        }


    # ==================================================
    # INIT
    # ==================================================

    def __init__(self, *args, **kwargs):

        super().__init__(
            *args,
            **kwargs
        )


        # ------------------------------------------
        # CLASSES - CONVERT SAVED STRING TO LIST
        # ------------------------------------------

        if self.instance and self.instance.classes:

            saved_classes = [
                item.strip()
                for item in self.instance.classes.split(',')
                if item.strip()
            ]

            self.initial['classes'] = saved_classes


        # ------------------------------------------
        # AVAILABLE TIME - CONVERT SAVED STRING
        # ------------------------------------------

        if (
            self.instance
            and self.instance.available_time
        ):

            saved_times = [
                item.strip()
                for item in self.instance.available_time.split(',')
                if item.strip()
            ]

            self.initial['available_time'] = saved_times


    # ==================================================
    # CLEAN CLASSES
    # ==================================================

    def clean_classes(self):

        classes = self.cleaned_data.get(
            'classes'
        )

        if not classes:

            raise forms.ValidationError(
                'Please select at least one class.'
            )

        return ', '.join(classes)


    # ==================================================
    # CLEAN AVAILABLE TIME
    # ==================================================

    def clean_available_time(self):

        times = self.cleaned_data.get(
            'available_time'
        )

        if not times:

            raise forms.ValidationError(
                'Please select at least one available time.'
            )

        return ', '.join(times)


# ==================================================
# REVIEW FORM
# ==================================================

class ReviewForm(forms.ModelForm):

    class Meta:

        model = Review

        fields = [
            'rating',
            'comment',
        ]

        widgets = {

            'rating': forms.Select(
                choices=[
                    (1, '⭐ 1'),
                    (2, '⭐⭐ 2'),
                    (3, '⭐⭐⭐ 3'),
                    (4, '⭐⭐⭐⭐ 4'),
                    (5, '⭐⭐⭐⭐⭐ 5'),
                ],
                attrs={
                    'class': 'form-select'
                }
            ),

            'comment': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': (
                        'Write your review...'
                    )
                }
            ),
        }