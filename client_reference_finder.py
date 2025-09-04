#!/usr/bin/env python3
"""
Phase 3: Client Reference Finder
Combines ACS scores with job data to help teams find similar clients for reference.
"""

import pandas as pd
import json
from typing import Dict, List, Tuple, Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ClientReferenceFinder:
    """
    Finds similar clients based on ACS scores and job categories for reference purposes.
    """
    
    def __init__(self, job_data_file: str = None):
        """Initialize the Client Reference Finder."""
        self.acs_data = None
        self.job_data = None
        self.country_data = None
        self.combined_data = None
        
        # Load ACS data (hardcoded for now)
        self.load_acs_data(None)
        
        # Load job data if file provided
        if job_data_file:
            self.load_job_data(job_data_file)
        
        # TODO: Load country data when needed
        # self.load_country_data(country_data_file)
        
        # Combine data if both ACS and job data are available
        if self.acs_data is not None and self.job_data is not None:
            self.combine_data()
    
    def load_acs_data(self, file_path: str) -> None:
        """Load ACS scores data."""
        try:
            # For now, we'll use the manual data you provided
            acs_data = {
                'LHH': 1, 'Adecco Personaldienstleistungen GmbH': 1, 'Adecco - Switzerland - Opti': 1,
                'Just Eat Takeaway - Corporate': 1, 'Scale AI': 1, 'Just Eat Takeaway - Courier': 1,
                'CareRite': 1, 'Roadie': 1, 'Centers Healthcare - Exchange': 1, 'Hoops HR - Exchange': 1,
                'DIS AG-Exchange': 1, 'Adecco World Wide Web DE': 1, 'DIS AG Central Campaigns Exchange': 1,
                'Adecco Personaldienstleistungen GmbH-Exchange': 1, 'Spring Health': 1, 'Adecco Germany Logistics Exchange': 1,
                'Angi Services': 1, 'Touchmark': 1, 'Piening GmbH Bielefeld - Exchange': 1, 'New Story Schools': 1,
                'WorkWhile- Exchange': 1, 'Pontoon - Switzerland': 1, 'Moments Hospice': 1, 'MJHS': 1,
                'MB HC - Exchange': 1, 'TRN Staffing': 1, 'Omnicom Media GmbH': 1, 'TAG - Adecco - USA': 1,
                'Five Guys': 1, 'MVT': 1, 'Recruitics - DE': 1, 'Smile Brands': 1, 'Proserv DE Exchange': 1,
                'Modis GmbH-Exchange': 1, 'Banner Bank': 1, 'Champions Group': 1, 'Riverside Transport': 1,
                'Piening GmbH Berlin - Exchange': 1, 'The UVM Health Network': 1, 'PetVet': 1, 'Adecco Central Campaigns Exchange': 1,
                'Idaho Milk': 1, 'Randstad DE': 1, 'Groendyke Transport': 1, 'Randall Reilly': 1, 'LHH Exchange': 1,
                'Affinix': 1, 'RSR - Frontier Exchange': 1, 'GetScale': 1, 'MetroPlus': 1, 'Knight Transportation': 1,
                'Visage': 1, 'RSR- Lonza SGD Exchange': 1, 'Quest Defense Systems & Solutions': 1, 'Chief': 1,
                'Cavco': 1, 'AICA Orthopedics': 1, 'Uber AI Solutions': 1, 'TAG - Adecco - Euro': 1, 'Totalmed Exchange': 1,
                'WorkerHero - Exchange': 1, 'Rakesh Test': 1, 'Avata Partners - Exchange': 1, 'K&B Transportation': 1,
                'Volvo Exchange': 1, 'Adecco Belgium Exchange': 1, 'TAG - The Adecco Group - Euro': 1,
                
                'Ashley Furniture': 2, 'Epic Healthcare': 2, 'New Story': 2, 'Lonza': 2, 'LHH - Switzerland - Opti': 2,
                'Korn_Ferry-Honeywell': 2, 'FLINT': 2, 'KAG': 2, 'inCare': 2, 'CWB': 2, 'Albertsons': 2,
                'Infinite Healthcare - Exchange': 2, 'Motion Recruitment': 2, 'Lululemon': 2, 'G&D Integrated': 2,
                'W.W.Williams': 2, 'Lionstep AG': 2, 'Penna Tesco': 2, 'Third Bridge': 2, 'CEDA': 2, 'Domino\'s': 2,
                'Camden Council': 2, 'TAG - LHH - USA': 2, 'Adecco Canada - Exchange': 2, 'KornFerry_Honeywell_Exchange': 2,
                'CoreCivic': 2,
                
                'CH Regionalmedien AG': 3, 'DWA - Northrop Grumman': 3, 'BrandSafway Exchange': 3,
                
                'Crash Champions': 4, 'Heartland Dental': 4, 'Amrize': 4, 'Yale New Haven Health': 4, 'Aviva': 4,
                'Charter': 4, 'Houston Methodist': 4, 'Gemeente': 4, 'ASPCA': 4, 'SKILLIT': 4, 'Publicis Sapient- Exchange': 4,
                'Enhance Therapies': 4, 'Lonza - NAM': 4, 'Mundipharma': 4, 'Parkland': 4, 'STG Logistics': 4,
                'Western Financial': 4, 'Helena Agri': 4, 'Sabic': 4, 'Johns Hopkins Health System': 4, 'Wuxi AppTec': 4,
                'Liberty Global': 4, 'Bausch and Lomb': 4, 'Red Bear Care Wellness': 4, 'KCB': 4, 'CAE': 4, 'XPO': 4,
                'Barclays - Exchange': 4, 'Publicis Sapient - Exchange': 4, 'Marten Transport': 4, 'Dana Farber': 4,
                'Kuehne+Nagel': 4, 'Gloucestershire County Council PennaPublic Exchange': 4, 'Amrize BE': 4,
                'Gloucestershire County Council': 4, 'Ericsson-Exchange': 4, 'TAG - Modis - USA': 4,
                'Cafcass- UK Penna Public Exchange': 4, 'University of Calgary': 4,
                
                'Wells Fargo': 5, 'Yacht': 5, 'ScionHealth': 5, 'Kenan Advantage Group': 5, 'Mars': 5,
                'Flexential - Exchange': 5, 'Johnson and Johnson- EU': 5, 'Methodist Le Bonheur': 5, 'Jackson Healthcare': 5,
                'Carrier': 5, 'Phoebe Putney Health System': 5, 'David Lloyd': 5, 'Nordstrom': 5, 'Werner': 5,
                'Jazz Pharmaceuticals': 5, 'Cambridge Health Alliance': 5, 'Tempur-Sealy': 5, 'ING Netherlands Euro exchange': 5,
                'TalentNext': 5, 'Novae': 5, 'Jefferson Health': 5, 'Clayton Homes': 5, 'Carrier One': 5,
                'Bristol Myers Squibb': 5, 'Bristol Myers Squibb - UK': 5,
                
                # Additional clients from your data
                'Uber': 2, 'Uber Eats': 2, 'Uber exchange': 2, 'Centers Healthcare': 1, 'Adecco': 1,
                'Uber eats exchange': 2, 'DIS AG': 1, 'Yellowshark': 2, 'Just Eats Takeaway - Scoober - Courier': 1,
                'DIS AG Central Campaigns': 1, 'Sky': 4, 'MADSACK Market Solutions': 1, 'Hoops HR': 1,
                'Adecco Amazon': 5, 'MB HC': 1, 'Infinite Healthcare': 2, 'Adecco Germany Logistics': 1,
                'Honeywell': 2, 'Adecco - France': 1, 'Publicis Sapient': 4, 'Aveanna Healthcare': 1,
                'Piening GmbH Bielefeld': 1, 'MHA': None, 'WorkWhile': 1, 'Flexential': 5, 'Aveanna Healthcare - Exchange': 1,
                'Shiftsmart': None, 'Little Wheel': 5, 'Otsuka Pharmaceutical': 5, 'Modis GmbH': 1,
                'Carpenter Technology': 5, 'Proserv DE': 1, 'inCare by Piening': 1, 'Brown Trucking': None,
                'OMPros': None, 'ING Netherlands': 5, 'Tesco': 2, 'Wahve': 1, 'Barclays': 4, 'Frontier': 1,
                'Air Canada': None, 'Amazon - HGV Drivers UK': None, 'Piening GmbH Berlin': 1, 'Acelero': 5,
                'Keller Williams': None, 'STG Logistics': None, 'Marvecs GmbH': 1, 'Adecco Central Campaigns': 1,
                'LE Growth': None, 'MI5': None, 'Ohio Living': 5, 'Westlake Ace Hardware': 5, 'LHH Recruitment Solutions': 1,
                'HMGCC': None, 'Tal.AI': None, 'Pentec Health': None, 'Lionstep AG 1': 2, 'Jobcloud DVinci': None,
                'Parachute': None, 'P2D': None, 'MI6': None, 'GCHQ': None, 'Fidelity RPO': None, 'UPT': None,
                'Goodyear': 4, 'Yellowshark CHF': 2, 'Galderma': 5, 'Family First': None, 'Lonza - APAC': 4,
                'Care UK': None, 'Fort Transfer': None, 'GECAD GmbH': None, 'Jobcloud DVinci - Exchange': None,
                'Stegra': None, 'Penna  - MI5 - Exchange': None, 'Eshyft': None, 'Wells Fargo RSR': None,
                'Youngs Pub': None, 'NAS_Quest': None, 'Penn Tank Lines': None, 'HMGCC - Penna': None,
                'Costa Coffee': None, 'Roehl Transport': None, 'Western Express': None, 'Proximus': None,
                'North Los Angeles County Regional Center': None, 'PR Management': None, 'MI6 - Penna': None,
                'Nurtured Talent': None, 'LifePoint Health': None, 'Fidelity': None, 'Akkodis CA': None,
                'Lennox': None, 'GCHQ - Penna': None, 'Homewood Retirement Centers': None, 'GreatWater': None,
                'J.B. Hunt': None, 'PGT': None, 'Marketplace': None, 'CareerBuilder - Staffing': None,
                'XBL': None, 'BrandSafway': None, 'Westrafo': None, 'CareerBuilder - Staffing - Exchange': None,
                'TWT Refrigerated Services': None, 'Revv Staffing': None, 'Nebraska Atlantic': None,
                'KAG Corp - Indeed': None, 'U.S. Xpress': None, 'Akkodis': None, 'St George\'s University': None,
                'Teesside University': None, 'Mars - APAC': None, 'Ofsted': None, 'National Carriers': None,
                'Rotherham MBC': None, 'Olam Agri': None, 'Oakley': None, 'K B Transportation': None,
                'London Borough of Waltham Forest': None, 'Adecco Amazon France': None, 'AICA Orthopedics': None,
                'Adeccogroup': None, 'Sig Sauer': None, 'Vale Food Co.': None, 'University of Cambridge': None,
                'Gulf Winds': None, 'James J. Williams Transport': None, 'Keller Williams- Exchange': None,
                'Genesis Healthcare': None, 'NFI': None, 'UPS - PA': None, 'UPS - OH': None, 'Adecco Canada': None,
                'The Adecco Group – Germany': None, 'Holiday Inn Express': None, 'Teesside University PennaPublic Exchange': None,
                'Angular Table PROD sanity': None, 'Mesilla Valley Transportation': None, 'Coverall': None,
                'RSR- Mars India Exchange': None, 'Philips': None, 'RG Transport': None, 'Pontoon': None,
                'Just Eats Takeaway - Delco - Courier': None, 'Careernow- Test Client': None, 'HoopsTest': None,
                'S-NB-PROD sanity(no net Budget)': None, 'Volvo': None, 'The Office for Students': None,
                'The Office for Students - Penna Public Exchange': None, 'Gale Healthcare': None, 'Ericsson': None,
                'Menulog - Australia': None, 'Totalmed': None, 'Piening Montage': None, 'R.E. Garrison': None,
                'Puls': None, 'Avata Partners': None, 'Joveo Individual': None, 'softgarden e-recruiting GmbH': None,
                'IT Projects': None, 'Test': None, 'Renesas': None, 'LHH.FR': None, 'Lifespan': None,
                'Five Guys- Exchange': None, 'SitePro Solutions': None, 'Infosys - FOP': None, 'Promotionbasis': None,
                'Adecco Staffing-Belgium': None, 'Attend home care': None, 'RPO': None, 'PennaPublic_University Of Essex': None,
                'feed 1': None, 'SitePro Solutions - Exchange': None, 'DIS AG Industry': None, 'Workerhero': None,
                'HealthTrust Workforce Solutions': None, 'Lakeside Book Company': None, 'Testing Triam': None,
                'iparkMedia - Euro': None, 'Lehigh Valley Health Network': None, 'TAG DRH': None, 'Uber - Supply': None,
                'MODISTECH.FR': None, 'ADECCOMEDICAL.FR': None, 'WICO GmbH': None, 'Cafcass- UK': None,
                'Adecco Brand- UK': None, 'Allaire Health Services': None, 'University of Essex': None,
                'Modis- Switzerland': None, 'TAG - LHH - Euro': None, 'Covelo Group': None, 'Gifted Healthcare': None
            }
            
            # Create DataFrame and filter out None values
            acs_list = []
            for client, score in acs_data.items():
                if score is not None:
                    acs_list.append({'CLIENT_NAME': client, 'ACS_SCORE': score})
            
            self.acs_data = pd.DataFrame(acs_list)
            
            logger.info(f"Loaded ACS data for {len(self.acs_data)} clients")
            
        except Exception as e:
            logger.error(f"Error loading ACS data: {e}")
            # Create minimal ACS data to prevent failure
            self.acs_data = pd.DataFrame([
                {'CLIENT_NAME': 'Test Client', 'ACS_SCORE': 1}
            ])
            logger.warning("Created minimal ACS data to prevent failure")
    
    def load_job_data(self, file_path: str) -> None:
        """Load job data from CSV."""
        try:
            # Read the CSV file
            self.job_data = pd.read_csv(file_path)
            
            # Clean column names
            self.job_data.columns = [col.strip() for col in self.job_data.columns]
            
            # Clean the data
            self.job_data = self.job_data.dropna(subset=['CLIENT_NAME', 'DETAIL_NORMALISED_CATEGORY'])
            self.job_data = self.job_data[self.job_data['DETAIL_NORMALISED_CATEGORY'] != '']
            
            logger.info(f"Loaded job data: {len(self.job_data)} job postings across {self.job_data['CLIENT_NAME'].nunique()} clients")
            
        except Exception as e:
            logger.error(f"Error loading job data: {e}")
            self.job_data = None

    def load_country_data(self, file_path: str) -> None:
        """Load country data from CSV."""
        try:
            # Read the CSV file
            self.country_data = pd.read_csv(file_path)
            
            # Clean column names
            self.country_data.columns = [col.strip() for col in self.country_data.columns]
            
            # Clean the data - replace empty/null values with "United States" as per user instruction
            self.country_data['NORMALISED_COUNTRY'] = self.country_data['NORMALISED_COUNTRY'].fillna('United States')
            self.country_data = self.country_data[self.country_data['NORMALISED_COUNTRY'] != '']
            
            logger.info(f"Loaded country data: {len(self.country_data)} client-country mappings")
            
        except Exception as e:
            logger.error(f"Error loading country data: {e}")
            self.country_data = None
    
    def combine_data(self) -> None:
        """Combine ACS and job data for analysis."""
        try:
            logger.info(f"Starting data combination...")
            logger.info(f"ACS data: {self.acs_data is not None}, shape: {self.acs_data.shape if self.acs_data is not None else 'None'}")
            logger.info(f"Job data: {self.job_data is not None}, shape: {self.job_data.shape if self.job_data is not None else 'None'}")
            logger.info(f"Country data: {self.country_data is not None}, shape: {self.country_data.shape if self.country_data is not None else 'None'}")
            
            if self.acs_data is None or self.job_data is None:
                logger.error("Cannot combine data: ACS or job data not loaded")
                return
            
            # Merge the datasets
            logger.info("Merging datasets...")
            self.combined_data = self.job_data.merge(
                self.acs_data, 
                on='CLIENT_NAME', 
                how='left'
            )
            logger.info(f"Merge completed: {len(self.combined_data)} rows")
            
            # TODO: Add country data when needed
            # if self.country_data is not None:
            #     logger.info("Adding country data...")
            #     self.combined_data = self.combined_data.merge(
            #         self.country_data,
            #         on='CLIENT_NAME',
            #         how='left'
            #     )
            #     # Fill missing countries with "United States"
            #     self.combined_data['NORMALISED_COUNTRY'] = self.combined_data['NORMALISED_COUNTRY'].fillna('United States')
            #     logger.info(f"Country data added: {len(self.combined_data)} rows")
            
            # Remove rows without ACS scores
            logger.info("Removing rows without ACS scores...")
            initial_count = len(self.combined_data)
            self.combined_data = self.combined_data.dropna(subset=['ACS_SCORE'])
            final_count = len(self.combined_data)
            logger.info(f"Rows with ACS scores: {final_count} (removed {initial_count - final_count})")
            
            logger.info(f"Combined data: {len(self.combined_data)} job postings with ACS scores")
            
        except Exception as e:
            logger.error(f"Error combining data: {e}")
            self.combined_data = None
    
    def find_similar_clients(self, target_acs: int, target_category: str, target_country: str = None, max_results: int = 10) -> List[Dict]:
        """
        Find clients with similar ACS scores and job categories.
        
        Args:
            target_acs: The ACS score to match
            target_category: The job category to match
            target_country: Optional country filter
            max_results: Maximum number of results to return
            
        Returns:
            List of client dictionaries with matching criteria
        """
        if self.combined_data is None:
            logger.error("No combined data available")
            return []
        
        try:
            # Filter by job category first (as per your requirement)
            category_filtered = self.combined_data[
                self.combined_data['DETAIL_NORMALISED_CATEGORY'] == target_category
            ]
            
            if len(category_filtered) == 0:
                logger.warning(f"No clients found with job category: {target_category}")
                return []
            
            # Filter by ACS score within the category-filtered data
            acs_filtered = category_filtered[
                category_filtered['ACS_SCORE'] == target_acs
            ]
            
            if len(acs_filtered) == 0:
                logger.warning(f"No clients found with ACS {target_acs} for category: {target_category}")
                return []
            
            # TODO: Add country filtering here once country data is provided
            # if target_country:
            #     acs_filtered = acs_filtered[
            #         acs_filtered['COUNTRY'] == target_country
            #     ]
            
            # TODO: Add country filtering here once country data is provided
            # if target_country:
            #     acs_filtered = acs_filtered[
            #         acs_filtered['COUNTRY'] == target_country
            #     ]
            
            logger.info(f"Found {len(acs_filtered)} clients with {target_category} jobs and ACS {target_acs}")
            
            # Group by client and aggregate data
            client_groups = acs_filtered.groupby('CLIENT_NAME').agg({
                'ACS_SCORE': 'first',
                'JOB_TITLE': lambda x: list(x.unique())[:5],  # Sample job titles
                'DETAIL_NORMALISED_CATEGORY': 'count'  # Job count
            }).reset_index()
            
            # Rename columns
            client_groups.columns = ['client_name', 'acs_score', 'sample_job_titles', 'job_count']
            
            # Sort by job count (more jobs = better reference)
            client_groups = client_groups.sort_values('job_count', ascending=False)
            
            # Limit results
            client_groups = client_groups.head(max_results)
            
            # Convert to list of dictionaries
            results = []
            for _, row in client_groups.iterrows():
                results.append({
                    'client_name': row['client_name'],
                    'acs_score': int(row['acs_score']),
                    'job_count': int(row['job_count']),
                    'sample_job_titles': row['sample_job_titles'],
                    'matching_category': target_category
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Error finding similar clients: {e}")
            return []
    
    def _calculate_similarity_score(self, client_row: pd.Series, target_acs: int, target_category: str = None) -> float:
        """Calculate a similarity score for ranking results."""
        score = 0.0
        
        # ACS score match (perfect = 100 points)
        if client_row['ACS_SCORE'] == target_acs:
            score += 100
        
        # Job count bonus (more jobs = better reference)
        score += min(client_row['JOB_COUNT'] * 0.1, 20)  # Max 20 points for job count
        
        # Category match bonus if specified
        if target_category:
            score += 10
        
        return round(score, 1)
    
    def get_job_categories(self) -> List[str]:
        """Get list of available job categories."""
        if self.job_data is None:
            return []
        
        return sorted(self.job_data['DETAIL_NORMALISED_CATEGORY'].unique().tolist())
    
    def get_client_summary(self, client_name: str) -> Dict:
        """Get comprehensive summary for a specific client."""
        if self.combined_data is None:
            return {}
        
        try:
            client_data = self.combined_data[self.combined_data['CLIENT_NAME'] == client_name]
            
            if len(client_data) == 0:
                return {}
            
            # Get ACS score
            acs_score = client_data.iloc[0]['ACS_SCORE']
            
            # Get job categories and counts
            category_counts = client_data['DETAIL_NORMALISED_CATEGORY'].value_counts()
            
            # Get sample job titles
            sample_jobs = client_data['JOB_TITLE'].unique()[:10]
            
            return {
                'client_name': client_name,
                'acs_score': int(acs_score),
                'total_jobs': len(client_data),
                'job_categories': category_counts.to_dict(),
                'sample_job_titles': sample_jobs.tolist(),
                'acs_complexity': self._get_acs_complexity_description(acs_score)
            }
            
        except Exception as e:
            logger.error(f"Error getting client summary: {e}")
            return {}
    
    def _get_acs_complexity_description(self, acs_score: int) -> str:
        """Get human-readable description of ACS complexity."""
        descriptions = {
            1: "Very Low Complexity - Simple, standardized processes",
            2: "Low Complexity - Basic workflows with some variation",
            3: "Medium Complexity - Moderate process complexity",
            4: "High Complexity - Complex, multi-step processes",
            5: "Very High Complexity - Highly specialized, complex workflows"
        }
        return descriptions.get(acs_score, "Unknown Complexity")
    
    def search_clients(self, query: str, max_results: int = 20) -> List[Dict]:
        """Search for clients by name."""
        if self.acs_data is None:
            return []
        
        try:
            # Search in client names
            matching_clients = self.acs_data[
                self.acs_data['CLIENT_NAME'].str.contains(query, case=False, na=False)
            ]
            
            # Limit results
            matching_clients = matching_clients.head(max_results)
            
            # Convert to list of dictionaries
            results = []
            for _, row in matching_clients.iterrows():
                results.append({
                    'client_name': row['CLIENT_NAME'],
                    'acs_score': int(row['ACS_SCORE'])
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Error searching clients: {e}")
            return []

def main():
    """Demo the Client Reference Finder."""
    print("🚀 Phase 3: Client Reference Finder")
    print("=" * 50)
    
    # Initialize the finder
    finder = ClientReferenceFinder(job_data_file="2025-08-29 3_39pm.csv")
    
    if finder.combined_data is None:
        print("❌ Failed to load data")
        return
    
    print(f"✅ Data loaded successfully!")
    print(f"📊 {len(finder.combined_data)} job postings with ACS scores")
    print(f"🏢 {finder.combined_data['CLIENT_NAME'].nunique()} unique clients")
    print(f"💼 {len(finder.get_job_categories())} job categories")
    print()
    
    # Demo: Find similar clients for Wells Fargo (ACS 5)
    print("🔍 Example: Finding similar clients to Wells Fargo (ACS 5)")
    print("-" * 50)
    
    similar_clients = finder.find_similar_clients(target_acs=5, max_results=5)
    
    for i, client in enumerate(similar_clients, 1):
        print(f"{i}. {client['client_name']} (ACS {client['acs_score']})")
        print(f"   📈 {client['job_count']} jobs | Similarity: {client['similarity_score']}")
        print(f"   💼 Sample: {', '.join(client['sample_job_titles'][:3])}")
        print()
    
    # Demo: Get client summary
    print("📋 Example: Client Summary for Wells Fargo")
    print("-" * 50)
    
    wells_fargo_summary = finder.get_client_summary("Wells Fargo")
    if wells_fargo_summary:
        print(f"🏢 {wells_fargo_summary['client_name']}")
        print(f"📊 ACS Score: {wells_fargo_summary['acs_score']} - {wells_fargo_summary['acs_complexity']}")
        print(f"📈 Total Jobs: {wells_fargo_summary['total_jobs']}")
        print(f"🎯 Top Job Categories:")
        for category, count in list(wells_fargo_summary['job_categories'].items())[:5]:
            print(f"   • {category}: {count} jobs")
        print()
    
    # Demo: Search functionality
    print("🔍 Example: Search for clients containing 'Adecco'")
    print("-" * 50)
    
    search_results = finder.search_clients("Adecco", max_results=5)
    for client in search_results:
        print(f"• {client['client_name']} (ACS {client['acs_score']})")
    
    print()
    print("🎉 Phase 3 Complete! Ready for integration into ACS Calculator.")

if __name__ == "__main__":
    main()
