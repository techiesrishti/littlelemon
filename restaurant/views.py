import json
from datetime import date as date_cls

from django.contrib.auth.models import User
from django.core import serializers as core_serializers
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from rest_framework import generics, viewsets
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly

from .models import Booking, Menu
from .serializers import MenuItemSerializer, MenuSerializer, BookingSerializer, UserSerializer

FIRST_SLOT, LAST_SLOT = 10, 20  # 10 AM ... 8 PM


# ---------------------------------------------------------------------------
# HTML Template Views (Static & Dynamic Template Serving)
# ---------------------------------------------------------------------------

def index(request):
    """Serves the Little Lemon home page."""
    return render(request, 'index.html', {})


def home(request):
    """Alias for index view."""
    return render(request, 'index.html', {})


def about(request):
    """Serves the Little Lemon about page."""
    return render(request, 'about.html')


def menu(request):
    """Serves the Little Lemon menu page."""
    return render(request, 'menu.html', {'menu': Menu.objects.all()})


def book(request):
    """Serves the table booking HTML form page."""
    return render(request, 'book.html')


def reservations(request):
    """Displays reservations on an HTML template."""
    return render(request, 'bookings.html')


# ---------------------------------------------------------------------------
# Django REST Framework (DRF) API Views
# ---------------------------------------------------------------------------

class MenuItemView(ListCreateAPIView):
    """
    Handles GET (list) and POST (create) method calls for Menu items.
    """
    queryset = Menu.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# Alias for curriculum compatibility
MenuItemsView = MenuItemView


class SingleMenuItemView(RetrieveUpdateAPIView, DestroyAPIView):
    """
    Handles GET, PUT, PATCH and DELETE method calls for a single Menu item.
    """
    queryset = Menu.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookingViewSet(viewsets.ModelViewSet):
    """
    API ViewSet for table bookings.
    GET    /api/bookings/ or /restaurant/booking/tables/ -> List all bookings
    POST   /api/bookings/ or /restaurant/booking/tables/ -> Create a booking
    GET    /api/bookings/<id>/                           -> Booking details
    PUT    /api/bookings/<id>/                           -> Update booking
    DELETE /api/bookings/<id>/                           -> Delete booking
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]


class UserRegistrationView(generics.CreateAPIView):
    """
    POST /api/registration/ -> Direct endpoint for user registration
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


# ---------------------------------------------------------------------------
# Legacy Function-based View for HTML JavaScript Frontend Compatibility
# ---------------------------------------------------------------------------

@csrf_exempt
def bookings(request):
    """
    GET  /bookings               -> all bookings (JSON)
    GET  /bookings?date=YYYY-MM-DD -> bookings for that date (JSON)
    POST /bookings               -> create a booking (JSON body)
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            first_name = str(data.get('first_name', '')).strip()
            res_date = date_cls.fromisoformat(str(data.get('reservation_date')))
            slot = int(data.get('reservation_slot', 10))
        except (ValueError, KeyError, TypeError):
            return JsonResponse({'error': 'Invalid or missing data.'}, status=400)

        if not first_name:
            return JsonResponse({'error': 'First name is required.'}, status=400)
        if not FIRST_SLOT <= slot <= LAST_SLOT:
            return JsonResponse({'error': 'Invalid reservation slot.'}, status=400)

        # Duplicate booking check (same date AND same time)
        if Booking.objects.filter(reservation_date=res_date, reservation_slot=slot).exists():
            return JsonResponse(
                {'error': 'That time slot is already booked on this date.'}, status=409)
        try:
            Booking.objects.create(
                first_name=first_name,
                name=first_name,
                reservation_date=res_date,
                booking_date=res_date,
                reservation_slot=slot
            )
        except IntegrityError:
            return JsonResponse(
                {'error': 'That time slot is already booked on this date.'}, status=409)
        return JsonResponse({'success': True}, status=201)

    # GET
    qs = Booking.objects.all().order_by('reservation_date', 'reservation_slot')
    req_date = request.GET.get('date')
    if req_date:
        try:
            qs = qs.filter(reservation_date=date_cls.fromisoformat(req_date))
        except ValueError:
            return JsonResponse({'error': 'Date must be YYYY-MM-DD.'}, status=400)
    return HttpResponse(core_serializers.serialize('json', qs), content_type='application/json')
