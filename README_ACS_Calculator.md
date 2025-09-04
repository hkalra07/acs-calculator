# ACS Calculator - Application Complexity Score Tool

## Overview

The ACS Calculator is a professional web application designed for business teams to calculate Application Complexity Scores (ACS) for job application processes. This tool helps optimize conversion rates and cost-per-application (CPA) by providing insights into application complexity.

## Features

### Phase 1: ACS Calculator ✅
- **Professional UI**: Clean, modern interface matching Joveo's design system
- **Input Form**: Collects all necessary factors for ACS calculation
- **Real-time Validation**: Ensures all required fields are completed
- **Instant Calculation**: Provides ACS score (1-5) with detailed explanations
- **Business Insights**: Clear implications and recommendations for each score level

### Phase 2: Data Storage (Planned)
- **Google Sheets Integration**: Store calculation results for analysis
- **Snowflake Integration**: Flow data to enterprise data warehouse
- **Historical Tracking**: Maintain calculation history and trends

### Phase 3: Client Reference Finder (Planned)
- **Job Category Matching**: Find clients with similar ACS scores
- **CPA Estimation**: Reference similar client profiles for cost planning
- **Performance Insights**: Learn from comparable application processes

## How to Use

### 1. Access the Tool
Open `acs_calculator.html` in any modern web browser.

### 2. Fill Out the Form
Complete all required fields marked with red asterisks (*):

#### Client Information
- **Client Name**: Enter the organization name
- **Sample Job Link**: Optional URL to the job posting
- **ATS Name**: Optional Applicant Tracking System name

#### Application Complexity Factors
- **Number of Pages**: Select from 1, 2-5, or >5 pages
- **Time to Fill**: Choose <5 min, 5-15 min, or >15 min
- **Documents Required**: Select 0, 1, or >1 documents
- **Login Required**: Choose Yes or No

### 3. Calculate ACS
Click "Calculate ACS Score" to generate your complexity score.

### 4. Review Results
The tool will display:
- **ACS Score**: Visual score circle (1-5)
- **Score Explanation**: What the score means
- **Business Implications**: Detailed recommendations and insights

## ACS Score Interpretation

### ACS 1: Very Low Complexity
- **Volume Potential**: Very high
- **CPA Impact**: Lowest cost-per-application
- **Best For**: High-volume campaigns, entry-level positions
- **Recommendation**: Focus on volume optimization

### ACS 2: Low Complexity
- **Volume Potential**: High
- **CPA Impact**: Low to moderate
- **Best For**: Most recruitment campaigns
- **Recommendation**: Balance volume and quality

### ACS 3: Moderate Complexity
- **Volume Potential**: Medium
- **CPA Impact**: Moderate
- **Best For**: Mid-level positions
- **Recommendation**: Balance volume and quality optimization

### ACS 4: High Complexity
- **Volume Potential**: Low to medium
- **CPA Impact**: Higher
- **Best For**: Senior positions
- **Recommendation**: Focus on quality optimization

### ACS 5: Very High Complexity
- **Volume Potential**: Very low
- **CPA Impact**: Highest
- **Best For**: Executive positions, specialized roles
- **Recommendation**: Consider process simplification

## Technical Details

### Files Structure
```
acs_calculator/
├── acs_calculator.html      # Main HTML interface
├── acs_calculator.css       # Styling and layout
├── acs_calculator.js        # Calculation logic and interactions
└── README_ACS_Calculator.md # This documentation
```

### Technology Stack
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Icons**: Font Awesome 6.0
- **Design**: Responsive, mobile-friendly interface
- **Storage**: Local storage (temporary), Google Sheets integration planned

### Browser Compatibility
- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

## Future Enhancements

### Phase 2: Data Integration
- Google Sheets API integration
- Automated data collection and storage
- Historical analysis and trending

### Phase 3: Advanced Analytics
- Client reference finder
- Job category matching
- CPA estimation tools
- Performance benchmarking

### Additional Features
- Export functionality (PDF, Excel)
- Team collaboration features
- Advanced reporting and analytics
- Integration with existing Joveo systems

## Development Notes

### ACS Formula (Hidden from Users)
The tool uses the official ACS formula:
```
ACS = (Page Score × 0.2) + (Time Score × 0.6) + (Document Score × 0.2) × Login Multiplier
```

### Scoring System
- **Pages**: 1 page (1), 2-5 pages (3), >5 pages (6)
- **Time**: <5 min (1), 5-15 min (4), >15 min (8)
- **Documents**: 0 (1), 1 (3), >1 (6)
- **Login**: No (1.0), Yes (1.2)

### Thresholds
- ≤1.5 → ACS 1
- ≤2.5 → ACS 2
- ≤3.5 → ACS 3
- ≤4.5 → ACS 4
- >4.5 → ACS 5

## Support and Feedback

For technical support or feature requests, please contact the development team.

## Version History

### v1.0.0 (Current)
- Initial ACS calculator implementation
- Professional UI matching Joveo design system
- Complete calculation logic and business insights
- Local data storage
- Responsive design for all devices

---

**Note**: This tool is designed for internal business use and follows Joveo's design standards and business processes.
