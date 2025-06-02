from flask import Blueprint, jsonify, request
from flaskinventory import db
from flaskinventory.models import Product, Balance, Movement
from sqlalchemy.exc import IntegrityError

api = Blueprint('api', __name__)

def product_to_dict(product):
    balance = Balance.query.filter_by(product=product.prod_name).first()
    location = balance.location if balance else 'Warehouse'
    
    return {
        'id': product.prod_id,
        'name': product.prod_name,
        'quantity': product.prod_qty,
        'location': location
    }

@api.route('/products', methods=['GET'])
def get_products():
    try:
        products = Product.query.all()
        return jsonify({
            'success': True,
            'count': len(products),
            'products': [product_to_dict(product) for product in products]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'An error occurred while retrieving products'
        }), 500

@api.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({
            'success': False,
            'error': 'Not Found',
            'message': f'Product with ID {product_id} not found'
        }), 404
    
    return jsonify({
        'success': True,
        'product': product_to_dict(product)
    }), 200

@api.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    
    if not all(key in data for key in ['name', 'quantity']):
        return jsonify({
            'success': False,
            'error': 'Bad Request',
            'message': 'Missing required fields: name and quantity are required'
        }), 400
    
    try:
        quantity = int(data['quantity'])
        if quantity < 5:
            return jsonify({
                'success': False,
                'error': 'Bad Request',
                'message': 'Quantity must be at least 5'
            }), 400
    except ValueError:
        return jsonify({
            'success': False,
            'error': 'Bad Request',
            'message': 'Quantity must be a number'
        }), 400
    
    try:
        product = Product(prod_name=data['name'], prod_qty=quantity)
        db.session.add(product)
        db.session.commit()
        
        if 'location' in data and data['location'] != 'Warehouse':
            balance = Balance(
                product=data['name'],
                location=data['location'],
                quantity=quantity
            )
            db.session.add(balance)
            
            from datetime import datetime
            movement = Movement(
                ts=datetime.utcnow(),
                frm='Warehouse',
                to=data['location'],
                pname=data['name'],
                pqty=quantity
            )
            db.session.add(movement)
            db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Product {data["name"]} created successfully',
            'product': product_to_dict(product)
        }), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Conflict',
            'message': f'Product with name {data["name"]} already exists'
        }), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500

@api.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({
            'success': False,
            'error': 'Not Found',
            'message': f'Product with ID {product_id} not found'
        }), 404
    
    data = request.get_json()
    if not data:
        return jsonify({
            'success': False,
            'error': 'Bad Request',
            'message': 'No data provided for update'
        }), 400
    
    try:
        original_name = product.prod_name
        
        if 'name' in data:
            product.prod_name = data['name']
            Balance.query.filter_by(product=original_name).update(dict(product=data['name']))
            Movement.query.filter_by(pname=original_name).update(dict(pname=data['name']))
        
        if 'quantity' in data:
            try:
                quantity = int(data['quantity'])
                if quantity < 5:
                    return jsonify({
                        'success': False,
                        'error': 'Bad Request',
                        'message': 'Quantity must be at least 5'
                    }), 400
                product.prod_qty = quantity
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': 'Bad Request',
                    'message': 'Quantity must be a number'
                }), 400
        
        db.session.commit()
        return jsonify({
            'success': True,
            'message': f'Product updated successfully',
            'product': product_to_dict(product)
        }), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Conflict',
            'message': f'Product with name {data.get("name")} already exists'
        }), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500

@api.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({
            'success': False,
            'error': 'Not Found',
            'message': f'Product with ID {product_id} not found'
        }), 404
    
    try:
        product_name = product.prod_name
        
        Balance.query.filter_by(product=product_name).delete()
        
        db.session.delete(product)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Product {product_name} deleted successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500