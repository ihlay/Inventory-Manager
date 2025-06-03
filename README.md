Inventory Manager REST API

A comprehensive REST API for managing product inventory with full CRUD operations, built with Flask and SQLAlchemy.

Overview
This API provides programmatic access to inventory management functionality, following RESTful principles with proper error handling, validation, and testing coverage.

Quick Start

Base URL
```
http://localhost:5000/api
```

Content Type
All requests and responses use `application/json`

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
```json
{
  "id": 1,
  "name": "Product Name",
  "quantity": 100,
  "location": "Warehouse"
}
```

Success Response
```json
{
  "success": true,
  "data": { ... },
  "message": "Operation completed successfully"
}
```

Error Response
```json
{
  "success": false,
  "error": "Error description",
  "code": 400
}
```

Usage Examples with Postman

Get All Products
1. Method: `GET`
2. URL: `http://localhost:5000/api/products`
3. Headers: None required
4. Body: None required

Get Single Product
1. Method: `GET`
2. URL: `http://localhost:5000/api/products/1`
3. Headers: None required
4. Body: None required

Create Product
1. Method: `POST`
2. URL: `http://localhost:5000/api/products`
3. Headers: 
   - `Content-Type: application/json`
4. Body (raw JSON):
   ```json
   {
     "name": "New Product",
     "quantity": 50,
     "location": "Warehouse A"
   }
   ```

Update Product
1. Method: `PUT`
2. URL: `http://localhost:5000/api/products/1`
3. Headers: 
   - `Content-Type: application/json`
4. Body (raw JSON):
   ```json
   {
     "name": "Updated Product",
     "quantity": 75
   }
   ```
   
   Partial Update (name only):
   ```json
   {
     "name": "New Name Only"
   }
   ```

Delete Product
1. Method: `DELETE`
2. URL: `http://localhost:5000/api/products/1`
3. Headers: None required
4. Body: None required

Postman Setup Guide

Creating a Collection
1. Open Postman and click Collections in the sidebar
2. Click the "+" button to create a new collection
3. Name it "Inventory API"

Adding Requests
1. Click "Add request" in your collection
2. Set the appropriate HTTP method (GET, POST, PUT, DELETE)
3. Enter the URL from the examples above
4. For POST/PUT requests:
   - Go to the "Body" tab
   - Select "raw" and choose "JSON" from dropdown
   - Paste the JSON payloa
5. Click "Send" to execute the request

Viewing Results
- Response data appears in the bottom panel
- Check the Status Code (200, 201, 400, etc.)
- View the Response Body for returned data
- Check Response Time and Size in the response details

Validation Rules

- Name: Required, must be unique across all products
- Quantity: Required, minimum value of 5
- Location: Optional, defaults to "Warehouse" if not specified

HTTP Status Codes

| Code | Description |
|------|-------------|
| `200` | Success |
| `201` | Resource created |
| `400` | Bad request (validation error) |
| `404` | Resource not found |
| `409` | Conflict (duplicate name) |
| `500` | Internal server error |

Error Handling

The API provides detailed error messages for common scenarios:

- Validation Errors: Missing required fields, invalid data types
- Business Logic Errors: Duplicate names, quantity below minimum
- Not Found: Attempting to access non-existent products
- Server Errors: Database connection issues, unexpected errors

Testing

Run the comprehensive test suite:

python -m pytest flaskinventory/test_api.py -v

The test suite includes:
- All CRUD operations
- Validation scenarios
- Error conditions
- Edge cases
- 100% code coverage

Technical Details

Architecture
- Framework: Flask with Blueprint organization
- Database: SQLAlchemy ORM
- Serialization: Native JSON handling
- Testing: pytest framework

Security Notes
- Currently no authentication required
- Suitable for local development
- Production: Implement proper authentication and authorization

Database Schema
```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    quantity INTEGER NOT NULL CHECK(quantity >= 5),
    location VARCHAR(100) DEFAULT 'Warehouse'
);
```

Development
Prerequisites
- Python 3.7+
- Flask
- SQLAlchemy
- pytest (for testing)

Installation
```
pip install flask sqlalchemy pytest
```

Running the API
```bash
python app.py
```

The API will be available at `http://localhost:5000/api`
