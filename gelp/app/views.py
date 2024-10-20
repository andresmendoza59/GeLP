from django.shortcuts import render
from django.http import HttpResponse
from .models import Appliance


# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the app index.")


def appliance_list():
    appliances = Appliance.objects.all()
    return HttpResponse(appliances)
    # return render(request, 'appliance_list.html', {'appliances': appliances})


def appliance_add(code: str, name: str):
    appliance = Appliance(code=code, name=name)
    appliance.save()
    return HttpResponse(appliance)


def appliance_details(request, appliance_id: Appliance.pk):
    appliance = Appliance.objects.get(pk=appliance_id)
    # return render(request, 'appliance_details')
    return HttpResponse(appliance)


def appliance_edit(request, appliance_id: Appliance.pk, new_appliance_code: str, new_appliance_name: str,
                   new_appliance_state: Appliance.Status):

    appliance = Appliance.objects.get(pk=appliance_id)
    appliance.name = new_appliance_name
    appliance.code = new_appliance_code
    if appliance.state in Appliance.Status:
        appliance.state = new_appliance_state
    appliance.save()
    # return render(request, 'appliance_edit.html', {'appliance': appliance})
    return HttpResponse(appliance)


def appliance_delete(request, appliance_id: Appliance.pk):
    appliance = Appliance.objects.get(pk=appliance_id)
    appliance.delete()
    return HttpResponse(f"Appliance deleted: {appliance_id}")
