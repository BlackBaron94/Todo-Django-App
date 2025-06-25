from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from .models import Task


# Testing models
class TaskModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password"
        )
        self.task = Task.objects.create(
            user=self.user, task_text="Test Task", pub_date="2023-01-01T00:00Z"
        )

    def test_str_method(self):
        self.assertEqual(str(self.task), "Test Task")

    def test_is_task_completed_returns_false_by_default(self):
        self.assertFalse(self.task.is_task_completed())


# Testing post methods of views
class TaskViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password"
        )
        self.client.login(username="testuser", password="password")
        self.now = timezone.now()

    def test_add_task_view_creates_task(self):
        self.client.post(reverse("add_task"), {"task_text": "New task"})
        self.assertEqual(Task.objects.count(), 1)

    def test_toggle_completed_updates_status(self):
        task = Task.objects.create(
            user=self.user, task_text="Task", pub_date=self.now
        )
        self.client.post(
            reverse("toggle_completed", args=[task.id]),
            {"completion_status": "on"},
        )
        task.refresh_from_db()
        self.assertTrue(task.is_task_completed())

    def test_edit_task_updates_text(self):
        task = Task.objects.create(
            user=self.user, task_text="Initial Text", pub_date=self.now
        )
        self.client.post(
            reverse("edit_completed", args=[task.id]),
            {"task_text": "Changed Test Task"},
        )
        task.refresh_from_db()
        self.assertEqual(task.task_text, "Changed Test Task")

    def test_edit_task_updates_status_completed(self):
        task = Task.objects.create(
            user=self.user, task_text="Run test", pub_date=self.now
        )
        self.client.post(
            reverse("edit_completed", args=[task.id]),
            {"task_text": "Run test", "completion_status": "on"},
        )
        task.refresh_from_db()
        self.assertEqual(task.task_text, "Run test")
        self.assertTrue(task.is_task_completed())

    def test_edit_task_updates_status_pending(self):
        task = Task.objects.create(
            user=self.user, task_text="Run test", pub_date=self.now
        )
        self.client.post(
            reverse("edit_completed", args=[task.id]),
            {"task_text": "Run test"},
        )
        task.refresh_from_db()
        self.assertEqual(task.task_text, "Run test")
        self.assertFalse(task.is_task_completed())

    def test_edit_task_updates_text_and_status_completed(self):
        task = Task.objects.create(
            user=self.user, task_text="Initial text", pub_date=self.now
        )
        self.assertFalse(task.is_task_completed())
        self.client.post(
            reverse("edit_completed", args=[task.id]),
            {"task_text": "New text", "completion_status": "on"},
        )
        task.refresh_from_db()
        self.assertEqual(task.task_text, "New text")
        self.assertTrue(task.is_task_completed())

    def test_new_task_with_200_characters(self):
        string = ""
        for i in range(0, 20):
            for letter in range(0, 10):
                string = string + str(letter)
        string = string[1:]
        string = string + "0"
        # Ensures correct string length
        self.assertEqual(len(string), 200)
        self.client.post(reverse("add_task"), {"task_text": string})
        self.assertEqual(Task.objects.count(), 1)

    def test_new_task_with_201_characters(self):
        string = ""
        for i in range(0, 20):
            for letter in range(0, 10):
                string = string + str(letter)
        string = string[1:]
        string = string + "01"
        # Ensures correct string length
        self.assertEqual(len(string), 201)
        self.client.post(reverse("add_task"), {"task_text": string})
        self.assertEqual(Task.objects.count(), 0)
    
    def test_add_task_fails_with_empty_text(self):
        self.client.post(reverse("add_task"), {"task_text": ""})
        self.assertEqual(Task.objects.count(), 0)

    def test_edit_task_with_200_characters(self):
        task = Task.objects.create(
            user=self.user, task_text="Initial short text", pub_date=self.now
        )
        string = ""
        for i in range(0, 20):
            for letter in range(0, 10):
                string = string + str(letter)
        string = string[1:]
        string = string + "0"
        # Ensures correct string length
        self.assertEqual(len(string), 200)
        self.client.post(
            reverse("edit_completed", args=[task.id]), {"task_text": string}
        )
        task.refresh_from_db()
        self.assertEqual(task.task_text, string)

    def test_edit_task_with_201_characters(self):
        task = Task.objects.create(
            user=self.user, task_text="Initial short text", pub_date=self.now
        )
        string = ""
        for i in range(0, 20):
            for letter in range(0, 10):
                string = string + str(letter)
        string = string[1:]
        string = string + "01"
        # Ensures correct string length
        self.assertEqual(len(string), 201)
        self.client.post(
            reverse("edit_completed", args=[task.id]), {"task_text": string}
        )
        task.refresh_from_db()
        self.assertEqual(task.task_text, "Initial short text")

    def test_delete_task(self):
        task = Task.objects.create(
            user=self.user, task_text="Delete task", pub_date=self.now
        )
        self.assertEqual(Task.objects.count(), 1)
        self.client.post(reverse("delete_task_confirmed", args=[task.id]))
        self.assertEqual(Task.objects.count(), 0)


class TestViewRedirectTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password"
        )
        self.now = timezone.now()

    # Login required tests
    def test_index_view_requires_login(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_edit_view_requires_login(self):
        task = Task.objects.create(
            user=self.user, task_text="Task to edit", pub_date=self.now
        )
        response = self.client.get(reverse("edit", args=[task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_delete_view_requires_login(self):
        task = Task.objects.create(
            user=self.user, task_text="Task to delete", pub_date=self.now
        )
        response = self.client.get(reverse("delete_task", args=[task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_create_view_requires_login(self):
        response = self.client.get(reverse("create"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_detail_view_requires_login(self):
        task = Task.objects.create(
            user=self.user, task_text="Task to delete", pub_date=self.now
        )
        response = self.client.get(reverse("detail", args=[task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    # Redirects of signup and login to index for logged in users
    def test_login_redirects_to_index(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("index"), response.url)

    def test_signup_redirects_to_index(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("index"), response.url)

    # Redirects after task completion tests
    def test_create_view_redirects_to_index(self):
        self.client.login(username="testuser", password="password")
        response = self.client.post(
            reverse("add_task"), {"task_text": "New task text"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("index"), response.url)

    def test_edit_task_redirects_to_index(self):
        self.client.login(username="testuser", password="password")
        task = Task.objects.create(
            user=self.user, task_text="Task to edit", pub_date=self.now
        )
        response = self.client.post(
            reverse("edit_completed", args=[task.id]),
            {"task_text": "Task text edited", "completion_status": "on"},
        )
        task.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(task.task_text, "Task text edited")
        self.assertTrue(task.is_task_completed())
        self.assertIn(reverse("index"), response.url)

    def test_delete_task_redirects_to_index(self):
        self.client.login(username="testuser", password="password")
        task = Task.objects.create(
            user=self.user, task_text="Task to delete", pub_date=self.now
        )
        self.assertEqual(Task.objects.count(), 1)
        response = self.client.post(
            reverse("delete_task_confirmed", args=[task.id])
        )
        self.assertEqual(Task.objects.count(), 0)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("index"), response.url)

    def test_detail_on_different_users_task(self):
        user2 = User.objects.create_user(
            username="testuser2", password="password2"
        )
        self.client.login(username="testuser", password="password")
        task = Task.objects.create(
            user=user2, task_text="User's 2 task", pub_date=self.now
        )
        self.assertEqual(Task.objects.count(), 1)
        self.assertTrue(task.user == user2)
        self.assertFalse(task.user == self.user)
        response = self.client.get(reverse("detail", args=[task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("index"), response.url)

    def test_edit_on_different_users_task(self):
        user2 = User.objects.create_user(
            username="testuser2", password="password2"
        )
        self.client.login(username="testuser", password="password")
        task = Task.objects.create(
            user=user2, task_text="User's 2 task", pub_date=self.now
        )
        self.assertEqual(Task.objects.count(), 1)
        self.assertTrue(task.user == user2)
        self.assertFalse(task.user == self.user)
        response = self.client.get(reverse("edit", args=[task.id]))
        self.assertEqual(response.status_code,302)
        self.assertIn(reverse("index"), response.url)
        
    def test_delete_on_different_users_task(self):
        user2 = User.objects.create_user(
            username="testuser2", password="password2"
        )
        self.client.login(username="testuser", password="password")
        task = Task.objects.create(
            user=user2, task_text="User's 2 task", pub_date=self.now
        )
        self.assertEqual(Task.objects.count(), 1)
        self.assertTrue(task.user == user2)
        self.assertFalse(task.user == self.user)
        response = self.client.get(reverse("delete_task", args=[task.id]))
        self.assertEqual(response.status_code,302)
        self.assertIn(reverse("index"), response.url)