# Deployment Guide - Inventory Management System

## 📦 Deployment Options

### Option 1: Local Development (Current Setup)

**Already Running!**
- URL: https://3000-5fd14a25-ec66-4074-a050-e08f92c00ea3.proxy.daytona.works
- Port: 3000
- Database: SQLite (instance/inventory.db)

### Option 2: Production Deployment

#### Using Gunicorn (Recommended)

1. **Install Gunicorn**
```bash
pip install gunicorn
```

2. **Run with Gunicorn**
```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

3. **With systemd service**
```ini
# /etc/systemd/system/inventory.service
[Unit]
Description=Inventory Management System
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/inventory_system
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/gunicorn -w 4 -b 0.0.0.0:8000 app:app

[Install]
WantedBy=multi-user.target
```

#### Using Docker

1. **Create Dockerfile**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY . .

EXPOSE 8000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
```

2. **Build and Run**
```bash
docker build -t inventory-system .
docker run -p 8000:8000 -v $(pwd)/instance:/app/instance inventory-system
```

#### Using Heroku

1. **Create Procfile**
```
web: gunicorn app:app
```

2. **Deploy**
```bash
heroku create inventory-system-app
git push heroku main
```

### Option 3: Cloud Platforms

#### AWS Elastic Beanstalk
```bash
eb init -p python-3.11 inventory-system
eb create inventory-env
eb deploy
```

#### Google Cloud Run
```bash
gcloud run deploy inventory-system \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

#### Azure App Service
```bash
az webapp up --name inventory-system --runtime "PYTHON:3.11"
```

---

## 🗄️ Database Migration

### From SQLite to PostgreSQL

1. **Install PostgreSQL adapter**
```bash
pip install psycopg2-binary
```

2. **Update app.py**
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/inventory_db'
```

3. **Export SQLite data**
```bash
sqlite3 instance/inventory.db .dump > backup.sql
```

4. **Import to PostgreSQL**
```bash
psql inventory_db < backup.sql
```

### From SQLite to MySQL

1. **Install MySQL adapter**
```bash
pip install pymysql
```

2. **Update app.py**
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:password@localhost/inventory_db'
```

---

## 🔒 Security Checklist

### Before Production Deployment

- [ ] Change SECRET_KEY to secure random value
- [ ] Set DEBUG = False
- [ ] Use environment variables for sensitive data
- [ ] Enable HTTPS/SSL
- [ ] Implement user authentication
- [ ] Add rate limiting
- [ ] Enable CORS if needed
- [ ] Set up database backups
- [ ] Configure logging
- [ ] Add monitoring (Sentry, New Relic)

### Environment Variables

Create `.env` file:
```bash
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=sqlite:///instance/inventory.db
FLASK_ENV=production
```

Update `app.py`:
```python
import os
from dotenv import load_dotenv

load_dotenv()

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
```

---

## 🌐 Nginx Configuration

```nginx
server {
    listen 80;
    server_name inventory.example.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static {
        alias /path/to/inventory_system/static;
    }
}
```

---

## 📊 Performance Optimization

### 1. Enable Caching
```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/reports')
@cache.cached(timeout=300)
def reports():
    # ... existing code
```

### 2. Database Indexing
```python
# Add indexes to models.py
class ProductMovement(db.Model):
    # ... existing fields
    
    __table_args__ = (
        db.Index('idx_product_location', 'product_id', 'to_location'),
        db.Index('idx_timestamp', 'timestamp'),
    )
```

### 3. Connection Pooling
```python
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,
    'pool_recycle': 3600,
    'pool_pre_ping': True
}
```

---

## 🔄 Backup Strategy

### Automated Backups

```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"

# Backup database
cp instance/inventory.db "$BACKUP_DIR/inventory_$DATE.db"

# Keep only last 7 days
find $BACKUP_DIR -name "inventory_*.db" -mtime +7 -delete
```

### Cron Job
```bash
# Run daily at 2 AM
0 2 * * * /path/to/backup.sh
```

---

## 📈 Monitoring

### Application Monitoring

```python
# Add to app.py
from flask import request
import logging

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

@app.before_request
def log_request():
    logging.info(f'{request.method} {request.path}')
```

### Health Check Endpoint

```python
@app.route('/health')
def health():
    try:
        # Check database connection
        db.session.execute('SELECT 1')
        return {'status': 'healthy'}, 200
    except:
        return {'status': 'unhealthy'}, 500
```

---

## 🚀 CI/CD Pipeline

### GitHub Actions Example

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: python -m pytest
      - name: Deploy to production
        run: |
          # Your deployment commands here
```

---

## 📝 Maintenance Tasks

### Regular Maintenance

1. **Database Optimization**
```sql
VACUUM;
ANALYZE;
```

2. **Log Rotation**
```bash
logrotate /etc/logrotate.d/inventory-app
```

3. **Dependency Updates**
```bash
pip list --outdated
pip install --upgrade -r requirements.txt
```

---

## 🆘 Troubleshooting

### Common Issues

**Issue: Database locked**
```python
# Add to app.py
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'connect_args': {'timeout': 15}
}
```

**Issue: Memory usage high**
```python
# Limit query results
movements = ProductMovement.query.limit(1000).all()
```

**Issue: Slow reports**
```python
# Add database indexes
# Optimize queries with joins
```

---

## 📞 Support & Resources

- **Documentation**: See README.md
- **Issues**: Create GitHub issue
- **Updates**: Check for new releases

---

**Current Status**: ✅ Running on port 3000
**Public URL**: https://3000-5fd14a25-ec66-4074-a050-e08f92c00ea3.proxy.daytona.works