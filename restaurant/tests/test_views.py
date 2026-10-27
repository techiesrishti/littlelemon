import datetime
from django.test import TestCase, Client
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token

from restaurant.models import Menu, Booking
from restaurant.serializers import MenuItemSerializer


class StaticHTMLServingTest(TestCase):
    """
    Test suite verifying Django serves static HTML content.
    """
    def setUp(self):
        self.client = Client()

    def test_home_page_serves_html(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome to Little Lemon')

    def test_about_page_serves_html(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)

    def test_book_page_serves_html(self):
        response = self.client.get('/book/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Make a reservation')

    def test_menu_page_serves_html(self):
        Menu.objects.create(title="Falafel", price=8.50, inventory=10)
        response = self.client.get('/menu/')
        self.assertEqual(response.status_code, 200)


class MenuViewTest(TestCase):
    """
    Test suite for Menu views as required by the Meta Capstone.
    """
    def setUp(self):
        self.client = APIClient()
        self.item1 = Menu.objects.create(title="Greek Salad", price=12.50, inventory=10)
        self.item2 = Menu.objects.create(title="Bruschetta", price=7.99, inventory=20)
        self.item3 = Menu.objects.create(title="Lemon Dessert", price=6.50, inventory=15)

    def test_getall(self):
        """Tests that GET request to menu-items endpoint returns all serialized items."""
        response = self.client.get('/api/menu-items/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        items = Menu.objects.all()
        serializer = MenuItemSerializer(items, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_single_item(self):
        """Tests retrieving a single menu item by ID."""
        response = self.client.get(f'/api/menu-items/{self.item1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Greek Salad")


class BookingViewTest(TestCase):
    """
    Test suite for Table Booking API viewset.
    """
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123'
        )
        self.token = Token.objects.create(user=self.user)
        self.booking = Booking.objects.create(
            name='Test Guest',
            no_of_guests=2,
            booking_date=datetime.date.today()
        )

    def test_unauthenticated_booking_access_denied(self):
        """Ensure unauthenticated access to bookings is unauthorized."""
        response = self.client.get('/api/bookings/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_booking_access_granted(self):
        """Ensure authenticated access using Token authorization succeeds."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get('/api/bookings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_booking_via_api(self):
        """Ensure creating a table booking works for authenticated user."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        payload = {
            'name': 'New Reservation',
            'no_of_guests': 5,
            'booking_date': str(datetime.date.today())
        }
        response = self.client.post('/api/bookings/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.filter(name='New Reservation').count(), 1)


class UserRegistrationTest(TestCase):
    """
    Test user registration API.
    """
    def setUp(self):
        self.client = APIClient()

    def test_user_registration(self):
        payload = {
            'username': 'newuser',
            'password': 'strongpassword123',
            'email': 'newuser@littlelemon.com'
        }
        response = self.client.post('/api/registration/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())


class DjoserAuthenticationTest(TestCase):
    """
    Test suite for Djoser endpoints (/auth/users/, /auth/token/login/, /auth/token/logout/).
    """
    def setUp(self):
        self.client = APIClient()

    def test_djoser_user_registration(self):
        payload = {
            'username': 'djoser_user',
            'password': 'ComplexPassword123!',
            'email': 'djoser@littlelemon.com'
        }
        response = self.client.post('/auth/users/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='djoser_user').exists())

    def test_djoser_token_login_and_logout(self):
        # Create user
        User.objects.create_user(
            username='auth_user',
            password='ComplexPassword123!'
        )
        # Login
        login_payload = {
            'username': 'auth_user',
            'password': 'ComplexPassword123!'
        }
        login_resp = self.client.post('/auth/token/login/', login_payload, format='json')
        self.assertEqual(login_resp.status_code, status.HTTP_200_OK)
        self.assertIn('auth_token', login_resp.data)
        token = login_resp.data['auth_token']

        # Logout
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        logout_resp = self.client.post('/auth/token/logout/')
        self.assertEqual(logout_resp.status_code, status.HTTP_204_NO_CONTENT)
