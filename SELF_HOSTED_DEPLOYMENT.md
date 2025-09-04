# 🏠 Self-Hosted ACS Calculator Deployment Guide

## 🚀 **Quick Start (5 minutes)**

### **Step 1: Start the Production Server**
```bash
# Navigate to your project directory
cd /home/coder/acs-calculator-project

# Start the production server
python3 acs_server_production.py
```

### **Step 2: Access Your Application**
- **Frontend**: http://localhost:8000/acs_calculator.html
- **API Status**: http://localhost:8000/status
- **Root URL**: http://localhost:8000/ (redirects to calculator)

## 🌐 **Making it Accessible from Internet**

### **Option 1: Port Forwarding (Home Network)**
1. **Find your local IP**: `ip addr show` or `ifconfig`
2. **Configure router port forwarding**:
   - External Port: 80 or 443
   - Internal IP: Your server IP
   - Internal Port: 8000
3. **Access via**: `http://YOUR_PUBLIC_IP/acs_calculator.html`

### **Option 2: Cloud Server (Recommended)**
1. **Rent a VPS** (DigitalOcean, AWS EC2, Google Cloud)
2. **SSH into server**:
   ```bash
   ssh user@your-server-ip
   ```
3. **Clone and deploy**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/acs-calculator.git
   cd acs-calculator
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python3 acs_server_production.py
   ```

### **Option 3: Domain + Reverse Proxy**
1. **Buy a domain** (Namecheap, GoDaddy)
2. **Set up Nginx reverse proxy**:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```
3. **Access via**: `https://your-domain.com/acs_calculator.html`

## 🔧 **Production Setup**

### **Auto-Start on Boot**
```bash
# Create systemd service
sudo cp acs-calculator.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable acs-calculator
sudo systemctl start acs-calculator
```

### **SSL Certificate (HTTPS)**
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d your-domain.com
```

### **Firewall Configuration**
```bash
# Allow HTTP and HTTPS
sudo ufw allow 80
sudo ufw allow 443
sudo ufw allow 8000  # Only if not using reverse proxy
```

## 📊 **Monitoring & Logs**

### **View Logs**
```bash
# Application logs
tail -f acs_calculator.log

# System service logs
sudo journalctl -u acs-calculator -f
```

### **Health Check**
```bash
# Check if server is running
curl http://localhost:8000/status

# Expected response:
{
  "success": true,
  "status": {
    "is_configured": true,
    "google_sheets_connected": true,
    "client_finder_ready": true,
    "server": "Production ACS Calculator",
    "version": "1.0.0"
  }
}
```

## 🔒 **Security Considerations**

### **Environment Variables**
```bash
# Create .env file for sensitive data
export GOOGLE_SHEETS_PRIVATE_KEY="your-private-key"
export GOOGLE_SHEETS_SPREADSHEET_ID="your-spreadsheet-id"
```

### **Firewall Rules**
```bash
# Only allow necessary ports
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

### **Regular Updates**
```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Update system packages
sudo apt update && sudo apt upgrade
```

## 🚨 **Troubleshooting**

### **Common Issues**

#### **Port Already in Use**
```bash
# Find process using port 8000
sudo lsof -i :8000

# Kill the process
sudo kill -9 PID
```

#### **Permission Denied**
```bash
# Fix file permissions
chmod +x acs_server_production.py
chmod 644 *.html *.css *.js
```

#### **Google Sheets Connection Failed**
```bash
# Check configuration
cat google_sheets_config.json

# Test connection
python3 -c "from google_sheets_backend import GoogleSheetsBackend; gs = GoogleSheetsBackend(); print('Connected:', gs.is_connected())"
```

### **Performance Optimization**

#### **Increase Memory Limit**
```bash
# Edit systemd service
sudo nano /etc/systemd/system/acs-calculator.service

# Add memory limit
Environment=PYTHONUNBUFFERED=1
```

#### **Enable Gzip Compression**
```nginx
# In Nginx config
gzip on;
gzip_types text/plain text/css application/json application/javascript;
```

## 📈 **Scaling Options**

### **Load Balancer**
```nginx
upstream acs_calculator {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
}
```

### **Multiple Instances**
```bash
# Start multiple instances on different ports
python3 acs_server_production.py --port 8000 &
python3 acs_server_production.py --port 8001 &
python3 acs_server_production.py --port 8002 &
```

## ✅ **Deployment Checklist**

- [ ] ✅ Server starts without errors
- [ ] ✅ Frontend loads correctly
- [ ] ✅ ACS calculation works
- [ ] ✅ Google Sheets integration works
- [ ] ✅ Client Reference Finder works
- [ ] ✅ Country filtering works
- [ ] ✅ SSL certificate installed (if using domain)
- [ ] ✅ Firewall configured
- [ ] ✅ Auto-start enabled
- [ ] ✅ Monitoring/logging set up
- [ ] ✅ Backup strategy in place

## 🎯 **Final Result**

Your self-hosted ACS Calculator will be available at:
- **Local**: http://localhost:8000/acs_calculator.html
- **Network**: http://YOUR_IP:8000/acs_calculator.html
- **Domain**: https://your-domain.com/acs_calculator.html

**Features Available:**
- ✅ ACS Score calculation
- ✅ Google Sheets data storage
- ✅ Client Reference Finder
- ✅ Country-based filtering
- ✅ Production-ready logging
- ✅ CORS support for cross-origin requests
