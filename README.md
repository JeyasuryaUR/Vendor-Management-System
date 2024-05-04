# Vendor Performance Metrics API

This project is a Django application that provides an API for tracking vendor performance metrics. It uses Django REST Framework for the API and Django's ORM for database interactions.

## Models

The application has three main models:

- `Vendor`: Represents a vendor with fields for name, contact details, address, vendor code, and various performance metrics.

- `PurchaseOrder`: Represents a purchase order with fields for PO number, vendor, order date, delivery date, items, quantity, status, quality rating, issue date, and acknowledgment date. It also includes methods to update the vendor's performance metrics when a purchase order is saved.

- `HistoricalPerformance`: Represents a vendor's historical performance metrics with fields for vendor, date, on-time delivery rate, average quality rating, average response time, and fulfillment rate.

## API

The application provides a RESTful API with endpoints for creating, retrieving, updating, and deleting vendors, purchase orders, and historical performance records. It uses Django REST Framework's viewsets and routers for easy URL configuration and concise, DRY views.

## Setup

To set up the application, follow these steps:

1. Clone the repository: `git clone https://github.com/JeyasuryaUR/Vendor-Management-System.git`
2. Install the requirements: `pip install -r requirements.txt`
3. Run the migrations: `python manage.py migrate`
4. Start the server: `python manage.py runserver`

Now you can access the API at `http://localhost:8000/api`.

## Usage

Here are some examples of how to use the API:

- To create a vendor, send a POST request to `/vendors/` with the vendor data in the request body.
- To retrieve all vendors, send a GET request to `/vendors/`.
- To update a vendor, send a PUT or PATCH request to `/vendors/<vendor_id>/` with the updated data in the request body.
- To delete a vendor, send a DELETE request to `/vendors/<vendor_id>/`.

You can use the same pattern to create, retrieve, update, and delete purchase orders and historical performance records.
