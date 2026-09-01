from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking

        fields = [
            'class_name',
            'subject',
            'preferred_time',
            'message',
        ]

        widgets = {
            'class_name': forms.Select(
                choices=[
                    ('Class 2', 'Class 2'),
                    ('Class 3', 'Class 3'),
                    ('Class 4', 'Class 4'),
                    ('Class 5', 'Class 5'),
                    ('Class 6', 'Class 6'),
                    ('Class 7', 'Class 7'),
                    ('Class 8', 'Class 8'),
                    ('Class 9', 'Class 9'),
                    ('Class 10', 'Class 10'),
                ],
                attrs={
                    'class': 'form-select'
                }
            ),

            'subject': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'e.g. Mathematics'
                }
            ),

            'preferred_time': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'e.g. 5 PM - 7 PM'
                }
            ),

            'message': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Write a message to the tutor',
                    'rows': 4
                }
            ),
        }