from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import (
    Appointment, ContactMessage, Patient, Service,
    GalleryImage, Testimonial, FAQ, HospitalInfo, DoctorProfile, VisitHistory
)


class AppointmentForm(forms.ModelForm):
    appointment_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
        }),
        label='Appointment Date'
    )

    class Meta:
        model = Appointment
        fields = ['parent_name', 'child_name', 'mobile', 'age',
                  'appointment_date', 'appointment_time', 'reason']
        widgets = {
            'parent_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Parent's Full Name",
            }),
            'child_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Child's Full Name",
            }),
            'mobile': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '10-digit Mobile Number',
                'pattern': '[0-9]{10}',
            }),
            'age': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Child Age (in years)',
                'min': 0,
                'max': 18,
            }),
            'appointment_time': forms.Select(attrs={
                'class': 'form-select',
            }),
            'reason': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Briefly describe the reason for visit...',
                'rows': 3,
            }),
        }
        labels = {
            'parent_name': "Parent's Name",
            'child_name': "Child's Name",
            'mobile': 'Mobile Number',
            'age': 'Child Age (years)',
            'appointment_time': 'Preferred Time',
            'reason': 'Reason for Visit',
        }

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile', '')
        if not mobile.isdigit():
            raise ValidationError('Mobile number must contain only digits.')
        if len(mobile) != 10:
            raise ValidationError('Mobile number must be exactly 10 digits.')
        return mobile

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is not None and (age < 0 or age > 18):
            raise ValidationError('Child age must be between 0 and 18 years.')
        return age

    def clean_appointment_date(self):
        date = self.cleaned_data.get('appointment_date')
        if date and date < timezone.now().date():
            raise ValidationError('Appointment date cannot be in the past.')
        return date

    def clean(self):
        cleaned_data = super().clean()
        apt_date = cleaned_data.get('appointment_date')
        apt_time = cleaned_data.get('appointment_time')
        mobile = cleaned_data.get('mobile')

        if apt_date and apt_time and mobile:
            # Check for duplicate pending/confirmed for same mobile on same date+time
            qs = Appointment.objects.filter(
                mobile=mobile,
                appointment_date=apt_date,
                appointment_time=apt_time,
                status__in=['pending', 'confirmed']
            )
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError(
                    'An active appointment already exists for this mobile number '
                    'on the selected date and time slot. Please choose a different slot.'
                )
        return cleaned_data


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Full Name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Email Address',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Phone Number (Optional)',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your message here...',
                'rows': 5,
            }),
        }


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'mobile', 'age', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Patient's Full Name"}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10-digit Mobile'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 18}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Address'}),
        }

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile', '')
        if not mobile.isdigit():
            raise ValidationError('Mobile number must contain only digits.')
        if len(mobile) != 10:
            raise ValidationError('Mobile number must be exactly 10 digits.')
        return mobile


class VisitHistoryForm(forms.ModelForm):
    class Meta:
        model = VisitHistory
        fields = ['visit_date', 'diagnosis', 'prescription', 'weight', 'notes']
        widgets = {
            'visit_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'diagnosis': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Primary diagnosis / complaint'}),
            'prescription': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Medicines, dosage...'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Weight in kg', 'step': '0.01'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Additional notes...'}),
        }


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['title', 'description', 'icon', 'image', 'order', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'icon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. bi-heart-pulse'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class GalleryImageForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ['image', 'title', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Image Title'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category'}),
        }


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['patient_name', 'feedback', 'rating', 'is_active']
        widgets = {
            'patient_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Patient / Parent Name'}),
            'feedback': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Write feedback...'}),
            'rating': forms.Select(
                choices=[(i, f'{i} Star{"s" if i > 1 else ""}') for i in range(1, 6)],
                attrs={'class': 'form-select'}
            ),
        }


class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['question', 'answer', 'order', 'is_active']
        widgets = {
            'question': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Frequently asked question'}),
            'answer': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Detailed answer...'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class HospitalInfoForm(forms.ModelForm):
    class Meta:
        model = HospitalInfo
        fields = [
            'name', 'tagline', 'address', 'mobile', 'whatsapp',
            'email', 'reg_no', 'opd_morning', 'opd_evening',
            'working_days', 'holiday', 'map_embed_url'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'tagline': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'whatsapp': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'reg_no': forms.TextInput(attrs={'class': 'form-control'}),
            'opd_morning': forms.TextInput(attrs={'class': 'form-control'}),
            'opd_evening': forms.TextInput(attrs={'class': 'form-control'}),
            'working_days': forms.TextInput(attrs={'class': 'form-control'}),
            'holiday': forms.TextInput(attrs={'class': 'form-control'}),
            'map_embed_url': forms.URLInput(attrs={'class': 'form-control'}),
        }


class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = DoctorProfile
        fields = [
            'name', 'qualification', 'specialization', 'experience',
            'consultation_fee', 'image', 'about', 'reg_no', 'languages'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'qualification': forms.TextInput(attrs={'class': 'form-control'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control'}),
            'experience': forms.NumberInput(attrs={'class': 'form-control'}),
            'consultation_fee': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'about': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'reg_no': forms.TextInput(attrs={'class': 'form-control'}),
            'languages': forms.TextInput(attrs={'class': 'form-control'}),
        }


class AppointmentStatusForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
