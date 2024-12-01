from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from calendar import monthrange
from datetime import datetime
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import EnrollmentForm, ContactForm, EventForm, TeacherForm
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .models import Student, Lesson, Event, Teacher, Schedule, Deadline, Announcement, Resources, Contact
from .validators import validate_file  # Assuming you have a custom file validator
import random

EMOJIS = ["📌", "📢", "🎉", "🚨", "📝", "💬", "🔔", "📅", "🔊", "⭐"]


@login_required
def role_redirect(request):
    role_urls = {
        'Student': 'student',
        'Teacher': 'teacher_dashboard',
        'Admin': 'admin_dashboard',
    }
    for role, url in role_urls.items():
        if request.user.groups.filter(name=role).exists():
            return redirect(url)
    messages.error(request, "You don't have an assigned role. Please contact an administrator.")
    return redirect('denied')

def login(request):
    context = {
        'header_title': 'Login',
        'page_title': 'iiH College Portal - Login',
    }
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Strip leading and trailing spaces from email and password
        email = email.strip() if email else ''
        password = password.strip() if password else ''

        print(f"Email: {email}, Password: {password}")  # Debugging print

        # Authenticate user using email and password
        user = authenticate(request, username=email, password=password)  # 'username' used as email
        if user is not None:
            auth_login(request, user)
            return redirect('home')  # Redirect to a post-login page
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'login.html', context)

def enroll(request):
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = EnrollmentForm()

    context = {
        'header_title': 'Enrollment Form',
        'page_title': 'IIH College Portal - Enroll New Student',
        'form': form,
    }
    return render(request, 'enroll.html', context)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')  # Replace 'success' with your success page URL name
    else:
        form = ContactForm()

    context = {
        'form': form,
        'school': 'IIHC La Forteza Campus',
        'email': 'info@iihc.edu.ph',
        'number': '09678929232',
        'location': 'Caloocan City, Philippines',
        'header_title': 'Contact',


    }
    return render(request, 'message/contact.html', context)

@login_required
def teacher_dashboard(request):
    students = Student.objects.filter(status=Student.PENDING)
    lessons = Lesson.objects.all()
    events = Event.objects.all() 
    announcements = Announcement.objects.all()
    deadlines = Deadline.objects.all() 
    resources = Resources.objects.all() 
    schedules = Schedule.objects.all() 
    try:
        teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        return redirect('home')  

    # Add a random emoji to each announcement
    for announcement in announcements:
        announcement.emoji = random.choice(EMOJIS)

    if request.method == 'POST':
        try:
            # Approve a student
            if 'approve_student' in request.POST:
                student = get_object_or_404(Student, id=request.POST.get('approve_student'))
                student.status = Student.APPROVED
                student.save()
                messages.success(request, f"Student {student.first_name} approved.")
                
            # Delete a student
            elif 'delete_student' in request.POST:
                student = get_object_or_404(Student, id=request.POST.get('delete_student'))
                student.delete()
                messages.success(request, f"Student {student.first_name} deleted.")
                
            # Add a new lesson
            elif 'add_lesson' in request.POST:
                title = request.POST.get('title')
                description = request.POST.get('description')
                attachment = request.FILES.get('attachment')

                # Validate the uploaded file
                validate_file(attachment)

                # Create a new lesson
                Lesson.objects.create(
                    title=title,
                    description=description,
                    attachment=attachment,
                )
                messages.success(request, "Lesson added successfully.")
                
            # Delete a lesson
            elif 'delete_lesson' in request.POST:
                lesson = get_object_or_404(Lesson, id=request.POST.get('delete_lesson'))
                lesson.delete()
                messages.success(request, f"Lesson '{lesson.title}' deleted.")

            # Add a new event
            elif 'add_event' in request.POST:
                title = request.POST.get('event_title')
                description = request.POST.get('event_description')
                date = request.POST.get('event_date_time')
                link = request.POST.get('event_link')  
                image = request.FILES.get('event_image')  # Fetch image from request.FILES

                # Create a new event
                Event.objects.create(
                    title=title,
                    description=description,
                    date=date,
                    link=link,
                    image=image,
                )
                messages.success(request, "Event added successfully.")

            # Delete an event
            elif 'delete_event' in request.POST:
                event = get_object_or_404(Event, id=request.POST.get('delete_event'))
                event.delete()
                messages.success(request, f"Event '{event.title}' deleted.")

            # Add a new announcement
            elif 'add_announcement' in request.POST:
                title = request.POST.get('announcement_title')
                description = request.POST.get('announcement_description')
                link = request.POST.get('announcement_link')

                # Create a new announcement
                Announcement.objects.create(
                    title=title,
                    description=description,
                    link=link,
                )
                messages.success(request, "Announcement added successfully.")

            # Delete an announcement
            elif 'delete_announcement' in request.POST:
                announcement = get_object_or_404(Announcement, id=request.POST.get('delete_announcement'))
                announcement.delete()
                messages.success(request, f"Announcement '{announcement.title}' deleted.")

            # Add a new deadline
            elif 'add_deadline' in request.POST:
                description = request.POST.get('deadline_description')
                date_time = request.POST.get('deadline_date_time')

                # Create a new deadline
                Deadline.objects.create(
                    description=description,
                    date_time=date_time,
                )
                messages.success(request, "Deadline added successfully.")

            # Delete a deadline
            elif 'delete_deadline' in request.POST:
                deadline = get_object_or_404(Deadline, id=request.POST.get('delete_deadline'))
                deadline.delete()
                messages.success(request, f"Deadline '{deadline.description}' deleted.")

            # Add a new resource
            elif 'add_resource' in request.POST:
                title = request.POST.get('resource_title')
                description = request.POST.get('resource_description')
                link = request.POST.get('resource_link')

                # Create a new resource
                Resources.objects.create(
                    title=title,
                    description=description,
                    link=link,
                )
                messages.success(request, "Resource added successfully.")

            # Delete a resource
            elif 'delete_resource' in request.POST:
                resource = get_object_or_404(Resources, id=request.POST.get('delete_resource'))
                resource.delete()
                messages.success(request, f"Resource '{resource.title}' deleted.")

            # Add a new schedule
            elif 'add_schedule' in request.POST:
                start_time = request.POST.get('schedule_start_time')
                end_time = request.POST.get('schedule_end_time')
                subject = request.POST.get('schedule_subject')
                teacher = request.POST.get('schedule_teacher')

                # Create a new schedule
                Schedule.objects.create(
                    start_time=start_time,
                    end_time=end_time,
                    subject=subject,
                    teacher=teacher,
                )
                messages.success(request, "Schedule added successfully.")

            # Delete a schedule
            elif 'delete_schedule' in request.POST:
                schedule = get_object_or_404(Schedule, id=request.POST.get('delete_schedule'))
                schedule.delete()
                messages.success(request, f"Schedule '{schedule.subject}' deleted.")

            elif 'add_deadline' in request.POST:
                title = request.POST.get('deadline_description')
                date_time = request.POST.get('deadline_date_time')

                # Create a new schedule
                Schedule.objects.create(
                    description=description,
                    date_time=date_time,
                )
                messages.success(request, "Schedule added successfully.")

            # Delete a schedule
            elif 'delete_deadline' in request.POST:
                schedule = get_object_or_404(Schedule, id=request.POST.get('delete_schedule'))
                schedule.delete()
                messages.success(request, f"Deadline '{deadline.date_time}' deleted.")


        except Exception as e:
            messages.error(request, str(e))

        return redirect('teacher_dashboard')  # Redirect to the same dashboard after processing

    context = {
        'header_title': 'Teacher Dashboard',
        'page_title': 'IIH College Portal - Teacher',
        'students': students,
        'lessons': lessons,
        'events': events,
        'teacher': teacher,
        'announcements': announcements,
        'deadlines': deadlines,
        'resources': resources,
        'schedules': schedules,
    }
    return render(request, 'user/teacher/teacher_dashboard.html', context)

@login_required
def student_dashboard(request):
    lessons = Lesson.objects.all()
    events = Event.objects.all() 
    announcements = Announcement.objects.all()
    deadlines = Deadline.objects.all() 
    resources = Resources.objects.all() 
    schedules = Schedule.objects.all() 
    try:
        student = Student.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        return redirect('home')  

    for announcement in announcements:
        announcement.emoji = random.choice(EMOJIS)

    context = {
        'header_title': 'Student',
        'page_title': 'IIH College Portal - Student',
        'student': student,
        'lessons': lessons,
        'events': events,
        'announcements': announcements,
        'deadlines': deadlines,
        'resources': resources,
        'schedules': schedules,

    }
    return render(request, 'user/student/student_dashboard.html', context)

@login_required
def admin_dashboard(request):
    return render(request, 'user/superuser/admin_dashboard.html')

def contact(request):
    context = {
        'page_title': 'IIH College Portal - Contact',
        'header_title': 'Contact',
        'school': 'IIHC La Forteza Campus',
        'email': 'info@iihc.edu.ph',
        'number': '09678929232',
        'location': 'Caloocan City, Philippines',
    }
    form = ContactForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()  # Assuming the form handles saving
        messages.success(request, 'Your message has been sent successfully!')
        return redirect('success')
    context['form'] = form
    return render(request, 'message/contact.html', context)

def validate_file(attachment):
    valid_types = ['application/pdf', 'image/jpeg', 'image/png']
    if attachment.content_type not in valid_types:
        raise ValidationError("Unsupported file type.")
    if attachment.size > 5 * 1024 * 1024:  # Limit size to 5MB
        raise ValidationError("File size exceeds the limit of 5MB.")

def approve_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    if student.status == Student.PENDING:
        student.status = Student.APPROVED
        student.save()  # Save the status change
        
        # Ensure the student has a user
        if not student.user:
            student.create_user()  # Create a user if none exists
        
        # Send a temporary password email and assign the student to the 'Student' group
        student.send_temp_password_email()

        # Success message
        messages.success(request, f"Student {student.first_name} {student.last_name} has been approved.")
    else:
        messages.warning(request, f"Student {student.first_name} {student.last_name} cannot be approved as their status is '{student.status}'.")

    return redirect('home')

def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        student.delete()
        messages.success(request, f'Student {student.first_name} {student.last_name} has been deleted successfully.')
    return redirect('teacher')  # Adjust the redirect as necessary

def teacher_profile(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)

    context = {
        'page_title': 'IIH College Portal - Teacher Profile',
        'teacher': teacher,
    }
    return render(request, 'user/teacher/teacher_profile.html', context)

def student_profile(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    return render(request, 'student/student_profile.html', context)

def register_teacher(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists. Please choose a different one.')
                return render(request, 'user/superuser/register_teacher.html', {'form': form})

            # Create the user
            user = User.objects.create_user(
                username=username,
                password=form.cleaned_data['password'],  # Ensure you have a password field in the form
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )

            # Save the teacher-specific fields
            teacher = Teacher(
                user=user,
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                subject=form.cleaned_data['subject'],
                teacher_strand=form.cleaned_data['teacher_strand'],
                tvl_options=form.cleaned_data['tvl_options'],
            )

            try:
                teacher.save()  # Save the teacher instance
                messages.success(request, 'Teacher registration successful!')
                return redirect('home')  # Redirect to a login page or another view
            except Exception as e:
                messages.error(request, f'Error registering teacher: {e}')
                return render(request, 'user/superuser/register_teacher.html', {'form': form})
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TeacherForm()

    return render(request, 'user/superuser/register_teacher.html', {'form': form})

