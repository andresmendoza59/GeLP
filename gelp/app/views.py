from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Appliance
from django.template import loader
from django.views import generic


class ListView(generic.ListView):
    template_name = 'app/appliance_list.html'
    context_object_name = 'appliance_list'

    def get_queryset(self):
        return Appliance.objects.all()


class DetailView(generic.DetailView):
    model = Appliance
    template_name = 'app/appliance_detail.html'


# Create your views here.
def index(request):
    appliance_list = Appliance.objects.all()
    template = loader.get_template("app/index.html")
    context = {
        "appliance_list": appliance_list,
    }
    return HttpResponse(template.render(context, request))


def appliance_add(request):
    return render(request, 'app/appliance_add.html')


def save_appliance(request):
    if request.method == 'POST':
        brand = request.POST['brand']
        model = request.POST['model']
        observations = request.POST['observations']

        appliance = Appliance(brand=brand, model=model, observations=observations)
        appliance.save()
        return HttpResponseRedirect('index.html')
    return HttpResponse("Invalid method", status=405)


def appliance_details(request, appliance_id: Appliance.pk):
    appliance = get_object_or_404(Appliance, pk=appliance_id)
    return render(request, 'appliance_details', {"appliance": appliance})


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


# Not necessary though
def appliance_delete(request, appliance_id: Appliance.pk):
    appliance = Appliance.objects.get(pk=appliance_id)
    appliance.delete()
    return HttpResponse(f"Appliance deleted: {appliance_id}")
