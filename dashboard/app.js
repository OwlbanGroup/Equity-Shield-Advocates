const API_BASE_URL = 'http://localhost:5001';
const RETRY_DELAY = 5000; // 5 seconds
const MAX_RETRIES = 3;

// Utility function to format currency
function formatCurrency(value) {
    if (value === null || value === undefined) return 'N/A';
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(value);
}

// Function to create a status indicator
function createStatusIndicator(status) {
    const isHealthy = status.toLowerCase() === 'healthy' || status.toLowerCase() === 'success';
    return `
        <span class="status-indicator status-${isHealthy ? 'healthy' : 'unhealthy'}"></span>
        ${status}
    `;
}

// Function to show loading state
function showLoading(elementId) {
    const element = document.getElementById(elementId);
    element.innerHTML = `
        <div class="loading">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
    `;
}

// Function to display error message with retry button
function showError(elementId, message, retryFunction) {
    const element = document.getElementById(elementId);
    element.innerHTML = `
        <div class="error-message">
            <i class="fas fa-exclamation-circle"></i>
            Error: ${message}
            <button class="btn btn-sm btn-outline-primary mt-2" onclick="${retryFunction.name}()">
                <i class="fas fa-sync"></i> Retry
            </button>
        </div>
    `;
}

// Function to fetch data with retries
async function fetchWithRetry(url, retries = MAX_RETRIES) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        if (data.status === 'error') {
            throw new Error(data.message || 'API returned an error');
        }
        return data;
    } catch (error) {
        if (retries > 0) {
            await new Promise(resolve => setTimeout(resolve, RETRY_DELAY));
            return fetchWithRetry(url, retries - 1);
        }
        throw error;
    }
}

// Function to update the health status
async function updateHealthStatus() {
    const elementId = 'health-status';
    showLoading(elementId);
    try {
        const data = await fetchWithRetry(`${API_BASE_URL}/health`);
        document.getElementById(elementId).innerHTML = `
            <div>
                ${createStatusIndicator(data.status)}
                <div class="timestamp">Last updated: ${new Date().toLocaleString()}</div>
                <div>Version: ${data.version}</div>
            </div>
        `;
    } catch (error) {
        showError(elementId, error.message, updateHealthStatus);
    }
}

// Function to update corporate data
async function updateCorporateData() {
    const elementId = 'corporate-data';
    showLoading(elementId);
    try {
        const response = await fetchWithRetry(`${API_BASE_URL}/api/v1/corporate-data`);
        const data = response.data;
        document.getElementById(elementId).innerHTML = `
            <div class="list-group">
                <div class="list-group-item">
                    <h6 class="mb-1">Executive Summary</h6>
                    <p class="mb-1">${data.executive_summary}</p>
                </div>
                <div class="list-group-item">
                    <h6 class="mb-1">Fund Overview</h6>
                    <p class="mb-1">${data.fund_overview}</p>
                </div>
                <div class="list-group-item">
                    <h6 class="mb-1">Investment Strategy</h6>
                    <p class="mb-1">${data.investment_strategy}</p>
                </div>
                <div class="list-group-item">
                    <h6 class="mb-1">Risk Assessment</h6>
                    <p class="mb-1">${data.risk_assessment}</p>
                </div>
                <div class="list-group-item">
                    <h6 class="mb-1">AUM</h6>
                    <p class="mb-1">${data.aum || 'N/A'}</p>
                </div>
            </div>
            <div class="timestamp">Last updated: ${new Date().toLocaleString()}</div>
        `;
    } catch (error) {
        showError(elementId, error.message, updateCorporateData);
    }
}

// Function to update corporate structure
async function updateCorporateStructure() {
    const elementId = 'corporate-structure';
    showLoading(elementId);
    try {
        const response = await fetchWithRetry(`${API_BASE_URL}/api/v1/corporate-structure`);
        const data = response.data;
        document.getElementById(elementId).innerHTML = `
            <div class="department-tree">
                ${data.departments.map(dept => `
                    <div class="department">
                        <h6>${dept.name}</h6>
                        <ul class="team-list">
                            ${dept.teams.map(team => `
                                <li>
                                    <strong>${team.name}</strong>
                                    <span class="team-info">(${team.size} ${team.role})</span>
                                </li>
                            `).join('')}
                        </ul>
                    </div>
                `).join('')}
            </div>
            <div class="timestamp">Last updated: ${new Date().toLocaleString()}</div>
        `;
    } catch (error) {
        showError(elementId, error.message, updateCorporateStructure);
    }
}

// Function to update real assets
async function updateRealAssets() {
    const elementId = 'real-assets';
    showLoading(elementId);
    try {
        const response = await fetchWithRetry(`${API_BASE_URL}/api/v1/real-assets`);
        const assets = response.data;
        
        document.getElementById(elementId).innerHTML = `
            <div>
                <div class="list-group mt-3">
                    ${assets.map(asset => `
                        <div class="list-group-item">
                            <h6 class="mb-1">${asset.symbol}</h6>
                            <p class="mb-1">Market Cap: ${formatCurrency(asset.market_cap)}</p>
                            <p class="mb-1">Revenue: ${formatCurrency(asset.revenue)}</p>
                            <small>Last Updated: ${new Date(asset.last_updated).toLocaleString()}</small>
                        </div>
                    `).join('')}
                </div>
                <div class="timestamp">Last updated: ${response.last_updated}</div>
                <div>Total Assets: ${response.total_assets}</div>
            </div>
        `;
    } catch (error) {
        showError(elementId, error.message, updateRealAssets);
    }
}

// Function to update all data
async function updateAllData() {
    await Promise.allSettled([
        updateHealthStatus(),
        updateCorporateData(),
        updateCorporateStructure(),
        updateRealAssets()
    ]);
}

// Add refresh button to each card
document.addEventListener('DOMContentLoaded', () => {
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        const header = card.querySelector('.card-header');
        const refreshBtn = document.createElement('button');
        refreshBtn.className = 'btn btn-sm btn-outline-secondary refresh-button';
        refreshBtn.innerHTML = '<i class="fas fa-sync"></i>';
        refreshBtn.onclick = () => {
            const cardId = card.querySelector('.card-body').id;
            switch (cardId) {
                case 'health-status':
                    updateHealthStatus();
                    break;
                case 'corporate-data':
                    updateCorporateData();
                    break;
                case 'corporate-structure':
                    updateCorporateStructure();
                    break;
                case 'real-assets':
                    updateRealAssets();
                    break;
            }
        };
        header.appendChild(refreshBtn);
    });

    // Initial load
    updateAllData();
    // Refresh data every 30 seconds
    setInterval(updateAllData, 30000);
});
