from django.db import models
from django.utils import timezone


# Create your models here.
class Appliance(models.Model):
    class Status(models.TextChoices):
        PENDING = "Pending"
        APPROVED = "Approved"
        REJECTED = "Rejected"

    brand = models.CharField(max_length=12, default='')
    model = models.CharField(max_length=12, default='')
    observations = models.TextField(default='')
    registration_date = models.DateTimeField(default=timezone.now)
    state = models.CharField(max_length=8, choices=Status, default=Status.PENDING)

    def __str__(self):
        return f"Model: {self.model}. Registered {self.registration_date}. State: {self.state}"


class Operator(models.Model):
    ...


class Diagnostic(models.Model):
    ...


class Report(models.Model):
    ...


class QualityManager(models.Model):
    ...
