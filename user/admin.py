from django.contrib import admin
from .models import Student, Contact, Lesson, Event, Teacher
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group

# Student Admin
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'strand', 'status')
    list_filter = ('status', 'strand', 'learning_mode')
    search_fields = ('first_name', 'last_name', 'email', 'strand')
    readonly_fields = ('generate_temp_password',)  # Optional for secure fields
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'middle_name', 'last_name', 'address', 'phone', 'email', 'mother_tongue', 'religion', 'sex')
        }),
        ('Academic Details', {
            'fields': ('learning_mode', 'strand', 'tvl_track', 'status', 'payment_method')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_relationship', 'emergency_contact_phone', 'emergency_contact_email')
        }),
    )

    def save_model(self, request, obj, form, change):
        # Ensure the Student is assigned to the Student group
        super().save_model(request, obj, form, change)
        student_group, created = Group.objects.get_or_create(name='Student')
        obj.user.groups.add(student_group)
        obj.user.save()  # Ensure the user is saved after assigning the group

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'subject', 'email', 'teacher_strand', 'created_at', 'updated_at')
    search_fields = ('first_name', 'last_name', 'email', 'subject')
    list_filter = ('teacher_strand', 'subject')
    fields = ('first_name', 'last_name', 'email', 'subject', 'teacher_strand', 'tvl_options', 'password')

    def save_model(self, request, obj, form, change):
        # Check if the related `user` exists
        try:
            _ = obj.user  # Try accessing the user field
        except User.DoesNotExist:
            # Create a new user if it doesn't exist
            user = User.objects.create_user(
                username=obj.email,
                email=obj.email,
                password=obj.password if obj.password else None,
                first_name=obj.first_name,
                last_name=obj.last_name
            )
            obj.user = user

        # If user exists, optionally update its attributes
        else:
            if obj.password:
                obj.user.set_password(obj.password)
                obj.user.save()

        # Save the Teacher object
        super().save_model(request, obj, form, change)
        teacher_group, created = Group.objects.get_or_create(name='Teacher')
        obj.user.groups.add(teacher_group)
        obj.user.save()  # Ensure the user is saved after assigning the group

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'title', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'title')
    readonly_fields = ('created_at',)

class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'attachment')
    search_fields = ('title',)

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    list_filter = ('date',)
    ordering = ('-date',)
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

from django.contrib import admin
from .models import Resources, Announcement, Schedule, Deadline

# Resource Admin
class ResourcesAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'link', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at', 'updated_at')

# Announcement Admin
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'link', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at', 'updated_at')

# Schedule Admin
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('subject', 'start_time', 'end_time', 'teacher', 'created_at', 'updated_at')
    search_fields = ('subject', 'teacher')
    list_filter = ('created_at', 'updated_at')

# Deadline Admin
class DeadlineAdmin(admin.ModelAdmin):
    list_display = ('description', 'date_time')
    search_fields = ('description',)
    list_filter = ('date_time',)


# Register your models here
admin.site.register(Resources, ResourcesAdmin)
admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Deadline, DeadlineAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Teacher, TeacherAdmin)
