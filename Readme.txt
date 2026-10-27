12
/api/bookings/
/api/registration/

=======================================================
Little Lemon Restaurant - Peer Review API Testing Guide
=======================================================

BASE URL:
http://127.0.0.1:8000/

-------------------------------------------------------
1. User Registration & Authentication Endpoints
-------------------------------------------------------
A) User Registration (Peer Test Path):
   - Method: POST
   - Path: /api/registration/
   - (Alternative Djoser path: /auth/users/)
   - Body (JSON):
     {
       "username": "peer_reviewer",
       "password": "peerpassword123",
       "email": "reviewer@littlelemon.com"
     }

B) Generate / Obtain Authentication Token:
   - Method: POST
   - Path: /auth/token/login/
   - (Alternative DRF path: /api-token-auth/)
   - Body (JSON):
     {
       "username": "peer_reviewer",
       "password": "peerpassword123"
     }
   - Response will return an auth token, e.g.:
     { "auth_token": "YOUR_TOKEN_HERE" }

-------------------------------------------------------
2. Menu API Endpoints
-------------------------------------------------------
A) List all Menu Items:
   - Method: GET
   - Path: /api/menu-items/
   - (Alternative path: /restaurant/menu-items/)
   - Header: Not required (publicly accessible)

B) Create a Menu Item:
   - Method: POST
   - Path: /api/menu-items/
   - Header: Authorization: Token <YOUR_TOKEN_HERE>
   - Body (JSON):
     {
       "title": "Lemon Tart",
       "price": "5.50",
       "inventory": 25
     }

C) Single Menu Item (Read / Update / Delete):
   - Method: GET / PUT / PATCH / DELETE
   - Path: /api/menu-items/1/
   - Header for PUT / DELETE: Authorization: Token <YOUR_TOKEN_HERE>

-------------------------------------------------------
3. Table Booking API Endpoints
-------------------------------------------------------
(Requires Authentication Token)

A) List all Table Bookings (Peer Test Path):
   - Method: GET
   - Path: /api/bookings/
   - (Alternative path: /restaurant/booking/tables/)
   - Header: Authorization: Token <YOUR_TOKEN_HERE>

B) Create a Table Reservation:
   - Method: POST
   - Path: /api/bookings/
   - (Alternative path: /restaurant/booking/tables/)
   - Header: Authorization: Token <YOUR_TOKEN_HERE>
   - Body (JSON):
     {
       "name": "Alex Johnson",
       "no_of_guests": 4,
       "booking_date": "2026-11-15"
     }

C) Single Booking Detail / Update / Cancel:
   - Method: GET / PUT / DELETE
   - Path: /api/bookings/1/
   - Header: Authorization: Token <YOUR_TOKEN_HERE>

-------------------------------------------------------
4. Static HTML Web Pages Served by Django
-------------------------------------------------------
- Home Page:          http://127.0.0.1:8000/
- About Us Page:      http://127.0.0.1:8000/about/
- Menu Web Page:      http://127.0.0.1:8000/menu/
- Table Booking Form: http://127.0.0.1:8000/book/
- Reservations List:  http://127.0.0.1:8000/reservations/

-------------------------------------------------------
5. How to Run Unit Tests
-------------------------------------------------------
Run the following command in terminal:
  python manage.py test
All 13 unit tests for models, views, authentication, and static templates will execute.
