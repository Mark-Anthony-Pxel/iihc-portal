from django import forms
from .models import Teacher, Student, Contact, Lesson, Event, Resources, Announcement, Schedule, Deadline
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'first_name', 'middle_name', 'last_name', 'address', 'phone', 
            'email', 'mother_tongue', 'religion', 'sex', 'learning_mode', 
            'strand', 'tvl_track', 'payment_method', 'emergency_contact_name', 
            'emergency_contact_relationship', 'emergency_contact_phone', 
            'emergency_contact_email'
        ]

    # Custom validation for TVL strand
    def clean(self):
        cleaned_data = super().clean()
        strand = cleaned_data.get('strand')
        tvl_track = cleaned_data.get('tvl_track')
        if strand == 'TVL' and not tvl_track:
            self.add_error('tvl_track', 'Please specify the TVL track if the strand is TVL.')
        return cleaned_data

class TeacherForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    subject = forms.CharField(max_length=50)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    password_confirmation = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = Teacher
        fields = ['subject', 'teacher_strand', 'tvl_options']  # Exclude user fields

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")

        if password and password_confirmation and password != password_confirmation:
            raise forms.ValidationError("Passwords do not match.")

    def save(self, commit=True):
        # Create the User instance
        user = User(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            is_staff=True,
            is_superuser=False
        )
        user.set_password(self.cleaned_data['password'])  # Hash the password
        if commit:
            user.save()  # Save the User instance

        # Create the Teacher instance
        teacher = super().save(commit=False)
        teacher.user = user  # Associate the User with the Teacher
        if commit:
            teacher.save()  # Save the Teacher instance
        return teacher

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'title', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email Address'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject of Your Message'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Type your message here...'}),
        }

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'description', 'attachment']

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'image', 'link']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class ResourcesForm(forms.ModelForm):
    class Meta:
        model = Resources
        fields = ['title', 'description', 'link']

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'description', 'link']

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['start_time', 'end_time', 'subject', 'teacher']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

class DeadlineForm(forms.ModelForm):
    class Meta:
        model = Deadline
        fields = ['description', 'date_time']
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }




