from django import forms
from .models import Appointment, ContactMessage, Patient, Service, GalleryImage


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
        mobile = self.cleaned_data.get('mobile')
        if not mobile.isdigit():
            raise forms.ValidationError('Mobile number must contain only digits.')
        if len(mobile) != 10:
            raise forms.ValidationError('Mobile number must be exactly 10 digits.')
        return mobile

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is not None and (age < 0 or age > 18):
            raise forms.ValidationError('Child age must be between 0 and 18 years.')
        return age


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
        mobile = self.cleaned_data.get('mobile')
        if not mobile.isdigit():
            raise forms.ValidationError('Mobile number must contain only digits.')
        if len(mobile) != 10:
            raise forms.ValidationError('Mobile number must be exactly 10 digits.')
        return mobile


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


class AppointmentStatusForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
