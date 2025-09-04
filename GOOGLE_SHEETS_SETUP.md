# Google Sheets Integration Setup Guide

## 🎯 **What We've Accomplished**

✅ **UI Cleanup**: Removed Google Sheets configuration section from the frontend  
✅ **Backend Ready**: Created Python backend for secure credential management  
✅ **Data Structure**: Configured to store only essential ACS data (no Business Implications)  
✅ **Automatic Flow**: All ACS calculations will automatically flow to your Google Sheet  

## 🚀 **Setup Steps**

### **Step 1: Google Cloud Project Setup**

1. **Go to [Google Cloud Console](https://console.cloud.google.com/)**
2. **Create a new project** or select existing one
3. **Enable Google Sheets API**:
   - Go to "APIs & Services" > "Library"
   - Search for "Google Sheets API"
   - Click "Enable"

### **Step 2: Create Service Account**

1. **Go to "APIs & Services" > "Credentials"**
2. **Click "Create Credentials" > "Service Account"**
3. **Fill in details**:
   - Name: `acs-calculator-service`
   - Description: `Service account for ACS Calculator Google Sheets integration`
4. **Click "Create and Continue"**
5. **Skip role assignment** (click "Continue")
6. **Click "Done"**

### **Step 3: Generate Private Key**

1. **Click on your service account** in the credentials list
2. **Go to "Keys" tab**
3. **Click "Add Key" > "Create new key"**
4. **Choose "JSON" format**
5. **Download the JSON file** (keep it secure!)

### **Step 4: Create Google Sheet**

1. **Go to [Google Sheets](https://sheets.google.com/)**
2. **Create a new spreadsheet**
3. **Name it**: `ACS Calculator Data`
4. **Copy the Spreadsheet ID** from the URL:
   ```
   https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit
   ```

### **Step 5: Share Sheet with Service Account**

1. **Click "Share" button** in your Google Sheet
2. **Add your service account email** (from the JSON file)
3. **Give it "Editor" access**
4. **Click "Send"**

### **Step 6: Configure Backend**

**Option A: Environment Variables**
```bash
export GOOGLE_SHEETS_SERVICE_ACCOUNT_EMAIL="your-service@project.iam.gserviceaccount.com"
export GOOGLE_SHEETS_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC..."
export GOOGLE_SHEETS_SPREADSHEET_ID="1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms"
```

**Option B: Config File**
Create `google_sheets_config.json`:
```json
{
  "service_account_email": "your-service@project.iam.gserviceaccount.com",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC...",
  "spreadsheet_id": "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms"
}
```

## 📊 **Data Structure**

Your Google Sheet will automatically create these columns:
- **Timestamp** - When calculation was made
- **Client Name** - Client organization name
- **Job Link** - Sample job posting URL (optional)
- **ATS Name** - Applicant Tracking System (optional)
- **Pages** - Number of application pages
- **Time to Fill** - Estimated completion time
- **Documents** - Documents required
- **Login Required** - Whether login is needed
- **ACS Score** - Final complexity score (1-5)
- **Raw Score** - Calculated raw score
- **Adjusted Score** - Score after login multiplier
- **Page Score** - Individual page factor score
- **Time Score** - Individual time factor score
- **Document Score** - Individual document factor score
- **Login Multiplier** - Applied multiplier value

## 🔧 **Installation & Testing**

1. **Install dependencies**:
   ```bash
   pip install -r requirements_google_sheets.txt
   ```

2. **Test configuration**:
   ```bash
   python3 google_sheets_backend.py
   ```

3. **Expected output**:
   ```
   === Google Sheets Backend Configuration ===
   Configured: True
   Service Account: ✓
   Private Key: ✓
   Spreadsheet ID: ✓
   ```

## 🎉 **What Happens Next**

Once configured:
- **Every ACS calculation** automatically goes to your Google Sheet
- **No user configuration** needed in the UI
- **Real-time updates** as users calculate ACS scores
- **Secure credential management** in the backend
- **Automatic fallback** to local storage if needed

## 🆘 **Troubleshooting**

**Common Issues:**
- **"Service account not found"**: Check email address spelling
- **"Permission denied"**: Ensure service account has Editor access to sheet
- **"Invalid private key"**: Check if private key includes `\n` characters
- **"API not enabled"**: Verify Google Sheets API is enabled in your project

**Need Help?**
- Check the logs in `google_sheets_backend.py`
- Verify your service account has the correct permissions
- Ensure your Google Cloud project has billing enabled

## 🔐 **Security Notes**

- **Never commit** the `google_sheets_config.json` file to version control
- **Keep your private key** secure and confidential
- **Use environment variables** in production environments
- **Rotate credentials** periodically for security

---

**Ready to proceed?** Once you complete the setup, all ACS calculations will automatically flow into your Google Sheet! 🚀
