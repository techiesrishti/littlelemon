import datetime
from django.db import models


class Booking(models.Model):
    name = models.CharField(max_length=255, default='')
    no_of_guests = models.IntegerField(default=1)
    booking_date = models.DateField(default=datetime.date.today)
    
    # Fields for compatibility with static HTML booking templates
    first_name = models.CharField(max_length=200, blank=True, default='')
    reservation_date = models.DateField(null=True, blank=True)
    reservation_slot = models.SmallIntegerField(default=10, null=True, blank=True)

    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'

    def save(self, *args, **kwargs):
        if self.name and not self.first_name:
            self.first_name = self.name
        elif self.first_name and not self.name:
            self.name = self.first_name

        if self.booking_date and not self.reservation_date:
            self.reservation_date = self.booking_date
        elif self.reservation_date and not self.booking_date:
            self.booking_date = self.reservation_date

        super().save(*args, **kwargs)

    def __str__(self):
        display_name = self.name or self.first_name or 'Reservation'
        display_date = self.booking_date or self.reservation_date
        return f'{display_name} : {display_date}'


class Menu(models.Model):
    title = models.CharField(max_length=255, default='')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.IntegerField(default=5)

    # Fields for compatibility with static HTML menu templates
    name = models.CharField(max_length=200, blank=True, default='')
    menu_item_description = models.TextField(max_length=1000, blank=True, default='')

    class Meta:
        verbose_name = 'Menu'
        verbose_name_plural = 'Menu Items'

    def save(self, *args, **kwargs):
        if self.title and not self.name:
            self.name = self.title
        elif self.name and not self.title:
            self.title = self.name
        super().save(*args, **kwargs)

    def __str__(self):
        item_title = self.title or self.name
        return f'{item_title} : {str(self.price)}'


# Alias for curriculum compatibility where MenuItem is referenced
MenuItem = Menu
