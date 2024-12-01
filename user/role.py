from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

@login_required
def role_redirect(request):
    """
    Check the user's group (role) and redirect them to the appropriate page.
    """
    if request.user.groups.filter(name='Student').exists():
        return redirect('student')  # URL for the student page
    elif request.user.groups.filter(name='Teacher').exists():
        return redirect('teacher')  # URL for the teacher page
    elif request.user.groups.filter(name='Admin').exists():
        return redirect('admin')  # URL for the admin page
    else:
        messages.error(request, "You don't have an assigned role. Please contact an administrator.")
        return redirect('denied')  # Redirect to a default page if no role found
