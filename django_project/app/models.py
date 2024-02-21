from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Note(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField(blank=True)
    last_updated = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('note-update', kwargs={'pk': self.pk})
