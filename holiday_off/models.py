from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()

class Holiday(models.Model):
    staff = models.ManyToManyField(User, related_name='holidays')
    name = models.CharField(max_length=255)
    date = models.DateField()
    total_days = models.IntegerField(default=0)  # Add this field
    remaining_days = models.IntegerField(default=0)  # Add this field
    

    def __str__(self):
        return self.name


class OffDuty(models.Model):
    staff = models.ForeignKey(User, on_delete=models.CASCADE)
    holiday = models.ForeignKey(Holiday, on_delete=models.CASCADE)
    date = models.DateField()
   
    

    def __str__(self):
        return f"{self.staff.username} - {self.date}"
