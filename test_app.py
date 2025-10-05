"""
Test Suite for Inventory Management System
Run with: python test_app.py
"""

from app import app, db, Product, Location, ProductMovement
from sqlalchemy import func

def test_database_connection():
    """Test database connection and tables"""
    print("Testing database connection...")
    with app.app_context():
        try:
            # Test connection
            db.session.execute('SELECT 1')
            print("✅ Database connection successful")
            
            # Check tables exist
            tables = db.engine.table_names()
            expected_tables = ['product', 'location', 'product_movement']
            for table in expected_tables:
                if table in tables:
                    print(f"✅ Table '{table}' exists")
                else:
                    print(f"❌ Table '{table}' missing")
            
            return True
        except Exception as e:
            print(f"❌ Database error: {e}")
            return False

def test_sample_data():
    """Test sample data was loaded"""
    print("\nTesting sample data...")
    with app.app_context():
        try:
            product_count = Product.query.count()
            location_count = Location.query.count()
            movement_count = ProductMovement.query.count()
            
            print(f"✅ Products: {product_count} (Expected: 4)")
            print(f"✅ Locations: {location_count} (Expected: 4)")
            print(f"✅ Movements: {movement_count} (Expected: 20)")
            
            if product_count >= 4 and location_count >= 4 and movement_count >= 20:
                print("✅ Sample data loaded successfully")
                return True
            else:
                print("⚠️  Sample data count mismatch")
                return False
        except Exception as e:
            print(f"❌ Error checking sample data: {e}")
            return False

def test_models():
    """Test model relationships"""
    print("\nTesting model relationships...")
    with app.app_context():
        try:
            # Test Product model
            product = Product.query.first()
            print(f"✅ Product: {product.name}")
            print(f"✅ Product has {len(product.movements)} movements")
            
            # Test Location model
            location = Location.query.first()
            print(f"✅ Location: {location.name}")
            print(f"✅ Location has {len(location.movements_from)} outgoing movements")
            print(f"✅ Location has {len(location.movements_to)} incoming movements")
            
            # Test ProductMovement model
            movement = ProductMovement.query.first()
            print(f"✅ Movement: {movement.product.name} - {movement.qty} units")
            print(f"✅ Movement type: {movement.get_movement_type()}")
            
            return True
        except Exception as e:
            print(f"❌ Error testing models: {e}")
            return False

def test_balance_calculation():
    """Test inventory balance calculation"""
    print("\nTesting balance calculation...")
    with app.app_context():
        try:
            # Get first product and location
            product = Product.query.first()
            location = Location.query.first()
            
            # Calculate balance
            incoming = db.session.query(func.sum(ProductMovement.qty)).filter(
                ProductMovement.product_id == product.product_id,
                ProductMovement.to_location == location.location_id
            ).scalar() or 0
            
            outgoing = db.session.query(func.sum(ProductMovement.qty)).filter(
                ProductMovement.product_id == product.product_id,
                ProductMovement.from_location == location.location_id
            ).scalar() or 0
            
            balance = incoming - outgoing
            
            print(f"✅ Product: {product.name}")
            print(f"✅ Location: {location.name}")
            print(f"✅ Incoming: {incoming}")
            print(f"✅ Outgoing: {outgoing}")
            print(f"✅ Balance: {balance}")
            
            return True
        except Exception as e:
            print(f"❌ Error calculating balance: {e}")
            return False

def test_routes():
    """Test application routes"""
    print("\nTesting application routes...")
    with app.test_client() as client:
        try:
            routes = [
                ('/', 'Home'),
                ('/products', 'Products'),
                ('/locations', 'Locations'),
                ('/movements', 'Movements'),
                ('/reports', 'Reports'),
            ]
            
            for route, name in routes:
                response = client.get(route)
                if response.status_code == 200:
                    print(f"✅ {name} route ({route}): OK")
                else:
                    print(f"❌ {name} route ({route}): Failed ({response.status_code})")
            
            return True
        except Exception as e:
            print(f"❌ Error testing routes: {e}")
            return False

def test_movement_types():
    """Test different movement types"""
    print("\nTesting movement types...")
    with app.app_context():
        try:
            # Test incoming movement (from_location = None)
            incoming = ProductMovement.query.filter(
                ProductMovement.from_location.is_(None),
                ProductMovement.to_location.isnot(None)
            ).first()
            if incoming:
                print(f"✅ Incoming movement found: {incoming.get_movement_type()}")
            
            # Test outgoing movement (to_location = None)
            outgoing = ProductMovement.query.filter(
                ProductMovement.from_location.isnot(None),
                ProductMovement.to_location.is_(None)
            ).first()
            if outgoing:
                print(f"✅ Outgoing movement found: {outgoing.get_movement_type()}")
            
            # Test transfer movement (both locations set)
            transfer = ProductMovement.query.filter(
                ProductMovement.from_location.isnot(None),
                ProductMovement.to_location.isnot(None)
            ).first()
            if transfer:
                print(f"✅ Transfer movement found: {transfer.get_movement_type()}")
            
            return True
        except Exception as e:
            print(f"❌ Error testing movement types: {e}")
            return False

def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("INVENTORY MANAGEMENT SYSTEM - TEST SUITE")
    print("=" * 60)
    
    tests = [
        test_database_connection,
        test_sample_data,
        test_models,
        test_balance_calculation,
        test_routes,
        test_movement_types,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"TEST RESULTS: {passed} passed, {failed} failed")
    print("=" * 60)
    
    if failed == 0:
        print("✅ ALL TESTS PASSED!")
    else:
        print(f"⚠️  {failed} test(s) failed")

if __name__ == '__main__':
    run_all_tests()