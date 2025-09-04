# ACS Calculator Tool

A comprehensive Application Complexity Score (ACS) calculator with client reference finder functionality.

## 🚀 Features

### Phase 1: ACS Calculator
- Calculate ACS scores (1-5) based on application complexity factors
- Real-time calculation as you fill the form
- Detailed business implications for each score level
- Professional UI with Joveo branding

### Phase 2: Data Storage
- Automatic storage of calculations in Google Sheets
- Secure backend integration
- No sensitive configuration exposed in frontend

### Phase 3: Client Reference Finder
- Find similar clients based on ACS scores and job categories
- Country/location filtering for more relevant results
- Sample job titles and client information
- Advanced filtering logic

## 🛠️ Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Backend**: Python 3.9+
- **Data Storage**: Google Sheets API
- **Deployment**: Vercel (Serverless Functions)
- **Data Processing**: Pandas, NumPy

## 📁 Project Structure

```
├── acs_calculator.html          # Main frontend interface
├── acs_calculator.css           # Styling
├── acs_calculator.js            # Frontend logic
├── api/
│   └── index.py                 # Serverless API endpoints
├── acs_server.py                # Local development server
├── client_reference_finder.py   # Client matching logic
├── google_sheets_backend.py     # Google Sheets integration
├── google_sheets_config.json    # Google Sheets configuration
├── client_countries.csv         # Client-country mappings
├── 2025-08-29 3_39pm.csv        # Job data
├── requirements.txt             # Python dependencies
├── vercel.json                  # Vercel configuration
└── README.md                    # This file
```

## 🚀 Deployment Instructions

### Option 1: Vercel Deployment (Recommended)

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Configure Environment Variables**:
   Create a `.env` file or set in Vercel dashboard:
   ```
   GOOGLE_SHEETS_EMAIL=your-service-account@project.iam.gserviceaccount.com
   GOOGLE_SHEETS_PRIVATE_KEY=your-private-key
   GOOGLE_SHEETS_SPREADSHEET_ID=your-spreadsheet-id
   ```

3. **Deploy**:
   ```bash
   vercel
   ```

4. **Set Production Domain**:
   ```bash
   vercel --prod
   ```

### Option 2: Netlify Deployment

1. **Create `netlify.toml`**:
   ```toml
   [build]
     publish = "."
     functions = "api"
   
   [[redirects]]
     from = "/api/*"
     to = "/.netlify/functions/index"
     status = 200
   ```

2. **Deploy via Netlify Dashboard** or CLI

## 🔧 Local Development

1. **Install Dependencies**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure Google Sheets**:
   - Follow `GOOGLE_SHEETS_SETUP.md` for setup instructions
   - Update `google_sheets_config.json` with your credentials

3. **Run Local Server**:
   ```bash
   python3 acs_server.py
   ```

4. **Access Application**:
   - Frontend: http://localhost:8000/acs_calculator.html
   - API Status: http://localhost:8000/status

## 📊 Data Files

### Required Data Files:
- `client_countries.csv`: Client-country mappings (657 entries)
- `2025-08-29 3_39pm.csv`: Job posting data (361,062 entries)

### Data Format:
- **Client Countries**: `CLIENT_NAME, NORMALISED_COUNTRY`
- **Job Data**: `CLIENT_NAME, JOB_TITLE, DETAIL_NORMALISED_CATEGORY`

## 🔌 API Endpoints

### GET Endpoints:
- `/api/status` - Check service status
- `/api/spreadsheet-info` - Google Sheets connection info

### POST Endpoints:
- `/api/store-calculation` - Store ACS calculation
- `/api/find-similar-clients` - Find similar clients

### Request Format for Similar Clients:
```json
{
  "target_acs": 3,
  "target_category": "Software Developers",
  "target_country": "United States",
  "max_results": 10
}
```

## 🎯 ACS Score Calculation

The ACS formula considers:
- **Pages** (20% weight): Number of application pages
- **Time** (60% weight): Time to complete application
- **Documents** (20% weight): Required documents
- **Login** (Multiplier): 1.2x if login required

Final scores range from 1 (Very Simple) to 5 (Very Complex).

## 🌍 Country Filtering

The tool supports filtering by 50+ countries including:
- United States, Germany, United Kingdom, Canada
- Switzerland, Netherlands, France, Austria
- And many more...

## 🔒 Security

- Google Sheets credentials stored securely
- No sensitive data exposed in frontend
- CORS properly configured
- Input validation on all endpoints

## 📈 Performance

- Serverless architecture for scalability
- Efficient data processing with Pandas
- Optimized client matching algorithms
- Fast response times (< 2 seconds)

## 🐛 Troubleshooting

### Common Issues:

1. **Google Sheets Connection Failed**:
   - Check service account credentials
   - Verify spreadsheet permissions
   - Ensure environment variables are set

2. **No Similar Clients Found**:
   - Verify job category spelling
   - Check if country name matches exactly
   - Ensure ACS score is valid (1-5)

3. **Deployment Issues**:
   - Check Vercel/Netlify logs
   - Verify `vercel.json` configuration
   - Ensure all files are committed

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review server logs
3. Verify data file formats
4. Test with local development first

## 📝 License

This project is proprietary to Joveo. All rights reserved.
