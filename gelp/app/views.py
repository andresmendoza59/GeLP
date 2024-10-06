from rest_framework import viewsets
from .serializer import ApplianceSerializer
from .models import Appliance


# Create your views here.
class ApplianceViewSet(viewsets.ModelViewSet):
    queryset = Appliance.objects.all()
    serializer_class = ApplianceSerializer
