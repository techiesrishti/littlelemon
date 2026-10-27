from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'tables', views.BookingViewSet, basename='tables')
router.register(r'bookings', views.BookingViewSet, basename='bookings')

urlpatterns = [
    # Static and dynamic HTML template views
    path('', views.home, name='home'),
    path('index/', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('menu/', views.menu, name='menu'),
    path('book/', views.book, name='book'),
    path('reservations/', views.reservations, name='reservations'),

    # DRF Menu API endpoints
    path('menu-items/', views.MenuItemsView.as_view(), name='menu-items'),
    path('menu-items/<int:pk>/', views.SingleMenuItemView.as_view(), name='single-menu-item'),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
    path('menu/items/', views.MenuItemsView.as_view(), name='menu-items-alt'),
    path('menu/items/<int:pk>/', views.SingleMenuItemView.as_view()),

    # Direct User Registration API endpoint (/api/registration/)
    path('registration/', views.UserRegistrationView.as_view(), name='user-registration'),
    path('registration', views.UserRegistrationView.as_view()),

    # DRF Table Booking API router endpoints (/booking/tables/, /tables/, /bookings/)
    path('booking/', include(router.urls)),
    path('', include(router.urls)),

    # Legacy JavaScript endpoint for book.js (exact match without trailing slash)
    path('bookings', views.bookings, name='bookings'),
]
