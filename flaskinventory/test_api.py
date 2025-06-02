import pytest
import json
from flaskinventory import app, db
from flaskinventory.models import Product, Balance, Movement

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

@pytest.fixture
def init_database(client):
    with app.app_context():
        test_product = Product(prod_name='Test Product', prod_qty=100)
        db.session.add(test_product)
        db.session.commit()
        
        product_id = test_product.prod_id
        
        return product_id

def test_get_products(client, init_database):
    response = client.get('/api/products')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['success'] == True
    assert data['count'] == 1
    assert len(data['products']) == 1
    assert data['products'][0]['name'] == 'Test Product'
    assert data['products'][0]['quantity'] == 100
    assert data['products'][0]['location'] == 'Warehouse'

def test_get_product(client, init_database):
    product_id = init_database
    response = client.get(f'/api/products/{product_id}')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['success'] == True
    assert data['product']['name'] == 'Test Product'
    assert data['product']['quantity'] == 100

def test_get_nonexistent_product(client):
    response = client.get('/api/products/9999')
    data = json.loads(response.data)
    
    assert response.status_code == 404
    assert data['success'] == False
    assert 'not found' in data['message'].lower()

def test_create_product(client):
    response = client.post(
        '/api/products',
        data=json.dumps({
            'name': 'New Product',
            'quantity': 50
        }),
        content_type='application/json'
    )
    data = json.loads(response.data)
    
    assert response.status_code == 201
    assert data['success'] == True
    assert data['product']['name'] == 'New Product'
    assert data['product']['quantity'] == 50
    
    with app.app_context():
        product = Product.query.filter_by(prod_name='New Product').first()
        assert product is not None
        assert product.prod_qty == 50

def test_create_product_with_location(client):
    response = client.post(
        '/api/products',
        data=json.dumps({
            'name': 'Located Product',
            'quantity': 75,
            'location': 'Warehouse A'
        }),
        content_type='application/json'
    )
    data = json.loads(response.data)
    
    assert response.status_code == 201
    assert data['success'] == True
    assert data['product']['name'] == 'Located Product'
    assert data['product']['location'] == 'Warehouse A'
    
    with app.app_context():
        balance = Balance.query.filter_by(product='Located Product').first()
        assert balance is not None
        assert balance.location == 'Warehouse A'
        assert balance.quantity == 75

def test_create_product_invalid_data(client):
    response = client.post(
        '/api/products',
        data=json.dumps({
            'name': 'Invalid Product'
        }),
        content_type='application/json'
    )
    data = json.loads(response.data)
    
    assert response.status_code == 400
    assert data['success'] == False
    
    response = client.post(
        '/api/products',
        data=json.dumps({
            'name': 'Invalid Product',
            'quantity': 'not-a-number'
        }),
        content_type='application/json'
    )
    data = json.loads(response.data)
    
    assert response.status_code == 400
    assert data['success'] == False
    
    response = client.post(
        '/api/products',
        data=json.dumps({
            'name': 'Invalid Product',
            'quantity': 3  
        }),
        content_type='application/json'
    )
    data = json.loads(response.data)
    
    assert response.status_code == 400
    assert data['success'] == False

def test_create_duplicate_product(client, init_database):
    response = client.post(
        '/api/products',
        data=json.dumps({
            'name': 'Test Product',  
            'quantity': 50
        }),
        content_type='application/json'
    )
    data = json.loads(response.data)
    
    assert response.status_code == 409  
    assert data['success'] == False
    assert 'already exists' in data['message'].lower()

def test_update_product(client, init_database):
    product_id = init_database
    response = client.put(
        f'/api/products/{product_id}',
        data=json.dumps({
            'name': 'Updated Product',
            'quantity': 200
        }),
        content_type='application/json'
    )
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['success'] == True
    assert data['product']['name'] == 'Updated Product'
    assert data['product']['quantity'] == 200
    
    with app.app_context():
        product = Product.query.get(product_id)
        assert product.prod_name == 'Updated Product'
        assert product.prod_qty == 200

def test_update_product_name_only(client, init_database):
    product_id = init_database
    response = client.put(
        f'/api/products/{product_id}',
        data=json.dumps({
            'name': 'Renamed Product'
        }),
        content_type='application/json'
    )
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['success'] == True
    assert data['product']['name'] == 'Renamed Product'
    assert data['product']['quantity'] == 100  

def test_update_product_quantity_only(client, init_database):
    product_id = init_database
    response = client.put(
        f'/api/products/{product_id}',
        data=json.dumps({
            'quantity': 150
        }),
        content_type='application/json'
    )
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['success'] == True
    assert data['product']['name'] == 'Test Product'  
    assert data['product']['quantity'] == 150

def test_update_nonexistent_product(client):
    response = client.put(
        '/api/products/9999',
        data=json.dumps({
            'name': 'Ghost Product',
            'quantity': 50
        }),
        content_type='application/json'
    )
    data = json.loads(response.data)
    
    assert response.status_code == 404
    assert data['success'] == False

def test_update_product_invalid_data(client, init_database):
    product_id = init_database
    
    response = client.put(
        f'/api/products/{product_id}',
        data=json.dumps({
            'quantity': 'not-a-number'
        }),
        content_type='application/json'
    )
    data = json.loads(response.data)
    
    assert response.status_code == 400
    assert data['success'] == False
    
    response = client.put(
        f'/api/products/{product_id}',
        data=json.dumps({
            'quantity': 3  
        }),
        content_type='application/json'
    )
    data = json.loads(response.data)
    
    assert response.status_code == 400
    assert data['success'] == False

def test_delete_product(client, init_database):
    product_id = init_database
    response = client.delete(f'/api/products/{product_id}')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['success'] == True
    
    with app.app_context():
        product = Product.query.get(product_id)
        assert product is None

def test_delete_nonexistent_product(client):
    response = client.delete('/api/products/9999')
    data = json.loads(response.data)
    
    assert response.status_code == 404
    assert data['success'] == False