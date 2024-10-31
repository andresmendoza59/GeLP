from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("appliance_list", views.ListView.as_view(), name="appliance_list"),
    path("appliance_add", views.appliance_add, name="appliance_add"),
    path("<int:pk>", views.DetailView.as_view(), name="appliance_details"),
    path("appliance_edit/<int:appliance_id>", views.appliance_edit, name="appliance_edit"),
    path("appliance_delete/<int:appliance_id>", views.appliance_delete, name="appliance_delete"),
    path('appliance/save/', views.save_appliance, name='save_appliance'),
]