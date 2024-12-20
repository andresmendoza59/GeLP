import django
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


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


class Diagnostic(models.Model):
    appliance_model = models.ForeignKey(Appliance, on_delete=models.CASCADE, related_name="diagnostics",
                                        default=6)
    amperage = models.FloatField(default=0.0)
    voltage = models.FloatField(default=0.0)
    electric_power = models.FloatField(default=0.0)
    average_temperature = models.FloatField(default=0.0)
    average_temperature_freezer = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.appliance_model} - {self.electric_power} - {self.average_temperature} - {self.average_temperature_freezer}"


class ApplianceOperator(models.Model):
    appliance_model = models.ForeignKey(Appliance, on_delete=models.CASCADE, related_name="appliance")
    operator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="operator")
    limit_date = models.DateTimeField(default=None, null=True)
    observations = models.TextField(default=None, null=True)

    def __str__(self):
        return f"{self.appliance_model} - {self.operator.username}"
