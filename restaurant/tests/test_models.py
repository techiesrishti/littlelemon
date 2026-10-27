import datetime
from django.test import TestCase
from restaurant.models import Menu, MenuItem, Booking


class MenuItemTest(TestCase):
    """
    Test suite for the Menu / MenuItem model as required by the Meta Capstone.
    """
    def test_get_item(self):
        item = MenuItem.objects.create(title="IceCream", price=80, inventory=100)
        self.assertEqual(str(item), "IceCream : 80")

    def test_menu_fields(self):
        item = Menu.objects.create(title="Pasta", price=14.50, inventory=15)
        self.assertEqual(item.title, "Pasta")
        self.assertEqual(float(item.price), 14.50)
        self.assertEqual(item.inventory, 15)
        # Check backward compatibility fields
        self.assertEqual(item.name, "Pasta")


class BookingTest(TestCase):
    """
    Test suite for the Booking model.
    """
    def test_create_booking(self):
        booking_date = datetime.date.today()
        booking = Booking.objects.create(
            name="Alice Smith",
            no_of_guests=4,
            booking_date=booking_date
        )
        self.assertEqual(booking.name, "Alice Smith")
        self.assertEqual(booking.no_of_guests, 4)
        self.assertEqual(booking.booking_date, booking_date)
        self.assertIn("Alice Smith", str(booking))
