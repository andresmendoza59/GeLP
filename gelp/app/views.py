import random
import io
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from .models import Appliance, Diagnostic, ApplianceOperator
from django.template import loader
from django.views import generic
from reportlab.pdfgen import canvas
from django.contrib.auth.models import User, Group


class ListView(generic.ListView):
    template_name = 'app/appliance_list.html'
    context_object_name = 'appliance_list'

    def get_queryset(self):
        appliances = Appliance.objects.all()

        for appliance in appliances:
            appliance.has_operator = ApplianceOperator.objects.filter(appliance_model=appliance).exists()

        return appliances

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Create a dictionary using the actual model string as the key
        has_diagnostic = {
            appliance.id: Diagnostic.objects.filter(appliance_model__model=appliance.model).exists()
            for appliance in context[self.context_object_name]
        }
        context['has_diagnostic'] = has_diagnostic

        # Check if each appliance has an operator assigned
        has_operator = {
            appliance.id: ApplianceOperator.objects.filter(appliance_model=appliance).exists()
            for appliance in context[self.context_object_name]
        }
        context['has_operator'] = has_operator

        return context


def operators_view(request):
    if request.method == 'POST':
        # Retrieve the "Operators" group
        operators_group = Group.objects.get(name='Operators')

        # Filter users belonging to the "Operators" group
        operators = User.objects.filter(groups=operators_group)

        # Pass the list of operators to the template context
        context = {
            'operators': operators,
            'appliance_id': request.POST.get('appliance_id')
        }

        # Render the template with the context data
        return render(request, 'app/assign_operator.html', context)
    return HttpResponse("Invalid method", status=405)


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


def aux_generate(name: str, value: str, upper_lim: float, lower_lim: float) -> str:
    if value < lower_lim:
        return f"Under average {name}"
    elif value > upper_lim:
        return f"Over average {name}"
    return "Working correctly"


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
        p.setFont("Times-Bold", 12)
        p.drawString(200, 750, f"{appliance.brand}: {appliance.model}")
        p.setFont("Times-Italic", 12)
        p.drawString(250, 730, "Type: fridge")
        p.setFont("Times-Roman", 12)
        p.drawString(20, 690, f"Amperage: {amperage:.2f} Amps; Ideal range: 3-6 Amps; {aux_generate("amperage", 
                                                                                                    amperage, 6, 3)}")
        p.drawString(20, 670, f"Voltage: {voltage:.2f} Volts; Ideal range: 115-125 Volts; {aux_generate("voltage", voltage, 
                                                                                              125, 115)}")
        p.drawString(20, 650, f"Electric Power: {electric_power:.2f} Watts; Ideal range: 300-800 Watts; "
                              f"{aux_generate("wattage", electric_power, 800, 300)}")
        p.drawString(20, 630, f"Temperature: {average_temperature:.2f} Celsius; Ideal range: 3-6 Celsius; "
                              f"{aux_generate("temperature", average_temperature, 5, 3)}")
        p.drawString(20, 610, f"Freezer Temperature: {average_temperature_freezer:.2f} Celsius; Ideal range: 0-4 Celsius; "
                              f"{aux_generate("freezer temperature", average_temperature_freezer, 4, 0)}")

        p.showPage()
        p.save()

        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='diagnostic.pdf')


def save_operator_appliance(request):
    if request.method == 'POST':
        appliance_id = request.POST.get('appliance_id')
        operator_id = request.POST.get('operator_id')
        limit_date = request.POST.get('limit_date')
        observations = request.POST.get('observations')
        appliance = Appliance.objects.get(id=appliance_id)
        operators_group = Group.objects.get(name='Operators')
        operators_users = User.objects.filter(groups=operators_group)
        operator = operators_users.get(id=operator_id)

        assignation = ApplianceOperator(appliance_model=appliance, operator=operator, limit_date=limit_date,
                                        observations=observations)
        assignation.save()

        return HttpResponseRedirect("../appliance_list")
    return HttpResponse("Invalid method", status=405)


def change_state(request):
    if request.method == 'POST':
        appliance_id = request.POST.get('appliance_id')
        new_state = request.POST.get('new_state')
        appliance = Appliance.objects.get(id=appliance_id)
        appliance.state = new_state
        appliance.save()
        return HttpResponseRedirect('appliance_list')
    return HttpResponse("Invalid method", status=405)
