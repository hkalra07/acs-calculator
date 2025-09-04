#!/usr/bin/env python3
""" 
ACS Calculator Server
Simple HTTP server to connect frontend with Google Sheets backend
"""

import json
import logging
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from google_sheets_backend import GoogleSheetsBackend
from datetime import datetime
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ACSCalculatorHandler(BaseHTTPRequestHandler):
    """HTTP request handler for ACS Calculator"""
    
    def __init__(self, *args, **kwargs):
        self.backend = None
        self.backend_initialized = False
        super().__init__(*args, **kwargs)
    
    def get_backend(self):
        """Lazy initialization of Google Sheets backend"""
        if not self.backend_initialized:
            try:
                self.backend = GoogleSheetsBackend()
                self.backend_initialized = True
                logger.info("Google Sheets backend initialized successfully")
            except Exception as e:
                logger.warning(f"Google Sheets backend initialization failed: {e}")
                self.backend = None
                self.backend_initialized = True
        return self.backend
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_url = urlparse(self.path)
        
        if parsed_url.path == '/':
            self.handle_root()
        elif parsed_url.path == '/status':
            self.handle_status()
        elif parsed_url.path == '/spreadsheet-info':
            self.handle_spreadsheet_info()
        elif parsed_url.path == '/get-all-clients':
            self.handle_get_all_clients()
        elif parsed_url.path.endswith(('.html', '.css', '.js', '.jpg', '.jpeg', '.png', '.svg')):
            self.handle_static_file(parsed_url.path)
        else:
            self.send_error(404, "Endpoint not found")
    
    def do_POST(self):
        """Handle POST requests"""
        parsed_url = urlparse(self.path)
        
        if parsed_url.path == '/store-calculation':
            self.handle_store_calculation()
        elif parsed_url.path == '/find-similar-clients':
            self.handle_find_similar_clients()
        else:
            self.send_error(404, "Endpoint not found")
    
    def handle_root(self):
        """Handle root path - redirect to demo page"""
        self.send_response(302)
        self.send_header('Location', '/demo.html')
        self.end_headers()
    
    def handle_static_file(self, file_path):
        """Handle static file requests (HTML, CSS, JS)"""
        try:
            # Remove leading slash
            if file_path.startswith('/'):
                file_path = file_path[1:]
            
            # Security check - only serve files in current directory
            if '..' in file_path or file_path.startswith('/'):
                self.send_error(403, "Access denied")
                return
            
            # Check if file exists
            if not os.path.exists(file_path):
                self.send_error(404, f"File not found: {file_path}")
                return
            
            # Determine content type
            content_type = 'text/plain'
            if file_path.endswith('.html'):
                content_type = 'text/html'
            elif file_path.endswith('.css'):
                content_type = 'text/css'
            elif file_path.endswith('.js'):
                content_type = 'application/javascript'
            elif file_path.endswith('.svg'):
                content_type = 'image/svg+xml'
            elif file_path.endswith(('.jpg', '.jpeg')):
                content_type = 'image/jpeg'
            
            # Read and serve file
            with open(file_path, 'rb') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-type', content_type)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(content)
            
        except Exception as e:
            logger.error(f"Error serving static file {file_path}: {e}")
            self.send_error(500, f"Internal server error: {str(e)}")
    
    def handle_status(self):
        """Handle status check request"""
        try:
            backend = self.get_backend()
            if backend:
                status = backend.get_configuration_status()
            else:
                status = {
                    'is_configured': False,
                    'has_service_account': False,
                    'has_private_key': False,
                    'has_spreadsheet_id': False,
                    'spreadsheet_id': None,
                    'worksheet_name': None,
                    'connection_status': 'Not Connected'
                }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                'success': True,
                'status': status,
                'timestamp': datetime.now().isoformat()
            }
            
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            logger.error(f"Error handling status request: {e}")
            self.send_error(500, f"Internal server error: {str(e)}")
    
    def handle_spreadsheet_info(self):
        """Handle spreadsheet info request"""
        try:
            backend = self.get_backend()
            if backend:
                info = backend.get_spreadsheet_info()
            else:
                info = {'error': 'Google Sheets not available'}
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                'success': True,
                'info': info,
                'timestamp': datetime.now().isoformat()
            }
            
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            logger.error(f"Error handling spreadsheet info request: {e}")
            self.send_error(500, f"Internal server error: {str(e)}")
    
    def handle_get_all_clients(self):
        """Handle request to get all clients with ACS data"""
        try:
            # Initialize client finder if not already done
            if not hasattr(self, 'client_finder') or self.client_finder is None:
                try:
                    from client_reference_finder import ClientReferenceFinder
                    self.client_finder = ClientReferenceFinder(job_data_file="2025-08-29 3_39pm.csv")
                    logger.info("Client Reference Finder initialized successfully")
                except Exception as e:
                    logger.error(f"Error initializing Client Reference Finder: {e}")
                    self.send_error(500, "Failed to initialize client finder")
                    return
            
            # Get all clients from the ACS data (not just from combined data)
            if self.client_finder.acs_data is not None and not self.client_finder.acs_data.empty:
                clients_data = []
                
                # Get all clients directly from ACS data DataFrame
                for _, row in self.client_finder.acs_data.iterrows():
                    clients_data.append({
                        'client_name': row['CLIENT_NAME'],
                        'acs_score': int(row['ACS_SCORE']),
                        'complexity_level': self.get_complexity_level(int(row['ACS_SCORE']))
                    })
                
                # Sort by client name
                clients_data.sort(key=lambda x: x['client_name'])
                
                logger.info(f"Retrieved {len(clients_data)} client records")
                
                # Send response
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                response = {
                    'success': True,
                    'clients': clients_data,
                    'total_count': len(clients_data),
                    'timestamp': datetime.now().isoformat()
                }
                
                self.wfile.write(json.dumps(response, indent=2).encode('utf-8'))
                
            else:
                self.send_error(500, "No client data available")
                
        except Exception as e:
            logger.error(f"Error handling get all clients request: {e}")
            self.send_error(500, f"Internal server error: {str(e)}")
    
    def get_complexity_level(self, score):
        """Get complexity level description for ACS score"""
        levels = {
            1: 'Very Simple',
            2: 'Simple', 
            3: 'Moderate',
            4: 'Complex',
            5: 'Very Complex'
        }
        return levels.get(score, 'Unknown')
    
    def handle_store_calculation(self):
        """Handle ACS calculation storage request"""
        try:
            # Get content length
            content_length = int(self.headers.get('Content-Length', 0))
            
            if content_length == 0:
                self.send_error(400, "No data provided")
                return
            
            # Read request body
            post_data = self.rfile.read(content_length)
            acs_data = json.loads(post_data.decode('utf-8'))
            
            logger.info(f"Received ACS calculation data: {acs_data}")
            
            # Store in Google Sheets
            backend = self.get_backend()
            if backend:
                result = backend.store_acs_calculation(acs_data)
            else:
                result = {'error': 'Google Sheets not available', 'row_number': None}
            
            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                'success': result.get('success', False),
                'message': result.get('message', 'Unknown error'),
                'row_number': result.get('row_number'),
                'timestamp': datetime.now().isoformat()
            }
            
            self.wfile.write(json.dumps(response).encode())
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in request: {e}")
            self.send_error(400, "Invalid JSON data")
        except Exception as e:
            logger.error(f"Error handling store calculation request: {e}")
            self.send_error(500, f"Internal server error: {str(e)}")
    
    def handle_find_similar_clients(self):
        """Handle requests to find similar clients."""
        try:
            # Get request body
            content_length = int(self.headers.get('Content-Length', 0))
            
            if content_length == 0:
                self.send_error(400, "No data provided")
                return
            
            # Read request body
            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode('utf-8'))
            
            # Extract parameters
            target_acs = request_data.get('target_acs')
            target_category = request_data.get('target_category')
            target_country = request_data.get('target_country')
            max_results = request_data.get('max_results', 10)
            
            if not target_acs or not target_category:
                self.send_error(400, "Missing required parameters: target_acs and target_category")
                return
            
            logger.info(f"Finding similar clients: ACS={target_acs}, Category={target_category}, Country={target_country}")
            
            # Initialize client finder if not already done
            if not hasattr(self, 'client_finder') or self.client_finder is None:
                try:
                    from client_reference_finder import ClientReferenceFinder
                    self.client_finder = ClientReferenceFinder(job_data_file="2025-08-29 3_39pm.csv")
                    logger.info("Client Reference Finder initialized successfully")
                except Exception as e:
                    logger.error(f"Error initializing Client Reference Finder: {e}")
                    self.send_error(500, "Failed to initialize client finder")
                    return
            
            # Find similar clients
            similar_clients = self.client_finder.find_similar_clients(
                target_acs=target_acs,
                target_category=target_category,
                target_country=target_country,
                max_results=max_results
            )
            
            logger.info(f"Found {len(similar_clients)} similar clients")
            
            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            response_data = {
                'success': True,
                'clients': similar_clients,
                'total_found': len(similar_clients),
                'search_params': {
                    'target_acs': target_acs,
                    'target_category': target_category,
                    'max_results': max_results
                }
            }
            
            self.wfile.write(json.dumps(response_data, indent=2).encode('utf-8'))
            
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON in request body")
        except Exception as e:
            logger.error(f"Error in handle_find_similar_clients: {e}")
            self.send_error(500, f"Internal server error: {str(e)}")
    
    def log_message(self, format, *args):
        """Custom logging for requests"""
        logger.info(f"{self.address_string()} - {format % args}")

def run_server(port=None):
    """Run the ACS Calculator server"""
    if port is None:
        port = int(os.getenv('PORT', 8000))
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, ACSCalculatorHandler)
    
    print(f"🚀 ACS Calculator Server starting on port {port}")
    print(f"📊 Frontend: http://localhost:{port}/acs_calculator.html")
    print(f"🔧 Backend API: http://localhost:{port}/")
    print(f"📋 Status: http://localhost:{port}/status")
    print(f"📈 Spreadsheet Info: http://localhost:{port}/spreadsheet-info")
    print(f"💾 Store Calculation: POST http://localhost:{port}/store-calculation")
    print(f"🔍 Find Similar Clients: POST http://localhost:{port}/find-similar-clients")
    print("\nPress Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        httpd.server_close()

if __name__ == "__main__":
    run_server()
