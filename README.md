Inventory Manager REST API

A comprehensive REST API for managing product inventory with full CRUD operations, built with Flask and SQLAlchemy.

Overview
This API provides programmatic access to inventory management functionality, following RESTful principles with proper error handling, validation, and testing coverage.

Quick Start
Base URL
http://localhost:5000/api
Content Type
All requests and responses use application/json

API Reference
Products

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/products` | Get all products |
| `GET` | `/products/{id}` | Get product by ID |
| `POST` | `/products` | Create new product |
| `PUT` | `/products/{id}` | Update existing product |
| `DELETE` | `/products/{id}` | Delete product |


Request/Response Format
Product Object

json{
  "id": 1,
  "name": "Product Name",
  "quantity": 100,
  "location": "Warehouse"
}
Success Response
json{
  "success": true,
  "data": { ... },
  "message": "Operation completed successfully"
}
Error Response
json{
  "success": false,
  "error": "Error description",
  "code": 400
}
Usage Examples with Postman
Get All Products

Method: GET
URL: http://localhost:5000/api/products
Headers: None required
Body: None required

Get Single Product

Method: GET
URL: http://localhost:5000/api/products/1
Headers: None required
Body: None required

Create Product

Method: POST
URL: http://localhost:5000/api/products
Headers:

Content-Type: application/json


Body (raw JSON):
json{
  "name": "New Product",
  "quantity": 50,
  "location": "Warehouse A"
}

Update Product

Method: PUT
URL: http://localhost:5000/api/products/1
Headers:

Content-Type: application/json


Body (raw JSON):
json{
  "name": "Updated Product",
  "quantity": 75
}
Partial Update (name only):
json{
  "name": "New Name Only"
}


Delete Product

Method: DELETE
URL: http://localhost:5000/api/products/1
Headers: None required
Body: None required

Postman Setup Guide
Creating a Collection

Open Postman and click "Collections" in the sidebar
Click the "+" button to create a new collection
Name it "Inventory API"

Adding Requests

Click "Add request" in your collection
Set the appropriate HTTP method (GET, POST, PUT, DELETE)
Enter the URL from the examples above
For POST/PUT requests:

Go to the "Body" tab
Select "raw" and choose "JSON" from dropdown
Paste the JSON payload


Click "Send" to execute the request

Viewing Results

Response data appears in the bottom panel
Check the Status Code (200, 201, 400, etc.)
View the Response Body for returned data
Check Response Time and Size in the response details

Validation Rules

Name: Required, must be unique across all products
Quantity: Required, minimum value of 5
Location: Optional, defaults to "Warehouse" if not specified

HTTP Status Codes
CodeDescription200Success201Resource created400Bad request (validation error)404Resource not found409Conflict (duplicate name)500Internal server error
Error Handling
The API provides detailed error messages for common scenarios:

Validation Errors: Missing required fields, invalid data types
Business Logic Errors: Duplicate names, quantity below minimum
Not Found: Attempting to access non-existent products
Server Errors: Database connection issues, unexpected errors

Testing
Run the comprehensive test suite:
bashpython -m pytest flaskinventory/test_api.py -v
The test suite includes:

All CRUD operations
Validation scenarios
Error conditions
Edge cases
100% code coverage

Technical Details
Architecture

Framework: Flask with Blueprint organization
Database: SQLAlchemy ORM
Serialization: Native JSON handling
Testing: pytest framework

Security Notes

Currently no authentication required
Suitable for local development
Production: Implement proper authentication and authorization

Database Schema
sqlCREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    quantity INTEGER NOT NULL CHECK(quantity >= 5),
    location VARCHAR(100) DEFAULT 'Warehouse'
);
Development
Prerequisites

Python 3.7+
Flask
SQLAlchemy
pytest (for testing)

Installation
bashpip install flask sqlalchemy pytest

Running the API
bashpython app.py
The API will be available at http://localhost:5000/api
