from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("/appliance_list", views.appliance_list, name="appliance_list"),
    path("/appliance_detail/<pk: appliance_id>", views.appliance_details, name="appliance_detail"),
    path("appliance_edit/<pk: appliance_id>", views.appliance_edit, name="appliance_edit"),
    path("appliance_delete/<pk:appliance_id>", views.appliance_delete, name="appliance_delete")
]