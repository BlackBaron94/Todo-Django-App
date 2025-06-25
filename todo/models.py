from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    last_update_date = models.DateTimeField(auto_now=True)
    completed = models.BooleanField("completion status", default=False)

    def is_task_completed(self):
        return self.completed

    def __str__(self):
        return self.task_text
