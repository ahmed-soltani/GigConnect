from django.urls import path
from . import views

urlpatterns = [
    path("", views.cs_dashboard, name="cs_dashboard"),
    path("reports/", views.cs_reports, name="cs_reports"),
]
