# Movie Ticket Booking System

This project is a **Movie Ticket Booking System** built using **Django Rest Framework (DRF)** and **Django Channels**. It allows users to browse events (movies), select tickets, and complete payments via PayPal. WebSockets are used for real-time ticket selection updates.

## Features
- **Event Listing & Details**: Users can view available movies with category filters.
- **Real-time Ticket Selection**: Users can select and unselect tickets using WebSockets.
- **Payment Integration**: PayPal is used for secure payments.
- **Refund System**: Users can request refunds for purchased tickets.
- **Authentication**: Users must be authenticated to book tickets.

## Technologies Used
- **Django Rest Framework (DRF)**: RESTful API development
- **Django Channels**: WebSockets for real-time ticket selection
- **PostgreSQL**: Database management
- **Celery & Redis**: Background task processing
- **PayPal SDK**: Online payment processing

---

## Key Features Implementation

### Real-time Ticket Selection

- Using `Django Channels` for WebSocket communication
- Limit users for selecting more than 4 tickets
- Preventing ticket selection conflicts using `database transactions`

### Payment Processing

- Integrating PayPal REST SDK
- Supports payment creation, execution, and refunds
- Requires authentication
- Saves payment details after successful transactions

### Security

- `JWT authentication` for WebSocket connections
- Permission classes for payment endpoints
- Database-level ticket selection locking
- User authentication required for ticket purchases


## API Endpoints

### Event API
- `GET /api/events/` - List all movies
- `GET /api/events/{id}/` - Retrieve a movie's details
- `GET /api/events/{id}/tickets/` - List available tickets for a movie

### Ticket Booking
- WebSocket: `ws://yourdomain.com/ws/events/{movie_id}/?date=YYYY-MM-DD&theater=XYZ`
- Allows real-time ticket selection and removal

### Payment API
- `POST /api/payment/create/` - Create PayPal payment
- `GET /api/payment/execute/` - Execute payment after approval
- `GET /api/payment/cancel/` - Handle payment cancellations
- `POST /api/payment/refund/` - Refund a completed transaction

---
## WebSocket Ticket Selection Flow
1. Users connect via WebSocket to the specific room for a movie, date, and theater.
2. Users send messages with `ticket_id` to select or unselect a ticket.
3. The system checks if the ticket is available and assigns it to the user.
4. The updated ticket status is broadcast to all connected users.

---
## Background Tasks
This system uses Celery for processing background tasks, such as:
- **Saving Ticket Purchases**
- **Handling Refunds**

---

## Installation Guide

### 1. Clone the Repository
```bash
    git clone https://github.com/gioms101/events.git
    cd events/
```

### 2. Create a Virtual Environment
```bash
    python -m venv venv
    source venv/bin/activate  # For MacOS/Linux
    venv\Scripts\activate  # For Windows
```

### 3. Install Dependencies
```bash
    pip install -r requirements.txt
```

### 4. Set Up the Database
Modify the `settings.py` file to configure your database settings, then run:
```bash
    python manage.py migrate
```

### 5. Create a Superuser (Optional, for Admin Access)
```bash
    python manage.py createsuperuser
```

### 6. Run the Development Server
```bash
    python manage.py runserver
```

### 7. Run Redis and Celery Workers
```bash
    redis-server  # Start Redis (Ensure Redis is installed)
    celery -A your_project_name worker --loglevel=info
```

### 8. Configure PayPal API Credentials
Update `settings.py` with your **PayPal Client ID** and **Secret**:
```python
    PAYPAL_MODE = 'sandbox'  # or 'live'
    PAYPAL_CLIENT_ID = 'your-client-id'
    PAYPAL_SECRET = 'your-client-secret'
```

---
