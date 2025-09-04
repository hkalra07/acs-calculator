#!/usr/bin/env python3
"""
Google Sheets Backend for ACS Calculator
This file handles the backend configuration and integration with Google Sheets
"""

import os
import json
from datetime import datetime
from typing import Dict, Any, Optional
import logging
import gspread
from google.oauth2.service_account import Credentials
from google.auth.exceptions import GoogleAuthError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GoogleSheetsBackend:
    """
    Backend class for Google Sheets integration
    All credentials and configuration are handled here
    """
    
    def __init__(self):
        self.service_account_email = None
        self.private_key = None
        self.spreadsheet_id = None
        self.sheet_name = "ACS_Calculations"
        self.is_configured = False
        self.gc = None  # gspread client
        self.spreadsheet = None
        self.worksheet = None
        
        # Load configuration from environment or config file
        self.load_configuration()
        
        # Initialize Google Sheets connection if configured
        if self.is_configured:
            self.initialize_google_sheets()
    
    def load_configuration(self):
        """Load Google Sheets configuration from environment variables or config file"""
        try:
            # Try environment variables first
            self.service_account_email = os.getenv('GOOGLE_SHEETS_SERVICE_ACCOUNT_EMAIL')
            self.private_key = os.getenv('GOOGLE_SHEETS_PRIVATE_KEY')
            self.spreadsheet_id = os.getenv('GOOGLE_SHEETS_SPREADSHEET_ID')
            
            # If not in environment, try config file
            if not all([self.service_account_email, self.private_key, self.spreadsheet_id]):
                self.load_config_from_file()
            
            # Validate configuration
            if all([self.service_account_email, self.private_key, self.spreadsheet_id]):
                self.is_configured = True
                logger.info("Google Sheets configuration loaded successfully")
            else:
                logger.warning("Google Sheets configuration incomplete")
                
        except Exception as e:
            logger.error(f"Error loading Google Sheets configuration: {e}")
    
    def load_config_from_file(self):
        """Load configuration from a config file"""
        config_file = "google_sheets_config.json"
        try:
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    self.service_account_email = config.get('service_account_email')
                    self.private_key = config.get('private_key')
                    self.spreadsheet_id = config.get('spreadsheet_id')
                    logger.info("Configuration loaded from config file")
            else:
                logger.info("No config file found, using environment variables")
        except Exception as e:
            logger.error(f"Error loading config file: {e}")
    
    def initialize_google_sheets(self):
        """Initialize Google Sheets connection using gspread"""
        try:
            # Create credentials from service account
            credentials = Credentials.from_service_account_info({
                "type": "service_account",
                "project_id": "acs-calculator-project",
                "private_key_id": "key_id_from_json",
                "private_key": self.private_key,
                "client_email": self.service_account_email,
                "client_id": "client_id_from_json",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{self.service_account_email}"
            }, scopes=['https://www.googleapis.com/auth/spreadsheets'])
            
            # Create gspread client
            self.gc = gspread.authorize(credentials)
            
            # Open spreadsheet
            self.spreadsheet = self.gc.open_by_key(self.spreadsheet_id)
            
            # Get or create worksheet
            try:
                self.worksheet = self.spreadsheet.worksheet(self.sheet_name)
                logger.info(f"Connected to existing worksheet: {self.sheet_name}")
            except gspread.WorksheetNotFound:
                # Create new worksheet with headers
                self.worksheet = self.spreadsheet.add_worksheet(
                    title=self.sheet_name, 
                    rows=1000, 
                    cols=20
                )
                self.setup_headers()
                logger.info(f"Created new worksheet: {self.sheet_name}")
            
            logger.info("Google Sheets connection established successfully")
            
        except GoogleAuthError as e:
            logger.error(f"Google authentication error: {e}")
            self.is_configured = False
        except Exception as e:
            logger.error(f"Error initializing Google Sheets: {e}")
            self.is_configured = False
    
    def setup_headers(self):
        """Set up column headers for the ACS data"""
        headers = [
            'Timestamp',
            'Client Name',
            'Job Link',
            'ATS Name',
            'Pages',
            'Time to Fill',
            'Documents',
            'Login Required',
            'ACS Score',
            'Raw Score',
            'Adjusted Score',
            'Page Score',
            'Time Score',
            'Document Score',
            'Login Multiplier'
        ]
        
        try:
            self.worksheet.update('A1:O1', [headers])
            self.worksheet.format('A1:O1', {
                'textFormat': {'bold': True},
                'backgroundColor': {'red': 0.9, 'green': 0.9, 'blue': 0.9}
            })
            logger.info("Headers set up successfully")
        except Exception as e:
            logger.error(f"Error setting up headers: {e}")
    
    def save_configuration(self, service_account_email: str, private_key: str, spreadsheet_id: str):
        """Save configuration to config file"""
        try:
            config = {
                'service_account_email': service_account_email,
                'private_key': private_key,
                'spreadsheet_id': spreadsheet_id,
                'last_updated': datetime.now().isoformat()
            }
            
            with open("google_sheets_config.json", 'w') as f:
                json.dump(config, f, indent=2)
            
            # Update instance variables
            self.service_account_email = service_account_email
            self.private_key = private_key
            self.spreadsheet_id = spreadsheet_id
            self.is_configured = True
            
            logger.info("Configuration saved successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
            return False
    
    def get_configuration_status(self) -> Dict[str, Any]:
        """Get current configuration status"""
        return {
            'is_configured': self.is_configured,
            'has_service_account': bool(self.service_account_email),
            'has_private_key': bool(self.private_key),
            'has_spreadsheet_id': bool(self.spreadsheet_id),
            'spreadsheet_id': self.spreadsheet_id if self.is_configured else None,
            'worksheet_name': self.sheet_name if self.is_configured else None,
            'connection_status': 'Connected' if self.worksheet else 'Not Connected'
        }
    
    def store_acs_calculation(self, acs_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Store ACS calculation data in Google Sheets
        """
        if not self.is_configured or not self.worksheet:
            return {
                'success': False,
                'message': 'Google Sheets not configured or connected',
                'data_stored_locally': True
            }
        
        try:
            # Prepare data row
            row_data = [
                acs_data.get('timestamp', datetime.now().isoformat()),
                acs_data.get('clientName', ''),
                acs_data.get('jobLink', ''),
                acs_data.get('atsName', ''),
                acs_data.get('pages', ''),
                acs_data.get('timeToFill', ''),
                acs_data.get('documents', ''),
                acs_data.get('loginRequired', ''),
                acs_data.get('acsScore', ''),
                acs_data.get('rawScore', ''),
                acs_data.get('adjustedScore', ''),
                acs_data.get('pageScore', ''),
                acs_data.get('timeScore', ''),
                acs_data.get('documentScore', ''),
                acs_data.get('loginMultiplier', '')
            ]
            
            # Append row to worksheet
            self.worksheet.append_row(row_data)
            
            # Get the row number (last row)
            row_number = len(self.worksheet.get_all_values())
            
            logger.info(f"ACS calculation data stored successfully in row {row_number}")
            
            return {
                'success': True,
                'message': 'Data stored in Google Sheets',
                'row_number': row_number,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error storing ACS calculation: {e}")
            return {
                'success': False,
                'message': f'Error: {str(e)}',
                'data_stored_locally': True
            }
    
    def get_spreadsheet_info(self) -> Dict[str, Any]:
        """Get information about the connected spreadsheet"""
        if not self.spreadsheet:
            return {'error': 'Not connected to spreadsheet'}
        
        try:
            return {
                'title': self.spreadsheet.title,
                'url': self.spreadsheet.url,
                'worksheet_name': self.sheet_name,
                'total_rows': len(self.worksheet.get_all_values()) if self.worksheet else 0
            }
        except Exception as e:
            return {'error': str(e)}

def main():
    """Main function to test the backend configuration"""
    backend = GoogleSheetsBackend()
    
    print("=== Google Sheets Backend Configuration ===")
    print(f"Configured: {backend.is_configured}")
    print(f"Service Account: {'✓' if backend.service_account_email else '✗'}")
    print(f"Private Key: {'✓' if backend.private_key else '✗'}")
    print(f"Spreadsheet ID: {'✓' if backend.spreadsheet_id else '✗'}")
    print(f"Connection Status: {backend.get_configuration_status().get('connection_status', 'Unknown')}")
    
    if backend.is_configured and backend.spreadsheet:
        print(f"\nSpreadsheet Info:")
        info = backend.get_spreadsheet_info()
        for key, value in info.items():
            print(f"  {key}: {value}")
    
    if not backend.is_configured:
        print("\nTo configure Google Sheets integration, you need to:")
        print("1. Set environment variables:")
        print("   export GOOGLE_SHEETS_SERVICE_ACCOUNT_EMAIL='your-service-account@project.iam.gserviceaccount.com'")
        print("   export GOOGLE_SHEETS_PRIVATE_KEY='-----BEGIN PRIVATE KEY-----...'")
        print("   export GOOGLE_SHEETS_SPREADSHEET_ID='your-spreadsheet-id'")
        print("\n2. Or create a config file: google_sheets_config.json")
        print("3. Or call backend.save_configuration(email, key, spreadsheet_id)")
    
    # Test with sample data
    sample_data = {
        'clientName': 'Test Client',
        'acsScore': 3,
        'timestamp': datetime.now().isoformat(),
        'pages': '2-5',
        'timeToFill': '5-15',
        'documents': '1',
        'loginRequired': True,
        'rawScore': '3.2',
        'adjustedScore': '3.84',
        'pageScore': 3,
        'timeScore': 4,
        'documentScore': 3,
        'loginMultiplier': 1.2
    }
    
    result = backend.store_acs_calculation(sample_data)
    print(f"\nTest storage result: {result}")

if __name__ == "__main__":
    main()
