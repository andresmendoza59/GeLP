from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("appliance_list", views.ListView.as_view(), name="appliance_list"),
    path("appliance_add", views.appliance_add, name="appliance_add"),
    path('appliance/save/', views.save_appliance, name='save_appliance'),
    path('appliance/delete/', views.appliance_delete, name='appliance_delete'),
    path("appliance/diagnostic/start/", views.start_diagnostic, name='start_diagnostic'),
    path("appliance/diagnostic/generate/", views.generate_diagnostic, name='generate_diagnostic'),
    path("assign_operator/", views.operators_view, name="assign_operator"),
    path("assign_operator/save", views.save_operator_appliance, name='save_operator_appliance'),
    path("change_state", views.change_state, name='change_state'),
]
