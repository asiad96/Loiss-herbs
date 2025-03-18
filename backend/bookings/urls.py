from django.urls import path
from . import views

app_name = "bookings"

urlpatterns = [
    path("services/", views.ServiceListView.as_view(), name="service_list"),
    path("book/", views.BookingCreateView.as_view(), name="booking_create"),
    path("confirmation/", views.booking_confirmation, name="booking_confirmation"),
    path("dashboard/", views.ClientDashboard.as_view(), name="client_dashboard"),
]
