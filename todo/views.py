from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import Task

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    """
    View for the main page of the ToDo App when logged in. Shows all tasks.
    """
    tasks = Task.objects.filter(user=request.user)
    return render(
        request, "todo/index.html", {"tasks": tasks, "user": request.user}
    )


@require_POST
@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def toggle_completed(request, task_id):
    """
    Function runs when checkbox status of index page is altered. Saves change
    to DB and displays a message to notify user of successful change.
    """
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    # Checkbox name "completed" will not be in request.POST when unchecked
    # When checked, will be as {"completed": "on"}
    task.completed = "completion_status" in request.POST
    task.save()
    if task.completed == True:
        completion_status="completed"
    else:
        completion_status="pending"
    string = "✅ Task completion status successfully updated as {0}.".format(completion_status)
    messages.success(request, string)
    return redirect("index")

# Detail view accessible only by the task owner
# Not linked from UI – meant as optional/internal fallback
@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def detail(request, task_id):
    """
    Detail view of a task showing all available data stored for the specific
    task. 
    
    Page exists for future expansions of app capabilities, giving the
    user the capability to inspect sum of task details, e.g. in the event of
    a "deadline date" field addition.
    """
    task = get_user_task_or_redirect(task_id, request.user)
    if task:
        return render(request, "todo/detail.html", {"task": task})
    else:
        return redirect("index")


def signup(request):
    """
    View for the signup. If user is logged in, they get redirected to index.
    If user successfuly signs up, they are automatically logged in and 
    redirected to index.
    """
    if request.user.is_authenticated:
        return redirect("index")
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def create(request):
    """
    View for creating a new task.
    """
    return render(request, "todo/create.html")


@require_POST
@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_task(request):
    """
    Function that handles the POST request from create.html form "Add" button.
    
    Creates a message in index which informs user in case of text field being
    empty, text field containing more than 200 chars or successful addition of
    task.
    """
    task_text = request.POST.get("task_text", "").strip()
    if task_text:
        if len(task_text) > 200:
            messages.error(request, """❌ Task description too long. 
Please, keep your task description under 200 characters.""")
            return redirect("index")
        Task.objects.create(
            user=request.user, task_text=task_text, pub_date=timezone.now()
        )
        messages.success(request, "✅ Task successfully added.")
    else:
        messages.error(
            request, "❌ Task description field was empty."
        )
    return redirect("index")


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit(request, task_id):
    """
    View for editing a specific task's task_text and/or completion status.
    """
    task = get_user_task_or_redirect(task_id, request.user)
    if task:
        return render(request, "todo/edit.html", {"task": task})
    else:
        return redirect("index")

@require_POST
@login_required
def edit_completed(request, task_id):
    """
    Function handling the POST request from edit.html "Confirm Changes" button.
    Checks for empty field, for field longer than 200 chars and notifies user
    accordingly with a message displayed at index page.
    """
    task = get_user_task_or_redirect(task_id, request.user)
    if task:
        new_task_text=request.POST.get("task_text", "").strip()
        if new_task_text:
            if len(new_task_text) > 200:
                messages.error(request, """❌ Task description too long. 
Please, keep your task description under 200 characters.""")
                return redirect("index")
            task.task_text=new_task_text
            # Checkbox is not in request.POST when unchecked
            task.completed = 'completion_status' in request.POST
            task.save()
            messages.success(request, "✅ Task edited successfully.")
        else:
            messages.error(request, "❌ Task field was empty. Edit a new description to task.")
    return redirect("index")


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_task(request, task_id):
    """
    View for deleting a task.
    """
    task = get_user_task_or_redirect(task_id, request.user)
    if task:
        return render(request, "todo/delete_task.html", {"task": task})
    else:
        return redirect("index")


@require_POST
@login_required
def delete_task_confirmed(request, task_id):
    """
    Function that handles the POST request from delete_task.html's "Yes" button
    that confirms deletion.
    Notifies the user with a mesasge at index page, where he is redirected.
    """
    task = get_user_task_or_redirect(task_id, request.user)
    if task:
        task.delete()
        messages.success(request, "✅ Task deleted successfully.")
    return redirect("index")


@login_required
def delete_task_aborted(request, task_id):
    """
    Function that handles the GET request from delete_task.html's "No" button
    that aborts the deletion. 
    User is notified with a message at index page, where he is redirected.
    """
    task = get_user_task_or_redirect(task_id, request.user)
    if task:
        string = """❌ Task "{0}" deletion aborted.""".format(task.task_text)
        messages.error(request, string)
    return redirect("index")


def get_user_task_or_redirect(task_id, user):
    """
    Helper function that checks if user is trying to access a task's URL
    without the task being the users. If task doesn't exist, gets a 404,
    if task is not created by user returns None, or finally returns task.


    Args:
        task_id (int): Task's primary key id value.
        user (User object): Logged in user's data.

    Returns:
        Task Object or None: If checks are okay, returns task.
    """
    task = get_object_or_404(Task, pk=task_id)
    if task.user != user:
        return None
    else:
        return task
