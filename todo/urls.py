from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from . import views
from django.http import HttpResponse

class CustomLoginView(LoginView):
    template_name = "registration/login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("index")  
        return super().dispatch(request, *args, **kwargs)



urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    path("signup/", views.signup, name="signup"),
    path("", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("create/add_task", views.add_task, name="add_task"),
    path("<int:task_id>/edit/", views.edit, name="edit"),
    path("<int:task_id>/edit_completed/", views.edit_completed, name="edit_completed"),
    path("<int:task_id>/delete_task/", views.delete_task, name="delete_task"),
    path("<int:task_id>/delete_task_confirmed/", views.delete_task_confirmed, name="delete_task_confirmed"),
    path("<int:task_id>/delete_task_aborted/", views.delete_task_aborted, name="delete_task_aborted"),
    # Optional route for task detail view
    # Used internally or manually, not linked from main UI
    path("<int:task_id>/", views.detail, name="detail"),
    path("<int:task_id>/toggle/", views.toggle_completed, name="toggle_completed"),

]