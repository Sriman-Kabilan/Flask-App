# Inventory Management System

A complete Flask web application for managing products, locations, and product movements between warehouses. Built with Flask, SQLAlchemy ORM, SQLite database, and Bootstrap 5.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.0-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## Features

✅ **Complete CRUD Operations**
- Add, Edit, View, and Delete Products
- Add, Edit, View, and Delete Locations
- Add, Edit, View, and Delete Product Movements

✅ **Inventory Tracking**
- Track incoming stock (from_location = NULL)
- Track outgoing stock (to_location = NULL)
- Track transfers between locations
- Automatic timestamp recording

✅ **Reporting**
- Real-time inventory balance by product and location
- Visual indicators for stock levels
- Calculated quantities based on movements

✅ **User Interface**
- Clean, responsive Bootstrap 5 design
- Intuitive navigation
- Form validation with flash messages
- Mobile-friendly layout

## Database Structure

### Tables

#### 1. Product
| Column | Type | Description |
|--------|------|-------------|
| product_id | INTEGER | Primary Key (Auto-increment) |
| name | VARCHAR(100) | Product name (Required) |
| description | TEXT | Product description (Optional) |

#### 2. Location
| Column | Type | Description |
|--------|------|-------------|
| location_id | INTEGER | Primary Key (Auto-increment) |
| name | VARCHAR(100) | Location name (Required) |
| address | VARCHAR(200) | Location address (Optional) |

#### 3. ProductMovement
| Column | Type | Description |
|--------|------|-------------|
| movement_id | INTEGER | Primary Key (Auto-increment) |
| timestamp | DATETIME | Movement timestamp (Auto-set) |
| from_location | INTEGER | Source location FK (Nullable) |
| to_location | INTEGER | Destination location FK (Nullable) |
| product_id | INTEGER | Product FK (Required) |
| qty | INTEGER | Quantity moved (Required) |

### Movement Rules

- **Incoming Stock**: `from_location = NULL`, `to_location = Location ID`
  - Items are moved INTO a location
  
- **Outgoing Stock**: `from_location = Location ID`, `to_location = NULL`
  - Items are moved OUT of a location (sales, disposal, etc.)
  
- **Transfer**: `from_location = Location A`, `to_location = Location B`
  - Items are moved between two locations

- **Validation**: At least one location (from or to) must be specified

### Balance Calculation

For each product in each location:
```
Balance = SUM(qty where to_location = location_id) - SUM(qty where from_location = location_id)
```

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone or Download

```bash
# If using git
git clone <repository-url>
cd inventory_system

# Or download and extract the ZIP file
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the Application

```bash
python app.py
```

The application will:
1. Create the SQLite database (`inventory.db`)
2. Initialize tables
3. Load sample seed data
4. Start the development server on `http://localhost:5000`

### Step 5: Access the Application

Open your web browser and navigate to:
```
http://localhost:5000
```

## Sample Data

The application comes pre-loaded with sample data:

### Products (4 items)
- Laptop Dell XPS 15
- Wireless Mouse Logitech
- USB-C Cable
- Monitor Samsung 27"

### Locations (4 warehouses)
- Main Warehouse (New York)
- Retail Store Downtown (New York)
- Distribution Center East (Newark)
- Regional Hub West (Los Angeles)

### Movements (20 transactions)
- Initial stock arrivals
- Transfers between locations
- Sales/outgoing transactions
- Restocking operations

## Usage Guide

### Managing Products

1. **View Products**: Click "Products" in the navigation menu
2. **Add Product**: Click "Add New Product" button
   - Enter product name (required)
   - Add description (optional)
   - Click "Save Product"
3. **Edit Product**: Click "Edit" button next to any product
4. **Delete Product**: Click "Delete" button (only if no movements exist)

### Managing Locations

1. **View Locations**: Click "Locations" in the navigation menu
2. **Add Location**: Click "Add New Location" button
   - Enter location name (required)
   - Add address (optional)
   - Click "Save Location"
3. **Edit Location**: Click "Edit" button next to any location
4. **Delete Location**: Click "Delete" button (only if no movements exist)

### Managing Product Movements

1. **View Movements**: Click "Movements" in the navigation menu
2. **Add Movement**: Click "Add New Movement" button
   - Select product (required)
   - Select from location (optional - leave empty for incoming)
   - Select to location (optional - leave empty for outgoing)
   - Enter quantity (required, must be > 0)
   - Click "Save Movement"
3. **Edit Movement**: Click "Edit" button next to any movement
4. **Delete Movement**: Click "Delete" button

### Viewing Reports

1. Click "Reports" in the navigation menu
2. View inventory balance for each product in each location
3. Green badges indicate positive stock
4. Red badges indicate negative stock (potential data errors)
5. Only locations with non-zero balance are displayed

## Project Structure

```
inventory_system/
│
├── app.py                  # Main Flask application
├── models.py               # SQLAlchemy database models
├── requirements.txt        # Python dependencies
├── README.md              # This file
│
├── templates/             # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Home page
│   ├── products.html     # Products list
│   ├── product_form.html # Product add/edit form
│   ├── locations.html    # Locations list
│   ├── location_form.html # Location add/edit form
│   ├── movements.html    # Movements list
│   ├── movement_form.html # Movement add/edit form
│   └── reports.html      # Inventory balance report
│
├── static/               # Static files (CSS, JS, images)
│   ├── css/
│   └── js/
│
└── inventory.db          # SQLite database (created on first run)
```

## Technologies Used

- **Backend**: Flask 3.0.0
- **ORM**: Flask-SQLAlchemy 3.1.1
- **Database**: SQLite
- **Frontend**: Bootstrap 5.3.0
- **Icons**: Bootstrap Icons 1.11.0
- **Python**: 3.8+

## Configuration

### Database Configuration

By default, the application uses SQLite. To change the database:

Edit `app.py`:
```python
# For MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/inventory_db'

# For PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/inventory_db'
```

### Secret Key

For production, change the secret key in `app.py`:
```python
app.config['SECRET_KEY'] = 'your-secure-random-secret-key-here'
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Home page |
| GET | `/products` | List all products |
| GET/POST | `/products/add` | Add new product |
| GET/POST | `/products/edit/<id>` | Edit product |
| POST | `/products/delete/<id>` | Delete product |
| GET | `/locations` | List all locations |
| GET/POST | `/locations/add` | Add new location |
| GET/POST | `/locations/edit/<id>` | Edit location |
| POST | `/locations/delete/<id>` | Delete location |
| GET | `/movements` | List all movements |
| GET/POST | `/movements/add` | Add new movement |
| GET/POST | `/movements/edit/<id>` | Edit movement |
| POST | `/movements/delete/<id>` | Delete movement |
| GET | `/reports` | View inventory balance report |

## Troubleshooting

### Database Issues

If you encounter database errors:
```bash
# Delete the database file
rm inventory.db

# Restart the application
python app.py
```

### Port Already in Use

If port 5000 is already in use:
```python
# Edit app.py, change the port number
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Missing Dependencies

```bash
# Reinstall all dependencies
pip install -r requirements.txt --force-reinstall
```

## Development

### Running in Debug Mode

Debug mode is enabled by default in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

### Adding New Features

1. Define new routes in `app.py`
2. Create corresponding templates in `templates/`
3. Update navigation in `base.html`
4. Add new models in `models.py` if needed

## Security Considerations

⚠️ **For Production Deployment:**

1. Change the `SECRET_KEY` to a secure random value
2. Set `debug=False` in `app.run()`
3. Use a production WSGI server (Gunicorn, uWSGI)
4. Enable HTTPS
5. Implement user authentication
6. Add input sanitization
7. Use environment variables for sensitive data

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or contributions:
- Create an issue on GitHub
- Submit a pull request
- Contact the development team

## Screenshots

### Home Page
Dashboard with quick access to all modules

### Products Page
Complete product catalog management

### Locations Page
Warehouse and storage location management

### Movements Page
Track all inventory movements with type indicators

### Reports Page
Real-time inventory balance across all locations

---

**Built with ❤️ using Flask and Bootstrap 5**