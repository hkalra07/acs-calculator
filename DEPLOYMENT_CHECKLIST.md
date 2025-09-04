# 🚀 Deployment Checklist

## ✅ Pre-Deployment Checklist

### 1. Code Review
- [ ] All features working locally
- [ ] Country filtering tested and working
- [ ] Similarity score removed from UI
- [ ] API endpoints updated for deployment
- [ ] Error handling implemented

### 2. Data Files
- [ ] `client_countries.csv` - 657 client-country mappings
- [ ] `2025-08-29 3_39pm.csv` - 361,062 job postings
- [ ] All data files committed to repository

### 3. Configuration Files
- [ ] `requirements.txt` - Python dependencies
- [ ] `vercel.json` - Vercel configuration
- [ ] `netlify.toml` - Netlify configuration (alternative)
- [ ] `api/index.py` - Serverless API endpoints
- [ ] `index.html` - Landing page

### 4. Environment Variables (Set in Vercel/Netlify Dashboard)
- [ ] `GOOGLE_SHEETS_EMAIL` - Service account email
- [ ] `GOOGLE_SHEETS_PRIVATE_KEY` - Private key (with newlines)
- [ ] `GOOGLE_SHEETS_SPREADSHEET_ID` - Spreadsheet ID

### 5. Google Sheets Setup
- [ ] Service account created
- [ ] Spreadsheet shared with service account
- [ ] Worksheet "ACS_Calculations" exists
- [ ] Permissions verified

## 🚀 Deployment Steps

### Vercel Deployment
1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy**:
   ```bash
   vercel
   ```

4. **Set Environment Variables** in Vercel Dashboard:
   - Go to Project Settings → Environment Variables
   - Add all required environment variables

5. **Deploy to Production**:
   ```bash
   vercel --prod
   ```

### Netlify Deployment (Alternative)
1. **Connect Repository** to Netlify
2. **Set Build Settings**:
   - Build command: (leave empty)
   - Publish directory: `.`
3. **Set Environment Variables** in Netlify Dashboard
4. **Deploy**

## 🧪 Post-Deployment Testing

### 1. Basic Functionality
- [ ] Landing page loads correctly
- [ ] ACS Calculator form accessible
- [ ] Form validation working
- [ ] ACS calculation working
- [ ] Results display correctly

### 2. Data Storage
- [ ] Google Sheets integration working
- [ ] Calculations stored successfully
- [ ] No sensitive data exposed

### 3. Client Reference Finder
- [ ] Modal opens correctly
- [ ] Job category dropdown populated
- [ ] Country input field working
- [ ] Search functionality working
- [ ] Results display with country info
- [ ] Country filtering working

### 4. API Endpoints
- [ ] `/api/status` - Returns service status
- [ ] `/api/store-calculation` - Stores data
- [ ] `/api/find-similar-clients` - Finds clients
- [ ] CORS headers set correctly

### 5. Performance
- [ ] Page load time < 3 seconds
- [ ] API response time < 2 seconds
- [ ] No console errors
- [ ] Mobile responsive

## 🔧 Troubleshooting

### Common Issues:
1. **Environment Variables Not Set**:
   - Check Vercel/Netlify dashboard
   - Verify variable names match exactly

2. **Google Sheets Connection Failed**:
   - Verify service account permissions
   - Check private key format (include newlines)
   - Ensure spreadsheet is shared

3. **API Endpoints Not Working**:
   - Check `vercel.json` routing
   - Verify function deployment
   - Check serverless function logs

4. **Data Files Missing**:
   - Ensure CSV files are committed
   - Check file paths in code
   - Verify file permissions

## 📊 Monitoring

### Set Up Monitoring:
- [ ] Vercel Analytics enabled
- [ ] Error tracking configured
- [ ] Performance monitoring active
- [ ] Uptime monitoring set up

### Key Metrics to Track:
- Page load times
- API response times
- Error rates
- User engagement
- Feature usage

## 🔒 Security Review

- [ ] No sensitive data in frontend
- [ ] API endpoints secured
- [ ] CORS properly configured
- [ ] Input validation implemented
- [ ] Rate limiting considered

## 📝 Documentation

- [ ] README.md updated
- [ ] API documentation complete
- [ ] Deployment instructions clear
- [ ] Troubleshooting guide ready

## 🎯 Final Checklist

- [ ] All tests passing
- [ ] Production URL working
- [ ] Team access granted
- [ ] Monitoring active
- [ ] Backup strategy in place
- [ ] Rollback plan ready

---

**Deployment Status**: ✅ Ready for Production

**Next Steps**:
1. Deploy to staging environment
2. Run full test suite
3. Deploy to production
4. Monitor for 24 hours
5. Announce to team
