
// Network Scanning Functionality
function initializeNetworkScan() {
    console.log("Network scanner initialized");
}

function scanNetwork(ipAddress) {
    if (!ipAddress) {
        alert('Please enter an IP address');
        return;
    }

    // Show scanning progress
    showScanProgress(ipAddress);

    // Call backend API
    fetch('/api/v1/network/scan', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ ip: ipAddress })
    })
    .then(response => response.json())
    .then(data => {
        displayNetworkResults(data);
    })
    .catch(error => {
        console.error('Network scan error:', error);
        displayScanError(error);
    });
}

function showScanProgress(ip) {
    const resultsContainer = document.getElementById('networkResults');
    resultsContainer.innerHTML = `
        <div class="result-item result-clean">
            <div class="result-icon"><i class="fas fa-search"></i></div>
            <div>
                <h4>Network Scan in Progress</h4>
                <p>Scanning IP: <strong>${ip}</strong></p>
                <div class="scan-progress">
                    <div class="progress-bar">
                        <div class="progress-fill"></div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

function displayNetworkResults(data) {
    const resultsContainer = document.getElementById('networkResults');
    
    if (data.error) {
        resultsContainer.innerHTML = `
            <div class="result-item result-malicious">
                <div class="result-icon"><i class="fas fa-exclamation-triangle"></i></div>
                <div>
                    <h4>Scan Error</h4>
                    <p>${data.error}</p>
                </div>
            </div>
        `;
        return;
    }

    const threatLevel = data.threat_assessment?.level || 'Unknown';
    const threatClass = threatLevel === 'High' ? 'result-malicious' : 
                       threatLevel === 'Medium' ? 'result-suspicious' : 'result-clean';

    let portsHTML = '';
    if (data.open_ports && data.open_ports.length > 0) {
        portsHTML = data.open_ports.map(port => `
            <div class="port-item">
                <span class="port-number">${port.port}</span>
                <span class="port-service">${port.service}</span>
                <span class="port-status status-open">OPEN</span>
            </div>
        `).join('');
    } else {
        portsHTML = '<p>No open ports detected</p>';
    }

    let warningsHTML = '';
    if (data.threat_assessment?.warnings && data.threat_assessment.warnings.length > 0) {
        warningsHTML = data.threat_assessment.warnings.map(warning => `
            <div class="warning-item">
                <i class="fas fa-exclamation-circle"></i> ${warning}
            </div>
        `).join('');
    }

    resultsContainer.innerHTML = `
        <div class="analysis-report">
            <div class="report-header">
                <div class="report-title">Network Intelligence Report</div>
                <div class="report-timestamp">${new Date().toLocaleString()}</div>
            </div>
            
            <div class="report-section">
                <div class="section-header">
                    <i class="fas fa-network-wired"></i>
                    <h3>Target Information</h3>
                </div>
                <div class="metadata-grid">
                    <div class="metadata-item">
                        <div class="metadata-label">IP Address</div>
                        <div class="metadata-value">${data.ip}</div>
                    </div>
                    <div class="metadata-item">
                        <div class="metadata-label">Reachability</div>
                        <div class="metadata-value">${data.reachable ? '✅ Reachable' : '❌ Not Reachable'}</div>
                    </div>
                    <div class="metadata-item">
                        <div class="metadata-label">Hostname</div>
                        <div class="metadata-value">${data.hostname || 'Unknown'}</div>
                    </div>
                    <div class="metadata-item">
                        <div class="metadata-label">Network Type</div>
                        <div class="metadata-value">${data.network_info?.type || 'Unknown'}</div>
                    </div>
                </div>
            </div>
            
            <div class="report-section">
                <div class="section-header">
                    <i class="fas fa-shield-alt"></i>
                    <h3>Threat Assessment</h3>
                </div>
                <div class="verdict-box ${threatClass}">
                    <div class="verdict-icon">
                        <i class="fas fa-${threatLevel === 'High' ? 'skull-crossbones' : threatLevel === 'Medium' ? 'exclamation-triangle' : 'check-circle'}"></i>
                    </div>
                    <div class="verdict-content">
                        <h3>${threatLevel.toUpperCase()} THREAT LEVEL</h3>
                        <p>Threat Score: ${data.threat_assessment?.threat_score || 0}/100</p>
                        <p>Open Ports: ${data.threat_assessment?.open_port_count || 0}</p>
                    </div>
                </div>
                ${warningsHTML ? `
                <div class="warning-section">
                    <h4>Security Warnings:</h4>
                    ${warningsHTML}
                </div>
                ` : ''}
            </div>
            
            <div class="report-section">
                <div class="section-header">
                    <i class="fas fa-door-open"></i>
                    <h3>Open Ports (${data.open_ports?.length || 0})</h3>
                </div>
                <div class="ports-grid">
                    ${portsHTML}
                </div>
            </div>
        </div>
    `;
}

function displayScanError(error) {
    const resultsContainer = document.getElementById('networkResults');
    resultsContainer.innerHTML = `
        <div class="result-item result-malicious">
            <div class="result-icon"><i class="fas fa-exclamation-triangle"></i></div>
            <div>
                <h4>Network Scan Failed</h4>
                <p>Error: ${error.message || 'Unknown error occurred'}</p>
            </div>
        </div>
    `;
}
