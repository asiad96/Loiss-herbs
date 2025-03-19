from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Service, Booking, Client
from django.contrib import messages
from django.contrib.auth import login
from .forms import ClientRegistrationForm
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.


class ServiceListView(ListView):
    """Display all available services"""

    model = Service
    template_name = "bookings/service_list.html"
    context_object_name = "services"

    def get_queryset(self):
        """Only show active services"""
        return Service.objects.filter(is_active=True)


class BookingCreateView(CreateView):
    """Handle new booking creation"""

    model = Booking
    template_name = "bookings/booking_form.html"
    fields = ["service", "date", "time", "notes"]
    success_url = reverse_lazy("booking_confirmation")

    def form_valid(self, form):
        """Add the current user's client profile to the booking"""
        # Get or create client profile for the current user
        client, created = Client.objects.get_or_create(
            user=self.request.user,
            defaults={
                "first_name": self.request.user.first_name,
                "last_name": self.request.user.last_name,
                "email": self.request.user.email,
            },
        )
        form.instance.client = client
        messages.success(self.request, "Booking created successfully!")
        return super().form_valid(form)


def booking_confirmation(request):
    """Display booking confirmation page"""
    return render(request, "bookings/booking_confirmation.html")


class ClientDashboard(LoginRequiredMixin, ListView):
    """Display client's bookings and allow management"""

    model = Booking
    template_name = "bookings/client_dashboard.html"
    context_object_name = "bookings"

    def get_queryset(self):
        """Only show current client's bookings"""
        return Booking.objects.filter(client__user=self.request.user).order_by(
            "date", "time"
        )


class ClientRegistrationView(CreateView):
    form_class = ClientRegistrationForm
    template_name = "bookings/registration.html"
    success_url = reverse_lazy("login")  # Redirect to login page after registration

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)  # Log the user in after registration
        return response


class ClientRegistrationAPI(APIView):
    """API endpoint for client registration"""

    def post(self, request):
        form = ClientRegistrationForm(data=request.data)
        if form.is_valid():
            user = form.save()
            return Response(
                {
                    "status": "success",
                    "message": "Registration successful",
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                    },
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"status": "error", "errors": form.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


# Views will be added here when we set up the React frontend
