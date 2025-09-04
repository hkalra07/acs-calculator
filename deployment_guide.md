# ACS Calculator Deployment Guide

## 🚀 **Deployment Options**

### **Option 1: Render (Recommended - Easiest)**
1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click "New Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Name**: acs-calculator
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python acs_server.py`
6. Deploy!

### **Option 2: Railway**
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway will auto-detect Python and deploy

### **Option 3: Heroku**
1. Install Heroku CLI: `curl https://cli-assets.heroku.com/install.sh | sh`
2. Login: `heroku login`
3. Create app: `heroku create acs-calculator-app`
4. Deploy: `git push heroku main`

### **Option 4: DigitalOcean App Platform**
1. Go to [digitalocean.com](https://digitalocean.com)
2. Create App Platform
3. Connect GitHub repository
4. Configure Python environment
5. Deploy

### **Option 5: Google Cloud Run**
1. Install gcloud CLI
2. Build container: `gcloud builds submit --tag gcr.io/PROJECT_ID/acs-calculator`
3. Deploy: `gcloud run deploy acs-calculator --image gcr.io/PROJECT_ID/acs-calculator`

## 📁 **Current Project Structure**
```
acs-calculator-project/
├── acs_calculator.html      # Frontend UI
├── acs_calculator.css       # Styles
├── acs_calculator.js        # Frontend logic
├── acs_server.py           # Backend server
├── client_reference_finder.py
├── google_sheets_backend.py
├── requirements.txt
├── data/                   # CSV files
├── render.yaml             # Render config
├── Procfile               # Heroku config
└── netlify.toml           # Netlify config
```

## 🔧 **Quick Deploy Commands**

### Render (Recommended)
```bash
# 1. Push to GitHub
git add .
git commit -m "Ready for deployment"
git push origin main

# 2. Deploy on Render
# - Go to render.com
# - Connect GitHub repo
# - Deploy automatically
```

### Railway
```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login and deploy
railway login
railway init
railway up
```

## 🌐 **Access Your Deployed App**
Once deployed, your app will be available at:
- **Render**: `https://acs-calculator.onrender.com`
- **Railway**: `https://acs-calculator-production.up.railway.app`
- **Heroku**: `https://acs-calculator-app.herokuapp.com`

## ✅ **Post-Deployment Checklist**
1. ✅ Test ACS calculation
2. ✅ Test Google Sheets integration
3. ✅ Test Client Reference Finder
4. ✅ Test country filtering
5. ✅ Verify all UI components work
6. ✅ Check mobile responsiveness

## 🛠 **Troubleshooting**
- **Import errors**: Check requirements.txt
- **File not found**: Verify data/ directory structure
- **CORS issues**: Check Access-Control headers
- **Google Sheets auth**: Verify service account credentials
