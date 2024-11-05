import random
import io
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from .models import Appliance, Diagnostic
from django.template import loader
from django.views import generic
from reportlab.pdfgen import canvas


class ListView(generic.ListView):
    template_name = 'app/appliance_list.html'
    context_object_name = 'appliance_list'

    def get_queryset(self):
        return Appliance.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Create a dictionary using the actual model string as the key
        has_diagnostic = {
            appliance.id: Diagnostic.objects.filter(appliance_model__model=appliance.model).exists()
            for appliance in context[self.context_object_name]
        }
        context['has_diagnostic'] = has_diagnostic
        return context


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
        return HttpResponseRedirect('../../appliance_list')
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


def appliance_delete(request):
    if request.method == "POST":
        appliance = get_object_or_404(Appliance, pk=request.POST.get("appliance_id"))
        appliance.delete()
        return HttpResponseRedirect('../../appliance_list')
    return HttpResponse("Invalid method", status=405)


def start_diagnostic(request):
    if request.method == "POST":
        appliance = get_object_or_404(Appliance, pk=request.POST.get("appliance_id"))
        model = appliance.model
        appliances = Appliance.objects.filter(model=model)
        amperages, voltages, electric_powers, avg_temperatures, avg_freezer_temperatures = [], [], [], [], []
        for appliance in appliances:
            amperages.append(random.randint(1, 9))
            voltages.append(random.randint(90, 250))
            electric_powers.append(random.randint(200, 1000))
            avg_temperatures.append(random.randint(-1, 6))
            avg_freezer_temperatures.append(random.randint(-23, 0))
        amperage = sum(amperages) / len(amperages)
        voltage = sum(voltages) / len(voltages)
        electric_power = sum(electric_powers) / len(electric_powers)
        avg_temp = sum(avg_temperatures) / len(avg_temperatures)
        avg_freezer_temp = sum(avg_freezer_temperatures) / len(avg_freezer_temperatures)

        diagnostic = Diagnostic(appliance_model=appliance, amperage=amperage, voltage=voltage,
                                electric_power=electric_power, average_temperature=avg_temp,
                                average_temperature_freezer=avg_freezer_temp)
        diagnostic.save()
        return HttpResponseRedirect('../../../appliance_list')
    return HttpResponse("Invalid method", status=405)


def generate_diagnostic(request):
    if request.method == "POST":
        appliance = Appliance.objects.get(pk=request.POST['appliance_id'])
        diagnostic = appliance.diagnostics.all()[0]
        amperage = diagnostic.amperage
        voltage = diagnostic.voltage
        electric_power = diagnostic.electric_power
        average_temperature = diagnostic.average_temperature
        average_temperature_freezer = diagnostic.average_temperature_freezer
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        p.drawString(100, 20, f"Amperage: {amperage:.2f}")
        p.drawString(100, 40, f"Voltage: {voltage:.2f}")
        p.drawString(100, 60, f"Electric Power: {electric_power:.2f}")
        p.drawString(100, 80, f"Temperature: {average_temperature:.2f}")
        p.drawString(100, 100, f"Freezer Temperature {average_temperature_freezer:.2f}")

        p.showPage()
        p.save()

        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='diagnostic.pdf')
