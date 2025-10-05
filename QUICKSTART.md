# Quick Start Guide - Inventory Management System

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
cd inventory_system
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python app.py
```

### Step 3: Access the Application
Open your browser to: **http://localhost:3000**

---

## 🎯 First Time User Guide

### 1. Explore the Dashboard
- Click on the **Home** link to see the main dashboard
- View the 4 main modules: Products, Locations, Movements, Reports

### 2. View Sample Data
The application comes pre-loaded with sample data:
- **4 Products** - Electronics items
- **4 Locations** - Warehouses across different cities
- **20 Movements** - Various inventory transactions

### 3. Try Adding a Product
1. Click **Products** in the navigation
2. Click **Add New Product** button
3. Enter product name (e.g., "Keyboard Mechanical")
4. Add description (optional)
5. Click **Save Product**

### 4. Create a Movement
1. Click **Movements** in the navigation
2. Click **Add New Movement** button
3. Select a product from dropdown
4. Choose movement type:
   - **Incoming**: Leave "From Location" empty, select "To Location"
   - **Outgoing**: Select "From Location", leave "To Location" empty
   - **Transfer**: Select both locations
5. Enter quantity
6. Click **Save Movement**

### 5. View Inventory Report
1. Click **Reports** in the navigation
2. See real-time balance for each product in each location
3. Green badges = stock available
4. Red badges = negative balance (check for errors)

---

## 📋 Common Tasks

### Add Incoming Stock
```
Products → Select Product
Movements → Add New Movement
From Location: (Leave empty)
To Location: Main Warehouse
Quantity: 50
```

### Transfer Between Warehouses
```
Movements → Add New Movement
From Location: Main Warehouse
To Location: Retail Store
Quantity: 10
```

### Record Sales (Outgoing)
```
Movements → Add New Movement
From Location: Retail Store
To Location: (Leave empty)
Quantity: 5
```

---

## 🔍 Understanding the Report

The **Inventory Balance Report** shows:
- **Product**: Item name
- **Warehouse**: Location name
- **Qty**: Current balance

**Balance Calculation:**
```
Balance = (Items moved IN) - (Items moved OUT)
Balance = SUM(to_location qty) - SUM(from_location qty)
```

---

## ⚠️ Important Rules

1. **At least one location** must be selected (From or To)
2. **From and To locations** cannot be the same
3. **Quantity** must be greater than 0
4. **Cannot delete** products/locations with existing movements
5. **Timestamps** are set automatically

---

## 🎨 Navigation Overview

| Menu Item | Purpose |
|-----------|---------|
| **Home** | Dashboard with quick access cards |
| **Products** | Manage product catalog |
| **Locations** | Manage warehouses/stores |
| **Movements** | Track inventory movements |
| **Reports** | View inventory balances |

---

## 💡 Tips & Tricks

1. **Use descriptive names** for products and locations
2. **Add descriptions** to products for better tracking
3. **Check reports regularly** to monitor stock levels
4. **Negative balances** indicate data entry errors
5. **Edit movements** if you make a mistake
6. **Use transfers** to move stock between locations

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Edit app.py and change the port number
app.run(debug=True, host='0.0.0.0', port=3001)
```

### Database Issues
```bash
# Delete and recreate database
rm instance/inventory.db
python app.py
```

### Missing Dependencies
```bash
pip install -r requirements.txt --force-reinstall
```

---

## 📚 Next Steps

1. ✅ Explore all features
2. ✅ Add your own products and locations
3. ✅ Create realistic movement scenarios
4. ✅ Monitor inventory through reports
5. ✅ Customize the application for your needs

---

## 🎓 Learning Resources

- **Flask Documentation**: https://flask.palletsprojects.com/
- **SQLAlchemy Tutorial**: https://docs.sqlalchemy.org/
- **Bootstrap 5 Docs**: https://getbootstrap.com/docs/5.3/

---

**Ready to start? Run `python app.py` and open http://localhost:3000**

🎉 **Happy Inventory Managing!**