from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),

    # Main restaurant app routes (HTML templates & API endpoints)
    path('', include('restaurant.urls')),
    path('restaurant/', include('restaurant.urls')),

    # Direct API prefix (supporting /api/bookings/, /api/registration/, /api/menu-items/, etc.)
    path('api/', include('restaurant.urls')),

    # Djoser Authentication & User endpoints (/auth/users/, /auth/token/login/, /auth/token/logout/)
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),

    # DRF Token Authentication endpoint
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]
