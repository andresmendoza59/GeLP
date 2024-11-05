from django.contrib import admin
from .models import Appliance, Diagnostic


# Register your models here.
admin.site.register(Appliance)
admin.site.register(Diagnostic)
