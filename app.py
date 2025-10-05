from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Product, Location, ProductMovement
from sqlalchemy import func
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


# Home Route
@app.route('/')
def index():
    return render_template('index.html')


# ==================== PRODUCT ROUTES ====================
@app.route('/products')
def products():
    all_products = Product.query.all()
    return render_template('products.html', products=all_products)


@app.route('/products/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        
        if not name:
            flash('Product name is required!', 'danger')
            return render_template('product_form.html')
        
        new_product = Product(name=name, description=description)
        db.session.add(new_product)
        db.session.commit()
        
        flash(f'Product "{name}" added successfully!', 'success')
        return redirect(url_for('products'))
    
    return render_template('product_form.html')


@app.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        
        if not name:
            flash('Product name is required!', 'danger')
            return render_template('product_form.html', product=product)
        
        product.name = name
        product.description = description
        db.session.commit()
        
        flash(f'Product "{name}" updated successfully!', 'success')
        return redirect(url_for('products'))
    
    return render_template('product_form.html', product=product)


@app.route('/products/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    # Check if product has movements
    if product.movements:
        flash(f'Cannot delete product "{product.name}" because it has movement records!', 'danger')
        return redirect(url_for('products'))
    
    name = product.name
    db.session.delete(product)
    db.session.commit()
    
    flash(f'Product "{name}" deleted successfully!', 'success')
    return redirect(url_for('products'))


# ==================== LOCATION ROUTES ====================
@app.route('/locations')
def locations():
    all_locations = Location.query.all()
    return render_template('locations.html', locations=all_locations)


@app.route('/locations/add', methods=['GET', 'POST'])
def add_location():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        address = request.form.get('address', '').strip()
        
        if not name:
            flash('Location name is required!', 'danger')
            return render_template('location_form.html')
        
        new_location = Location(name=name, address=address)
        db.session.add(new_location)
        db.session.commit()
        
        flash(f'Location "{name}" added successfully!', 'success')
        return redirect(url_for('locations'))
    
    return render_template('location_form.html')


@app.route('/locations/edit/<int:location_id>', methods=['GET', 'POST'])
def edit_location(location_id):
    location = Location.query.get_or_404(location_id)
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        address = request.form.get('address', '').strip()
        
        if not name:
            flash('Location name is required!', 'danger')
            return render_template('location_form.html', location=location)
        
        location.name = name
        location.address = address
        db.session.commit()
        
        flash(f'Location "{name}" updated successfully!', 'success')
        return redirect(url_for('locations'))
    
    return render_template('location_form.html', location=location)


@app.route('/locations/delete/<int:location_id>', methods=['POST'])
def delete_location(location_id):
    location = Location.query.get_or_404(location_id)
    
    # Check if location has movements
    if location.movements_from or location.movements_to:
        flash(f'Cannot delete location "{location.name}" because it has movement records!', 'danger')
        return redirect(url_for('locations'))
    
    name = location.name
    db.session.delete(location)
    db.session.commit()
    
    flash(f'Location "{name}" deleted successfully!', 'success')
    return redirect(url_for('locations'))


# ==================== PRODUCT MOVEMENT ROUTES ====================
@app.route('/movements')
def movements():
    all_movements = ProductMovement.query.order_by(ProductMovement.timestamp.desc()).all()
    return render_template('movements.html', movements=all_movements)


@app.route('/movements/add', methods=['GET', 'POST'])
def add_movement():
    if request.method == 'POST':
        from_location = request.form.get('from_location')
        to_location = request.form.get('to_location')
        product_id = request.form.get('product_id')
        qty = request.form.get('qty')
        
        # Validation
        if not product_id:
            flash('Product is required!', 'danger')
            return redirect(url_for('add_movement'))
        
        if not qty or int(qty) <= 0:
            flash('Quantity must be greater than 0!', 'danger')
            return redirect(url_for('add_movement'))
        
        if not from_location and not to_location:
            flash('At least one location (From or To) must be selected!', 'danger')
            return redirect(url_for('add_movement'))
        
        if from_location == to_location and from_location:
            flash('From and To locations cannot be the same!', 'danger')
            return redirect(url_for('add_movement'))
        
        # Convert empty strings to None
        from_loc = int(from_location) if from_location else None
        to_loc = int(to_location) if to_location else None
        
        new_movement = ProductMovement(
            from_location=from_loc,
            to_location=to_loc,
            product_id=int(product_id),
            qty=int(qty)
        )
        
        db.session.add(new_movement)
        db.session.commit()
        
        flash('Product movement added successfully!', 'success')
        return redirect(url_for('movements'))
    
    products = Product.query.all()
    locations = Location.query.all()
    return render_template('movement_form.html', products=products, locations=locations)


@app.route('/movements/edit/<int:movement_id>', methods=['GET', 'POST'])
def edit_movement(movement_id):
    movement = ProductMovement.query.get_or_404(movement_id)
    
    if request.method == 'POST':
        from_location = request.form.get('from_location')
        to_location = request.form.get('to_location')
        product_id = request.form.get('product_id')
        qty = request.form.get('qty')
        
        # Validation
        if not product_id:
            flash('Product is required!', 'danger')
            return redirect(url_for('edit_movement', movement_id=movement_id))
        
        if not qty or int(qty) <= 0:
            flash('Quantity must be greater than 0!', 'danger')
            return redirect(url_for('edit_movement', movement_id=movement_id))
        
        if not from_location and not to_location:
            flash('At least one location (From or To) must be selected!', 'danger')
            return redirect(url_for('edit_movement', movement_id=movement_id))
        
        if from_location == to_location and from_location:
            flash('From and To locations cannot be the same!', 'danger')
            return redirect(url_for('edit_movement', movement_id=movement_id))
        
        # Convert empty strings to None
        from_loc = int(from_location) if from_location else None
        to_loc = int(to_location) if to_location else None
        
        movement.from_location = from_loc
        movement.to_location = to_loc
        movement.product_id = int(product_id)
        movement.qty = int(qty)
        
        db.session.commit()
        
        flash('Product movement updated successfully!', 'success')
        return redirect(url_for('movements'))
    
    products = Product.query.all()
    locations = Location.query.all()
    return render_template('movement_form.html', movement=movement, products=products, locations=locations)


@app.route('/movements/delete/<int:movement_id>', methods=['POST'])
def delete_movement(movement_id):
    movement = ProductMovement.query.get_or_404(movement_id)
    
    db.session.delete(movement)
    db.session.commit()
    
    flash('Product movement deleted successfully!', 'success')
    return redirect(url_for('movements'))


# ==================== REPORT ROUTE ====================
@app.route('/reports')
def reports():
    # Calculate balance for each product in each location
    # Balance = SUM(qty where to_location = location_id) - SUM(qty where from_location = location_id)
    
    locations = Location.query.all()
    products = Product.query.all()
    
    balance_data = []
    
    for product in products:
        for location in locations:
            # Calculate incoming quantity (to_location)
            incoming = db.session.query(func.sum(ProductMovement.qty)).filter(
                ProductMovement.product_id == product.product_id,
                ProductMovement.to_location == location.location_id
            ).scalar() or 0
            
            # Calculate outgoing quantity (from_location)
            outgoing = db.session.query(func.sum(ProductMovement.qty)).filter(
                ProductMovement.product_id == product.product_id,
                ProductMovement.from_location == location.location_id
            ).scalar() or 0
            
            balance = incoming - outgoing
            
            # Only show locations with non-zero balance
            if balance != 0:
                balance_data.append({
                    'product': product.name,
                    'location': location.name,
                    'quantity': balance
                })
    
    return render_template('reports.html', balance_data=balance_data)


# ==================== DATABASE INITIALIZATION ====================
def init_db():
    with app.app_context():
        db.create_all()
        
        # Check if data already exists
        if Product.query.first() is None:
            # Add sample products
            products = [
                Product(name='Laptop Dell XPS 15', description='High-performance laptop with 16GB RAM and 512GB SSD'),
                Product(name='Wireless Mouse Logitech', description='Ergonomic wireless mouse with USB receiver'),
                Product(name='USB-C Cable', description='2-meter USB-C charging and data cable'),
                Product(name='Monitor Samsung 27"', description='27-inch 4K UHD monitor with HDR support')
            ]
            
            for product in products:
                db.session.add(product)
            
            # Add sample locations
            locations = [
                Location(name='Main Warehouse', address='123 Industrial Blvd, New York, NY 10001'),
                Location(name='Retail Store Downtown', address='456 Main Street, New York, NY 10002'),
                Location(name='Distribution Center East', address='789 Logistics Ave, Newark, NJ 07102'),
                Location(name='Regional Hub West', address='321 Commerce Dr, Los Angeles, CA 90001')
            ]
            
            for location in locations:
                db.session.add(location)
            
            db.session.commit()
            
            # Add sample product movements
            movements = [
                # Initial stock arrivals (from_location = None means incoming)
                ProductMovement(from_location=None, to_location=1, product_id=1, qty=50),
                ProductMovement(from_location=None, to_location=1, product_id=2, qty=100),
                ProductMovement(from_location=None, to_location=1, product_id=3, qty=200),
                ProductMovement(from_location=None, to_location=1, product_id=4, qty=30),
                
                # Transfers between warehouses
                ProductMovement(from_location=1, to_location=2, product_id=1, qty=10),
                ProductMovement(from_location=1, to_location=3, product_id=1, qty=15),
                ProductMovement(from_location=1, to_location=4, product_id=1, qty=5),
                
                ProductMovement(from_location=1, to_location=2, product_id=2, qty=25),
                ProductMovement(from_location=1, to_location=3, product_id=2, qty=30),
                ProductMovement(from_location=1, to_location=4, product_id=2, qty=15),
                
                ProductMovement(from_location=1, to_location=2, product_id=3, qty=50),
                ProductMovement(from_location=1, to_location=3, product_id=3, qty=60),
                ProductMovement(from_location=1, to_location=4, product_id=3, qty=40),
                
                ProductMovement(from_location=1, to_location=2, product_id=4, qty=8),
                ProductMovement(from_location=1, to_location=3, product_id=4, qty=10),
                
                # Sales/outgoing (to_location = None means outgoing)
                ProductMovement(from_location=2, to_location=None, product_id=1, qty=3),
                ProductMovement(from_location=2, to_location=None, product_id=2, qty=10),
                ProductMovement(from_location=3, to_location=None, product_id=3, qty=20),
                ProductMovement(from_location=4, to_location=None, product_id=4, qty=2),
                
                # Additional restocking
                ProductMovement(from_location=None, to_location=2, product_id=2, qty=50),
            ]
            
            for movement in movements:
                db.session.add(movement)
            
            db.session.commit()
            
            print("Database initialized with sample data!")


if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=3000)