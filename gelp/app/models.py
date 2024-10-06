from django.db import models


# Create your models here.
class Appliance(models.Model):
    class Status(models.TextChoices):
        PENDING = "Pending"
        APPROVED = "Approved"
        REJECTED = "Rejected"

    code = models.CharField(max_length=12, default='')
    name = models.CharField(max_length=20, default='')
    state = models.CharField(max_length=8, choices=Status, default=Status.PENDING)

    def __str__(self):
        return f"Code: {self.code}.  Name: {self.name}. State: {self.state}"


class Operator(models.Model):
    ...


class Diagnostic(models.Model):
    ...


class Report(models.Model):
    ...


class QualityManager(models.Model):
    ...
