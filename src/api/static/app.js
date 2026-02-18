/**
 * BADI Oerlikon Attendance Tracker - Frontend Application
 */

const API_BASE_URL = '/api';
let autoRefreshInterval = null;
let autoRefreshEnabled = false;

/**
 * Initialize the application
 */
document.addEventListener('DOMContentLoaded', () => {
    console.log('Initializing BADI Oerlikon Tracker');
    
    // Set up event listeners
    document.getElementById('refreshBtn').addEventListener('click', refreshData);
    document.getElementById('autoRefreshBtn').addEventListener('click', toggleAutoRefresh);
    
    // Load initial data
    loadLatestData();
    loadHistory();
});

/**
 * Fetch and display latest data
 */
async function loadLatestData() {
    const statusBox = document.getElementById('currentStatus');
    const lastUpdatedDiv = document.getElementById('lastUpdated');
    const latestDataDiv = document.getElementById('latestData');
    
    try {
        statusBox.classList.remove('loading', 'available', 'busy', 'full');
        statusBox.classList.add('loading');
        statusBox.innerHTML = '<div class="loading-spinner"></div>';
        
        const response = await fetch(`${API_BASE_URL}/data/latest`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Display the data
        displayLatestData(data, statusBox, lastUpdatedDiv, latestDataDiv);
        
    } catch (error) {
        console.error('Error loading latest data:', error);
        statusBox.classList.remove('loading');
        statusBox.innerHTML = `<p class="error-message">Error loading data: ${error.message}</p>`;
        lastUpdatedDiv.textContent = 'Error';
    }
}

/**
 * Display the latest data in the UI
 */
function displayLatestData(data, statusBox, lastUpdatedDiv, latestDataDiv) {
    // Update timestamp
    const timestamp = data.timestamp || new Date().toISOString();
    const date = new Date(timestamp);
    lastUpdatedDiv.textContent = date.toLocaleString();
    
    // Determine status based on data
    let status = 'unknown';
    let statusText = 'Status Unknown';
    
    const scrapedData = data.data || {};
    if (scrapedData.occupancy !== undefined) {
        const occupancy = scrapedData.occupancy;
        if (occupancy <= 30) {
            status = 'available';
            statusText = `✅ Available (${occupancy}% occupied)`;
        } else if (occupancy <= 70) {
            status = 'busy';
            statusText = `⚠️ Busy (${occupancy}% occupied)`;
        } else {
            status = 'full';
            statusText = `🚫 Full (${occupancy}% occupied)`;
        }
    }
    
    // Update status display
    statusBox.classList.remove('loading');
    statusBox.classList.add(status);
    statusBox.innerHTML = `<p>${statusText}</p>`;
    
    // Display raw data
    latestDataDiv.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
}

/**
 * Load and display history
 */
async function loadHistory() {
    const historyDiv = document.getElementById('historyList');
    
    try {
        const response = await fetch(`${API_BASE_URL}/data/blobs`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        const blobs = result.blobs || [];
        
        if (blobs.length === 0) {
            historyDiv.innerHTML = '<p>No historical data available</p>';
            return;
        }
        
        // Display blobs in reverse order (most recent first)
        const historyHTML = blobs
            .reverse()
            .slice(0, 10) // Show last 10
            .map(blob => `
                <div class="history-item" onclick="loadHistoryItem('${blob}')">
                    <div class="history-item-timestamp">${formatBlobName(blob)}</div>
                    <div class="history-item-info">Click to view details</div>
                </div>
            `)
            .join('');
        
        historyDiv.innerHTML = historyHTML;
        
    } catch (error) {
        console.error('Error loading history:', error);
        historyDiv.innerHTML = `<p class="error-message">Error loading history: ${error.message}</p>`;
    }
}

/**
 * Load and display specific history item
 */
async function loadHistoryItem(blobName) {
    try {
        const response = await fetch(`${API_BASE_URL}/data/${blobName}`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        const latestDataDiv = document.getElementById('latestData');
        latestDataDiv.innerHTML = `
            <p><strong>Viewing: ${formatBlobName(blobName)}</strong></p>
            <pre>${JSON.stringify(data, null, 2)}</pre>
        `;
        
        // Scroll to data section
        latestDataDiv.scrollIntoView({ behavior: 'smooth' });
        
    } catch (error) {
        console.error('Error loading history item:', error);
        alert(`Error loading data: ${error.message}`);
    }
}

/**
 * Refresh data
 */
async function refreshData() {
    const btn = document.getElementById('refreshBtn');
    btn.disabled = true;
    btn.textContent = '⏳ Refreshing...';
    
    try {
        await loadLatestData();
        await loadHistory();
    } finally {
        btn.disabled = false;
        btn.textContent = '↻ Refresh Now';
    }
}

/**
 * Toggle auto-refresh
 */
function toggleAutoRefresh() {
    const btn = document.getElementById('autoRefreshBtn');
    
    if (autoRefreshEnabled) {
        // Disable auto-refresh
        autoRefreshEnabled = false;
        clearInterval(autoRefreshInterval);
        btn.classList.remove('active');
        btn.textContent = '⏱ Auto Refresh (60s)';
    } else {
        // Enable auto-refresh
        autoRefreshEnabled = true;
        btn.classList.add('active');
        btn.textContent = '⏸ Auto Refresh (60s) - Active';
        
        // Refresh immediately
        refreshData();
        
        // Set up interval
        autoRefreshInterval = setInterval(() => {
            refreshData();
        }, 60000); // 60 seconds
    }
}

/**
 * Format blob name to readable timestamp
 */
function formatBlobName(blobName) {
    // Format: scraped_data_2024-01-15_14-30-45.json
    const match = blobName.match(/scraped_data_(\d{4}-\d{2}-\d{2})_(\d{2})-(\d{2})-(\d{2})/);
    if (match) {
        const date = `${match[1]} ${match[2]}:${match[3]}:${match[4]}`;
        return date;
    }
    return blobName;
}

// Clean up on page unload
window.addEventListener('beforeunload', () => {
    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
    }
});
