#!/usr/bin/env python3
"""
Health check script for ACS Calculator production deployment
"""
import requests
import sys
import os

def check_health():
    """Check if all routes are working in production"""
    base_url = "https://buildingfeed.coder.prod.joveo.com"
    
    routes = [
        "/",
        "/acs_calculator.html",
        "/acs_calculator.css", 
        "/acs_calculator.js",
        "/status",
        "/spreadsheet-info",
        "/get-all-clients",
        "/joveo_logo.jpg"
    ]
    
    print("🔍 Checking ACS Calculator Production Health...")
    print(f"🌐 Base URL: {base_url}")
    print("-" * 50)
    
    all_healthy = True
    
    for route in routes:
        try:
            url = f"{base_url}{route}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ {route} - OK ({response.status_code})")
            else:
                print(f"❌ {route} - FAILED ({response.status_code})")
                all_healthy = False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ {route} - ERROR: {str(e)}")
            all_healthy = False
    
    print("-" * 50)
    
    if all_healthy:
        print("🎉 All routes are working correctly!")
        return True
    else:
        print("⚠️  Some routes are not working. Check the errors above.")
        return False

if __name__ == "__main__":
    success = check_health()
    sys.exit(0 if success else 1)
