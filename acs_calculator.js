// ACS Calculator JavaScript
class ACSCalculator {
    constructor() {
        this.initializeEventListeners();
        this.setupProfileDropdown();
        this.backendUrl = ''; // Use root path for local server
        this.initializeBackendConnection();
        this.forceDropdownStyling();
    }

    initializeEventListeners() {
        const form = document.getElementById('acsForm');
        if (form) {
            form.addEventListener('submit', (e) => this.handleFormSubmit(e));
        }

        // Real-time calculation as user fills form
        const formInputs = document.querySelectorAll('#acsForm select, #acsForm input');
        formInputs.forEach(input => {
            input.addEventListener('change', () => this.updateRealTimeCalculation());
        });
    }

    setupProfileDropdown() {
        // Profile section removed
    }

    forceDropdownStyling() {
        // Force styling on all select elements and their options
        const selects = document.querySelectorAll('select');
        selects.forEach(select => {
            // Style the select element itself
            select.style.backgroundColor = 'white';
            select.style.color = '#000000';
            
            // Style all options
            const options = select.querySelectorAll('option');
            options.forEach(option => {
                option.style.backgroundColor = 'white';
                option.style.color = '#000000';
                option.style.fontWeight = '500';
            });
        });
    }

    async initializeBackendConnection() {
        try {
            // Check backend status
            const response = await fetch(`/status`);
            const data = await response.json();
            
            if (data.success && data.status.is_configured) {
                this.showNotification('✅ Connected to Google Sheets backend', 'success');
                console.log('Backend status:', data.status);
            } else {
                this.showNotification('⚠️ Backend not fully configured', 'warning');
            }
            
            // Load job categories
            await this.loadJobCategories();
        } catch (error) {
            console.warn('Backend connection failed:', error);
            this.showNotification('❌ Backend connection failed', 'error');
        }
    }

    async loadJobCategories() {
        try {
            // Load categories from the text file we created
            const response = await fetch('/job_categories.txt');
            if (response.ok) {
                const categoriesText = await response.text();
                const categories = categoriesText.trim().split('\n').filter(cat => cat.trim());
                
                // Populate the dropdown
                const jobCategorySelect = document.getElementById('jobCategorySelect');
                if (jobCategorySelect) {
                    // Clear existing options except the first one
                    jobCategorySelect.innerHTML = '<option value="">-- Select a category --</option>';
                    
                    // Add all categories
                    categories.forEach(category => {
                        const option = document.createElement('option');
                        option.value = category;
                        option.textContent = category;
                        jobCategorySelect.appendChild(option);
                    });
                    
                    console.log(`Loaded ${categories.length} job categories`);
                }
            } else {
                console.error('Failed to load job categories');
            }
        } catch (error) {
            console.error('Error loading job categories:', error);
        }
    }

    handleFormSubmit(e) {
        e.preventDefault();
        console.log('Form submitted!');
        
        const formData = new FormData(e.target);
        const data = Object.fromEntries(formData.entries());
        console.log('Form data:', data);
        
        // Validate required fields
        if (!this.validateForm(data)) {
            console.log('Form validation failed');
            return;
        }

        console.log('Form validation passed, calculating ACS...');
        
        // Calculate ACS
        const acsResult = this.calculateACS(data);
        console.log('ACS calculation result:', acsResult);
        
        // Display results
        console.log('Calling displayResults...');
        this.displayResults(acsResult, data);
        
        // Store data
        console.log('Calling storeData...');
        this.storeData(data, acsResult);
    }

    validateForm(data) {
        const requiredFields = ['clientName', 'pages', 'timeToFill', 'documents', 'loginRequired'];
        const missingFields = requiredFields.filter(field => !data[field]);
        
        if (missingFields.length > 0) {
            alert('Please fill in all required fields marked with *');
            return false;
        }
        
        return true;
    }

    calculateACS(data) {
        // Get factor scores based on your documentation
        const pageScore = this.getPageScore(data.pages);
        const timeScore = this.getTimeScore(data.timeToFill);
        const documentScore = this.getDocumentScore(data.documents);
        const loginMultiplier = data.loginRequired === 'true' ? 1.2 : 1.0;

        // Calculate raw score using your formula
        const rawScore = (pageScore * 0.2) + (timeScore * 0.6) + (documentScore * 0.2);
        
        // Apply login multiplier
        const adjustedScore = rawScore * loginMultiplier;
        
        // Determine final ACS (1-5) based on thresholds
        const finalACS = this.getFinalACS(adjustedScore);
        
        return {
            pageScore,
            timeScore,
            documentScore,
            loginMultiplier,
            rawScore: rawScore.toFixed(2),
            adjustedScore: adjustedScore.toFixed(2),
            finalACS,
            factors: {
                pages: data.pages,
                time: data.timeToFill,
                documents: data.documents,
                login: data.loginRequired === 'true'
            }
        };
    }

    getPageScore(pages) {
        switch (pages) {
            case '1': return 1;
            case '2-5': return 3;
            case '>5': return 6;
            default: return 1;
        }
    }

    getTimeScore(time) {
        switch (time) {
            case '<5': return 1;
            case '5-15': return 4;
            case '>15': return 8;
            default: return 1;
        }
    }

    getDocumentScore(documents) {
        switch (documents) {
            case '0': return 1;
            case '1': return 3;
            case '>1': return 6;
            default: return 1;
        }
    }

    getFinalACS(adjustedScore) {
        if (adjustedScore <= 1.5) return 1;
        if (adjustedScore <= 2.5) return 2;
        if (adjustedScore <= 3.5) return 3;
        if (adjustedScore <= 4.5) return 4;
        return 5;
    }

    getComplexityLevel(acsScore) {
        const levels = {
            1: "Very Simple",
            2: "Simple", 
            3: "Moderate",
            4: "Complex",
            5: "Very Complex"
        };
        return levels[acsScore] || "Unknown";
    }

    displayResults(acsResult, formData) {
        console.log('displayResults called with:', acsResult, formData);
        
        const scoreSection = document.getElementById('scoreSection');
        const acsScore = document.getElementById('acsScore');
        const complexityLevel = document.getElementById('complexityLevel');
        const scoreExplanation = document.getElementById('scoreExplanation');
        const businessImplications = document.getElementById('businessImplications');

        console.log('Found elements:', {
            scoreSection: !!scoreSection,
            acsScore: !!acsScore,
            complexityLevel: !!complexityLevel,
            scoreExplanation: !!scoreExplanation,
            businessImplications: !!businessImplications
        });

        if (scoreSection && acsScore && complexityLevel && scoreExplanation && businessImplications) {
            console.log('All elements found, updating content...');
            
            // Display ACS score
            acsScore.textContent = acsResult.finalACS;
            
            // Display complexity level
            complexityLevel.textContent = this.getComplexityLevel(acsResult.finalACS);
            
            // Update score circle color based on ACS level
            const scoreCircle = document.querySelector('.score-circle');
            if (scoreCircle) {
                scoreCircle.className = `score-circle acs-${acsResult.finalACS}`;
            }

            // Display score explanation
            scoreExplanation.innerHTML = this.getScoreExplanation(acsResult);
            
            // Display business implications
            businessImplications.innerHTML = this.getBusinessImplications(acsResult);
            
            // Show results section
            scoreSection.style.display = 'block';
            console.log('Results section should now be visible');
            
            // Scroll to results
            scoreSection.scrollIntoView({ behavior: 'smooth' });
        } else {
            console.error('Missing required elements for displaying results:', {
                scoreSection: !!scoreSection,
                acsScore: !!acsScore,
                rawScore: !!rawScore,
                adjustedScore: !!adjustedScore,
                complexityLevel: !!complexityLevel,
                scoreExplanation: !!scoreExplanation,
                businessImplications: !!businessImplications
            });
        }
    }

    getScoreExplanation(acsResult) {
        const explanations = {
            1: "Your application process is very simple and user-friendly. This typically results in the highest application volume and lowest cost-per-application (CPA).",
            2: "Your application process is simple and efficient. This provides a good balance of high volume and reasonable quality, ideal for volume-focused campaigns.",
            3: "Your application process has moderate complexity. This offers a balanced approach between application volume and candidate quality.",
            4: "Your application process is relatively complex. This may result in lower volume but higher quality candidates, potentially leading to higher CPAs.",
            5: "Your application process is very complex. This represents the complexity ceiling where additional complexity won't significantly impact user abandonment rates."
        };
        
        return `<p><strong>ACS ${acsResult.finalACS}</strong>: ${explanations[acsResult.finalACS]}</p>`;
    }

    getBusinessImplications(acsResult) {
        const implications = {
            1: `
                <ul>
                    <li><strong>Volume Potential:</strong> Very high - expect maximum application volume</li>
                    <li><strong>CPA Impact:</strong> Lowest cost-per-application</li>
                    <li><strong>Quality:</strong> Standard candidate quality</li>
                    <li><strong>Best For:</strong> High-volume recruitment campaigns, entry-level positions</li>
                    <li><strong>Recommendation:</strong> Focus on volume optimization and broad reach</li>
                </ul>
            `,
            2: `
                <ul>
                    <li><strong>Volume Potential:</strong> High - good application volume</li>
                    <li><strong>CPA Impact:</strong> Low to moderate cost-per-application</li>
                    <li><strong>Quality:</strong> Good candidate quality</li>
                    <li><strong>Best For:</strong> Most recruitment campaigns, balanced approach</li>
                    <li><strong>Recommendation:</strong> Optimize for volume while maintaining quality</li>
                </ul>
            `,
            3: `
                <ul>
                    <li><strong>Volume Potential:</strong> Medium - balanced application volume</li>
                    <li><strong>CPA Impact:</strong> Moderate cost-per-application</li>
                    <li><strong>Quality:</strong> Good to high candidate quality</li>
                    <li><strong>Best For:</strong> Mid-level positions, quality-focused campaigns</li>
                    <li><strong>Recommendation:</strong> Balance volume and quality optimization</li>
                </ul>
            `,
            4: `
                <ul>
                    <li><strong>Volume Potential:</strong> Low to medium - reduced application volume</li>
                    <li><strong>CPA Impact:</strong> Higher cost-per-application</li>
                    <li><strong>Quality:</strong> High candidate quality</li>
                    <li><strong>Best For:</strong> Senior positions, quality-focused campaigns</li>
                    <li><strong>Recommendation:</strong> Focus on quality optimization and targeted reach</li>
                </ul>
            `,
            5: `
                <ul>
                    <li><strong>Volume Potential:</strong> Very low - minimal application volume</li>
                    <li><strong>CPA Impact:</strong> Highest cost-per-application</li>
                    <li><strong>Quality:</strong> Premium candidate quality</li>
                    <li><strong>Best For:</strong> Executive positions, specialized roles</li>
                    <li><strong>Recommendation:</strong> Consider simplifying the process or targeting premium candidates only</li>
                </ul>
            `
        };
        
        return implications[acsResult.finalACS];
    }

    updateRealTimeCalculation() {
        // This could show a preview calculation as user fills the form
        // For now, we'll just validate the form
        const form = document.getElementById('acsForm');
        const submitButton = form.querySelector('.submit-button');
        
        if (form) {
            const requiredFields = form.querySelectorAll('[required]');
            const allFilled = Array.from(requiredFields).every(field => field.value.trim() !== '');
            
            if (allFilled) {
                submitButton.disabled = false;
                submitButton.style.opacity = '1';
            } else {
                submitButton.disabled = true;
                submitButton.style.opacity = '0.6';
            }
        }
    }

    async storeData(formData, acsResult) {
        const dataToStore = {
            timestamp: new Date().toISOString(),
            clientName: formData.clientName,
            jobLink: formData.jobLink || '',
            atsName: formData.atsName || '',
            pages: formData.pages,
            timeToFill: formData.timeToFill,
            documents: formData.documents,
            loginRequired: formData.loginRequired === 'true',
            acsScore: acsResult.finalACS,
            rawScore: acsResult.rawScore,
            adjustedScore: acsResult.adjustedScore,
            pageScore: acsResult.pageScore,
            timeScore: acsResult.timeScore,
            documentScore: acsResult.documentScore,
            loginMultiplier: acsResult.loginMultiplier
        };

        console.log('Data to store:', dataToStore);
        
        // Store in backend (Google Sheets)
        try {
            const response = await fetch(`/store-calculation`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(dataToStore)
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.showNotification(`✅ Data stored in Google Sheets (Row ${result.row_number})`, 'success');
                console.log('Data stored successfully:', result);
            } else {
                this.showNotification(`⚠️ Storage failed: ${result.message}`, 'warning');
                console.warn('Storage failed:', result);
            }
            
        } catch (error) {
            console.error('Error storing data:', error);
            this.showNotification('❌ Error connecting to backend', 'error');
        }
    }

    // Show notification to user
    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <span class="notification-message">${message}</span>
            <button class="notification-close">&times;</button>
        `;

        // Add to page
        document.body.appendChild(notification);

        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 5000);

        // Close button functionality
        const closeBtn = notification.querySelector('.notification-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            });
        }
    }
}

// Initialize the calculator when the page loads
document.addEventListener('DOMContentLoaded', () => {
    const calculator = new ACSCalculator();
    
    // Force dropdown styling after a short delay to ensure DOM is fully loaded
    setTimeout(() => {
        calculator.forceDropdownStyling();
    }, 100);
    
    // Add some visual feedback for form interactions
    const formInputs = document.querySelectorAll('.form-input, .form-select');
    formInputs.forEach(input => {
        input.addEventListener('focus', () => {
            input.parentElement.parentElement.classList.add('focused');
        });
        
        input.addEventListener('blur', () => {
            input.parentElement.parentElement.classList.remove('focused');
        });
    });
});

// Add CSS for focused state
const style = document.createElement('style');
style.textContent = `
    .form-field.focused .field-icon {
        background: #e3f2fd;
        border: 2px solid #1976d2;
    }
    
    .form-field.focused .field-icon i {
        color: #1976d2;
    }
    
    .acs-1 .score-circle { background: linear-gradient(135deg, #4caf50 0%, #66bb6a 100%); }
    .acs-2 .score-circle { background: linear-gradient(135deg, #8bc34a 0%, #9ccc65 100%); }
    .acs-3 .score-circle { background: linear-gradient(135deg, #ff9800 0%, #ffb74d 100%); }
    .acs-4 .score-circle { background: linear-gradient(135deg, #f57c00 0%, #ff8a65 100%); }
    .acs-5 .score-circle { background: linear-gradient(135deg, #d32f2f 0%, #ef5350 100%); }
`;
document.head.appendChild(style);

// Modal functionality
const modal = document.getElementById('similarClientsModal');
const findSimilarBtn = document.getElementById('findSimilarBtn');
const closeBtn = document.querySelector('.close');
const searchBtn = document.getElementById('searchSimilarBtn');
// jobTitleInput removed - now using only dropdown
const jobCategorySelect = document.getElementById('jobCategorySelect');
const resultsSection = document.getElementById('resultsSection');
const loadingSection = document.getElementById('loadingSection');
const clientsList = document.getElementById('clientsList');
const searchCategory = document.getElementById('searchCategory');
            const countrySelect = document.getElementById('countrySelect');

// Open modal
findSimilarBtn.addEventListener('click', () => {
    modal.style.display = 'block';
    document.body.style.overflow = 'hidden';
});

// Close modal
closeBtn.addEventListener('click', () => {
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
    resetModal();
});

// Close modal when clicking outside
window.addEventListener('click', (event) => {
    if (event.target === modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
        resetModal();
    }
});

// Reset modal state
function resetModal() {
    jobCategorySelect.value = '';
    resultsSection.style.display = 'none';
    loadingSection.style.display = 'none';
    clientsList.innerHTML = '';
}

// Search for similar clients
searchBtn.addEventListener('click', async () => {
    const jobCategory = jobCategorySelect.value;
    const country = countrySelect.value.trim() || null;
    
    if (!jobCategory) {
        alert('Please select a job category');
        return;
    }
    
    // Show loading
    loadingSection.style.display = 'block';
    resultsSection.style.display = 'none';
    
    try {
        // Get current ACS score for comparison
        const currentAcsScore = parseInt(document.getElementById('acsScore').textContent);
        
        // Prepare search parameters
        const searchParams = {
            target_acs: currentAcsScore,
            target_category: jobCategory,
            target_country: country || null,
            max_results: 10
        };
        
        // Call backend API
        const response = await fetch(`/find-similar-clients`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(searchParams)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Hide loading and show results
        loadingSection.style.display = 'none';
        displayResults(data, jobCategory || jobTitle, country);
        
    } catch (error) {
        console.error('Error searching for similar clients:', error);
        loadingSection.style.display = 'none';
        
        // Show error message
        clientsList.innerHTML = `
            <div class="error-message">
                <p>❌ Error searching for similar clients. Please try again.</p>
                <p class="error-details">${error.message}</p>
            </div>
        `;
        resultsSection.style.display = 'block';
    }
});

// Display search results
function displayResults(response, category, country) {
    // Extract clients from the response structure
    const clients = response.clients || [];
    
    if (!clients || clients.length === 0) {
        const countryText = country ? ` in ${country}` : '';
        clientsList.innerHTML = `
            <div class="no-results">
                <p>🔍 No similar clients found for "${category}"${countryText} with ACS ${document.getElementById('acsScore').textContent}</p>
                <p>Try a different job category, title, or country.</p>
                <p><strong>Available categories include:</strong> Tellers, Software Developers, Accountants and Auditors, Registered Nurses, etc.</p>
            </div>
        `;
    } else {
        const countryText = country ? ` in ${country}` : '';
        searchCategory.textContent = `${category}${countryText}`;
        
        const clientsHTML = clients.map(client => `
            <div class="client-card">
                <div class="client-header">
                    <h3 class="client-name">${client.client_name}</h3>
                    <span class="acs-badge">ACS ${client.acs_score}</span>
                </div>
                
                <div class="client-stats">
                    <div class="stat-item">
                        <div class="stat-label">Job Categories Count</div>
                        <div class="stat-value">${client.job_count.toLocaleString()}</div>
                    </div>
                </div>
                
                <div class="sample-jobs">
                    <h4>💼 Sample Job Titles:</h4>
                    <div class="job-tags">
                        ${client.sample_job_titles.map(job => 
                            `<span class="job-tag">${job}</span>`
                        ).join('')}
                    </div>
                </div>
            </div>
        `).join('');
        
        clientsList.innerHTML = clientsHTML;
    }
    
    resultsSection.style.display = 'block';
}

// Add error message styles
const errorStyles = document.createElement('style');
errorStyles.textContent = `
    .error-message {
        text-align: center;
        padding: 2rem;
        background: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 10px;
        color: #721c24;
    }
    
    .error-details {
        font-size: 0.9rem;
        opacity: 0.8;
        margin-top: 0.5rem;
    }
    
    .no-results {
        text-align: center;
        padding: 2rem;
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 10px;
        color: #6c757d;
    }
`;
document.head.appendChild(errorStyles);

// Tab functionality
document.addEventListener('DOMContentLoaded', function() {
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetTab = button.getAttribute('data-tab');
            
            // Remove active class from all buttons and contents
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Add active class to clicked button and corresponding content
            button.classList.add('active');
            document.getElementById(`${targetTab}-tab`).classList.add('active');
            
            // Load database data when switching to database tab
            if (targetTab === 'database') {
                loadDatabaseData();
            }
        });
    });
});

// Database functionality
let allClientsData = [];

async function loadDatabaseData() {
    const loadingSection = document.getElementById('databaseLoadingSection');
    const tableContainer = document.getElementById('clientsTableContainer');
    const noResults = document.getElementById('databaseNoResults');
    const resultsCount = document.getElementById('databaseResultsCount');
    
    loadingSection.style.display = 'block';
    tableContainer.style.display = 'none';
    noResults.style.display = 'none';
    
    try {
        // Fetch real client data from the backend
        const response = await fetch('/get-all-clients');
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.success) {
            allClientsData = data.clients;
            displayDatabaseResults(allClientsData);
        } else {
            throw new Error(data.message || 'Failed to load client data');
        }
        
    } catch (error) {
        console.error('Error loading database data:', error);
        displayDatabaseError(error.message);
    } finally {
        loadingSection.style.display = 'none';
    }
}

function generateSampleClientData() {
    // This is sample data based on real client names from the logs and common job categories
    const countries = ['United States', 'Germany', 'Canada', 'Switzerland', 'Netherlands', 'Australia', 'Austria', 'Argentina', 'Guadeloupe', 'United Kingdom', 'France', 'Spain', 'Italy', 'Brazil', 'Mexico', 'India', 'Japan', 'China'];
    const categories = [
        'Registered Nurses', 'Software Engineers', 'Bank Tellers', 'Sales Representatives',
        'Administrative Assistants', 'Truck Drivers', 'Cashiers', 'Customer Service Representatives',
        'Financial Managers', 'Marketing Specialists', 'Human Resources', 'Operations Managers',
        'First-Line Supervisors of Production and Operating Workers', 'Taxi Drivers', 'Administrative Services Managers',
        'Computer User Support Specialists', 'Heavy and Tractor-Trailer Truck Drivers', 'Medical Assistants',
        'Retail Sales Workers', 'Food Service Workers', 'Security Guards', 'Janitors and Cleaners'
    ];
    
    const clients = [
        'Adecco', 'Uber Eats', 'Just Eat Takeaway', 'Scale AI', 'CareRite', 'Roadie',
        'Centers Healthcare', 'Hoops HR', 'DIS AG', 'LHH', 'Spring Health', 'MVT',
        'Piening GmbH', 'inCare by Piening', 'ING Netherlands', 'KCB', 'Lonza',
        'Aveanna Healthcare', 'Recruitics - DE', 'Adecco - Switzerland - Opti',
        'Piening GmbH Bielefeld', 'Piening GmbH Berlin', 'TAG - LHH - USA',
        'LHH Recruitment Solutions', 'Just Eat Takeaway - Corporate', 'Just Eat Takeaway - Courier',
        'Uber exchange', 'DIS AG-Exchange', 'DIS AG Central Campaigns Exchange',
        'Adecco World Wide Web DE', 'Adecco Personaldienstleistungen GmbH'
    ];
    
    const data = [];
    
    // Generate more comprehensive data with realistic combinations
    for (let i = 0; i < 100; i++) {
        const client = clients[Math.floor(Math.random() * clients.length)];
        const category = categories[Math.floor(Math.random() * categories.length)];
        const country = countries[Math.floor(Math.random() * countries.length)];
        const acs_score = Math.floor(Math.random() * 5) + 1;
        
        data.push({
            client_name: client + (i > clients.length ? ` - ${i}` : ''),
            job_category: category,
            country: country,
            acs_score: acs_score,
            complexity_level: getComplexityLevel(acs_score)
        });
    }
    
    // Sort by client name for better organization
    return data.sort((a, b) => a.client_name.localeCompare(b.client_name));
}

function getComplexityLevel(score) {
    const levels = {
        1: 'Very Simple',
        2: 'Simple', 
        3: 'Moderate',
        4: 'Complex',
        5: 'Very Complex'
    };
    return levels[score] || 'Unknown';
}

function displayDatabaseResults(clients) {
    const tableBody = document.getElementById('clientsTableBody');
    const resultsCount = document.getElementById('databaseResultsCount');
    const tableContainer = document.getElementById('clientsTableContainer');
    const noResults = document.getElementById('databaseNoResults');
    
    if (clients.length === 0) {
        tableContainer.style.display = 'none';
        noResults.style.display = 'block';
        resultsCount.textContent = '0 clients found';
        return;
    }
    
    resultsCount.textContent = `${clients.length} clients found`;
    
    const clientsHTML = clients.map(client => `
        <tr>
            <td><strong>${client.client_name}</strong></td>
            <td><span class="score-badge">${client.acs_score}</span></td>
            <td><span class="complexity-level level-${client.acs_score}">${client.complexity_level}</span></td>
        </tr>
    `).join('');
    
    tableBody.innerHTML = clientsHTML;
    tableContainer.style.display = 'block';
    noResults.style.display = 'none';
}

function displayDatabaseError(message) {
    const tableContainer = document.getElementById('clientsTableContainer');
    const noResults = document.getElementById('databaseNoResults');
    const resultsCount = document.getElementById('databaseResultsCount');
    
    tableContainer.style.display = 'none';
    noResults.style.display = 'block';
    noResults.innerHTML = `<p>Error loading client data: ${message}</p>`;
    resultsCount.textContent = 'Error';
}

// Database filtering functionality
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('databaseSearch');
    const acsFilter = document.getElementById('databaseAcsFilter');
    
    function filterDatabase() {
        if (allClientsData.length === 0) return;
        
        const searchTerm = searchInput.value.toLowerCase();
        const selectedAcs = acsFilter.value;
        
        const filteredClients = allClientsData.filter(client => {
            const matchesSearch = !searchTerm || 
                client.client_name.toLowerCase().includes(searchTerm);
            
            const matchesAcs = !selectedAcs || client.acs_score.toString() === selectedAcs;
            
            return matchesSearch && matchesAcs;
        });
        
        displayDatabaseResults(filteredClients);
    }
    
    if (searchInput) searchInput.addEventListener('input', filterDatabase);
    if (acsFilter) acsFilter.addEventListener('change', filterDatabase);
});
