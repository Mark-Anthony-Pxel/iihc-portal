from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.contrib.auth.models import Group
import string
from django.contrib.auth.models import User
import random

class Student(models.Model):
    # Add the student_id field
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student', null=True, blank=True)  # Link student to user
    student_id = models.CharField(max_length=5, unique=True, editable=False, blank=True)

    # Existing fields
    PENDING = 'Pending'
    APPROVED = 'Approved'
    REJECTED = 'Rejected'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    ]

    SEX_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    LEARNING_MODE_CHOICES = [
        ('Modular', 'Modular'),
        ('Face to Face', 'Face to Face'),
        ('Online', 'Online'),
        ('Hybrid', 'Hybrid'),
    ]

    STRAND_CHOICES = [
        ('STEM', 'STEM (Science, Technology, Engineering, Mathematics)'),
        ('ABM', 'ABM (Accountancy, Business, and Management)'),
        ('HUMSS', 'HUMSS (Humanities and Social Sciences)'),
        ('GAS', 'GAS (General Academic Strand)'),
        ('TVL', 'TVL (Technical-Vocational-Livelihood)'),
    ]

    TVL_TRACK_CHOICES = [
        ('ICT', 'Information and Communications Technology (ICT)'),
        ('Home Economics', 'Home Economics'),
        ('Tourism', 'Tourism'),
        ('Agri-fishery Arts', 'Agri-fishery Arts (Soon)'),
        ('Industrial Arts', 'Industrial Arts (Soon)'),
        ('Entrepreneurship', 'Entrepreneurship (Soon)'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('Cash', 'Cash'),
        ('Bank Transfer', 'Bank Transfer'),
        ('Mobile Wallet', 'Mobile Wallet'),
    ]

    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30)
    address = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=50, unique=True)
    phone_validator = RegexValidator(
        regex=r'^(?:\+63|09)\d{9}$',
        message="Phone number must start with '+63' or '09' and be followed by 9 digits."
    )
    phone = models.CharField(validators=[phone_validator], max_length=13, blank=True, null=True)    
    mother_tongue = models.CharField(max_length=30, blank=True)
    religion = models.CharField(max_length=30, blank=True)
    sex = models.CharField(max_length=6, choices=SEX_CHOICES, blank=True)
    learning_mode = models.CharField(max_length=20, choices=LEARNING_MODE_CHOICES, blank=True)
    strand = models.CharField(max_length=20, choices=STRAND_CHOICES, blank=True)
    tvl_track = models.CharField(max_length=30, choices=TVL_TRACK_CHOICES, blank=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, blank=True)
    emergency_contact_name = models.CharField(max_length=50, blank=True)
    emergency_contact_relationship = models.CharField(max_length=20, blank=True)
    emergency_contact_phone = models.CharField(max_length=15, blank=True)
    emergency_contact_email = models.EmailField(blank=True)
    temp_password = models.CharField(max_length=128, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)

    def __str__(self):
        return f"{self.student_id} - {self.first_name} {self.middle_name} {self.last_name} ({self.status})"

    class Meta:
        ordering = ['last_name', 'first_name']
        indexes = [
            models.Index(fields=['student_id']),
            models.Index(fields=['email']),
        ]
        
    def generate_temp_password(self):
        """Generate a random temporary password."""
        length = 8
        characters = string.ascii_letters + string.digits + string.punctuation
        temp_password = ''.join(random.choice(characters) for _ in range(length))
        return temp_password

    def save(self, *args, **kwargs):
        if not self.student_id:
            # Generate a unique student ID
            last_student = Student.objects.order_by('-student_id').first()
            new_id = int(last_student.student_id) + 1 if last_student else 1
            self.student_id = f"{new_id:05d}"

        if self.status == self.APPROVED and not self.temp_password:
            # Generate a temp password if none exists
            self.temp_password = self.generate_temp_password()
            self.send_temp_password_email()

        super().save(*args, **kwargs)

    def create_user(self):
        """Create a User associated with the Student."""
        if not self.user:  # Ensure we only create a User if one doesn't already exist
            user = User.objects.create_user(
                username=self.email,  # Use the email as the username
                email=self.email,
                password=self.temp_password  # Assign the temporary password
            )
            self.user = user  # Ensure this links the user correctly to the student
            self.save()  # Save the student with the associated user
        else:
            print("User already exists for this student.")

    def send_temp_password_email(self):
        """Send an email with the temporary password."""
        try:
            subject = 'Your Temporary Password'
            message = (
                f"Hello {self.first_name},\n\n"
                f"Your email is {self.email},\n\n"
                f"Your temporary password is: {self.temp_password}\n\n"
                f"Please change it after logging in.\n\n"
                "Thank you!"
            )
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [self.email])
        except Exception as e:
            print(f"Failed to send email: {e}")  # Consider logging this error in production
        
    # Ensure the Student group exists and assign the user to it
        if self.user:
            student_group, created = Group.objects.get_or_create(name='Student')
            self.user.groups.add(student_group)

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher', blank=True)
    student_id = models.CharField(max_length=5, unique=True, editable=False, blank=True)
    username = models.CharField(max_length=50, editable=False, blank=True, unique=True)
    subject = models.CharField(max_length=50)
    password = models.CharField(max_length=128, blank=True)
    email = models.EmailField(unique=True, blank=True)
    first_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20, blank=True)

    STRANDS = [
        ('STEM', 'STEM'),
        ('ABM', 'ABM'),
        ('HUMSS', 'HUMSS'),
        ('GAS', 'GAS'),
        ('TVL', 'TVL'),
    ]
    teacher_strand = models.CharField(max_length=5, choices=STRANDS)

    TVL_OPTIONS = [
        ('HE - Cookery', 'HE - Cookery'),
        ('HE - Tourism', 'HE - Tourism'),
        ('ICT', 'ICT'),
    ]
    tvl_options = models.CharField(max_length=15, choices=TVL_OPTIONS, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.subject}"

    def save(self, *args, **kwargs):
        # Create or update the related user when saving the teacher instance
        if not self.user:
            # Generate a username if not provided
            if not self.username:
                self.username = self.email

            # Create a User instance
            user = User.objects.create_user(
                username=self.username,
                email=self.email,
                password=self.password if self.password else None,
                first_name=self.first_name,
                last_name=self.last_name
            )
            self.user = user

        # Hash the password if it's provided
        if self.password:
            self.user.set_password(self.password)
            self.user.save()

    # Ensure the Teacher group exists and assign the user to it
        teacher_group, created = Group.objects.get_or_create(name='Teacher')
        self.user.groups.add(teacher_group)
    
        super().save(*args, **kwargs)

class Contact(models.Model):
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=50)
    title = models.CharField(max_length=150, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.title}"

class Lesson(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    attachment = models.FileField(upload_to='lesson/attachments/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Event(models.Model):
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    date = models.DateTimeField(blank=True)
    image = models.ImageField(upload_to='events/images/', blank=True, null=True)  # Image field added
    link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.date})"

class Resources(models.Model):
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Announcement(models.Model):
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Schedule(models.Model):
    start_time = models.TimeField(blank=True)  
    end_time = models.TimeField(blank=True)    
    subject = models.CharField(max_length=255, blank=True)  
    teacher = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.subject} ({self.start_time} - {self.end_time})"

class Deadline(models.Model):
    description = models.CharField(max_length=255)
    date_time = models.DateTimeField()

    def __str__(self):
        return f"{self.description} - {self.date_time}"
    
    
    
    
    
    
    