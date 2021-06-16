from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from simple_history.models import HistoricalRecords

# Create your models here.

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)
    date = models.DateField()
    time_in = models.TimeField()
    time_out = models.TimeField()
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    comment = models.TextField()
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.first_name} {self.last_name} | {self.time_in}-{self.time_out} | {self.date} | BY {self.user}'
    
    def get_absolute_url(self):
        return reverse('booking-list')

class ChangeLog(models.Model):
    log = models.TextField()
    date_logged = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.log}'