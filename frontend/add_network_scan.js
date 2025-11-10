// Simple network scan function to add to existing JavaScript
function scanNetwork(ipAddress) {
    if (!ipAddress) {
        alert('Please enter an IP address');
        return;
    }

    const resultsContainer = document.getElementById('networkResults');
    resultsContainer.innerHTML = '<div class="result-item result-clean"><div class="result-icon"><i class="fas fa-search"></i></div><div><h4>Scanning Network...</h4><p>Scanning IP: ' + ipAddress + '</p></div></div>';

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
        resultsContainer.innerHTML = '<div class="result-item result-malicious"><div class="result-icon"><i class="fas fa-exclamation-triangle"></i></div><div><h4>Scan Failed</h4><p>Error: ' + error.message + '</p></div></div>';
    });
}

function displayNetworkResults(data) {
    const resultsContainer = document.getElementById('networkResults');
    
    if (data.error) {
        resultsContainer.innerHTML = '<div class="result-item result-malicious"><div class="result-icon"><i class="fas fa-exclamation-triangle"></i></div><div><h4>Scan Error</h4><p>' + data.error + '</p></div></div>';
        return;
    }

    let threatClass = 'result-clean';
    let threatIcon = 'check-circle';
    if (data.threat_assessment?.level === 'High') {
        threatClass = 'result-malicious';
        threatIcon = 'skull-crossbones';
    } else if (data.threat_assessment?.level === 'Medium') {
        threatClass = 'result-suspicious';
        threatIcon = 'exclamation-triangle';
    }

    let portsHTML = '';
    if (data.open_ports && data.open_ports.length > 0) {
        data.open_ports.forEach(port => {
            portsHTML += '<div style="display: flex; justify-content: space-between; padding: 0.5rem; border-bottom: 1px solid rgba(255,255,255,0.1)"><span>Port ' + port.port + '</span><span>' + port.service + '</span><span style="color: #68d391">OPEN</span></div>';
        });
    } else {
        portsHTML = '<p>No open ports detected</p>';
    }

    resultsContainer.innerHTML = `
        <div class="analysis-report">
            <div class="report-header">
                <div class="report-title">Network Scan Report</div>
                <div class="report-timestamp">${new Date().toLocaleString()}</div>
            </div>
            
            <div class="report-section">
                <div class="section-header">
                    <i class="fas fa-network-wired"></i>
                    <h3>Target Information</h3>
                </div>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
                    <div style="background: rgba(15, 23, 42, 0.5); padding: 1rem; border-radius: 6px;">
                        <div style="font-size: 0.8rem; color: #a0aec0;">IP Address</div>
                        <div style="font-weight: 600;">${data.ip}</div>
                    </div>
                    <div style="background: rgba(15, 23, 42, 0.5); padding: 1rem; border-radius: 6px;">
                        <div style="font-size: 0.8rem; color: #a0aec0;">Reachability</div>
                        <div style="font-weight: 600;">${data.reachable ? '✅ Reachable' : '❌ Not Reachable'}</div>
                    </div>
                    <div style="background: rgba(15, 23, 42, 0.5); padding: 1rem; border-radius: 6px;">
                        <div style="font-size: 0.8rem; color: #a0aec0;">Network Type</div>
                        <div style="font-weight: 600;">${data.network_info?.type || 'Unknown'}</div>
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
                        <i class="fas fa-${threatIcon}"></i>
                    </div>
                    <div class="verdict-content">
                        <h3>${data.threat_assessment?.level?.toUpperCase() || 'UNKNOWN'} THREAT LEVEL</h3>
                        <p>Threat Score: ${data.threat_assessment?.threat_score || 0}/100</p>
                        <p>Open Ports: ${data.open_ports?.length || 0}</p>
                    </div>
                </div>
            </div>
            
            <div class="report-section">
                <div class="section-header">
                    <i class="fas fa-door-open"></i>
                    <h3>Open Ports (${data.open_ports?.length || 0})</h3>
                </div>
                <div>
                    ${portsHTML}
                </div>
            </div>
        </div>
    `;
}
