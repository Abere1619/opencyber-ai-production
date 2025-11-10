// Enhanced Threat Detection Functions

let threatStats = {
    totalScans: 0,
    threatsDetected: 0,
    ethiopianOrgs: 12,
    confidenceRate: "95%"
};

function analyzeThreat(type) {
    let inputValue, resultsContainer;
    
    switch(type) {
        case 'url':
            inputValue = document.getElementById('urlInput').value.trim();
            resultsContainer = document.getElementById('urlResults');
            break;
        case 'ip':
            inputValue = document.getElementById('ipInput').value.trim();
            resultsContainer = document.getElementById('ipResults');
            break;
        case 'file':
            if (!window.currentFile) {
                alert('Please select a file first');
                return;
            }
            inputValue = window.currentFile.name;
            resultsContainer = document.getElementById('fileResults');
            break;
    }
    
    if (!inputValue) {
        alert(`Please enter a ${type} to analyze`);
        return;
    }

    // Update statistics
    threatStats.totalScans++;
    updateThreatStats();

    // Show analysis in progress
    showEnhancedAnalysisProgress(type, inputValue, resultsContainer);

    // Call appropriate API endpoint
    let endpoint, payload;
    
    switch(type) {
        case 'url':
            endpoint = '/api/v1/analysis/url';
            payload = { url: inputValue };
            break;
        case 'ip':
            endpoint = '/api/v1/analysis/ip';
            payload = { ip: inputValue };
            break;
        case 'file':
            endpoint = '/api/v1/analysis/file';
            const formData = new FormData();
            formData.append('file', window.currentFile);
            // For file upload, we'll handle differently
            uploadFileForAnalysis(formData, resultsContainer);
            return;
    }

    // Perform API call
    fetch(endpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        displayEnhancedResults(type, data, resultsContainer);
        
        // Update threat stats if threats detected
        if (data.risk_level !== 'low') {
            threatStats.threatsDetected++;
            updateThreatStats();
        }
    })
    .catch(error => {
        console.error('Analysis error:', error);
        displayAnalysisError(error, resultsContainer);
    });
}

function showEnhancedAnalysisProgress(type, inputValue, container) {
    const analysisSteps = {
        url: [
            'Initializing URL Analysis',
            'Checking Ethiopian Organizational Context', 
            'Phishing Pattern Detection',
            'Malware Distribution Analysis',
            'International Threat Feed Check',
            'Final Threat Assessment'
        ],
        ip: [
            'Initializing IP Analysis',
            'Geolocation Lookup',
            'ASN Information Retrieval',
            'Ethiopian Network Context',
            'International Reputation Check',
            'Threat Level Calculation'
        ],
        file: [
            'Initializing File Analysis',
            'File Type Verification',
            'Static Analysis',
            'Behavioral Pattern Detection',
            'AI Engine Processing',
            'Threat Assessment'
        ]
    };
    
    container.innerHTML = `
        <div style="text-align: center; padding: 2rem;">
            <div style="font-size: 3rem; color: var(--link-color); margin-bottom: 1rem;">
                <i class="fas fa-robot"></i>
            </div>
            <h3>Enhanced Threat Analysis in Progress</h3>
            <p>Analyzing ${type.toUpperCase()}: <strong>${inputValue}</strong></p>
            
            <div style="margin: 2rem 0;">
                ${analysisSteps[type].map((step, index) => `
                    <div style="display: flex; align-items: center; padding: 0.5rem 0; border-bottom: 1px solid rgba(255,255,255,0.1)">
                        <i class="fas fa-${index === 0 ? 'play' : 'circle'} ${index === 0 ? 'text-primary' : 'text-muted'}" 
                           style="margin-right: 1rem;"></i>
                        <span>${step}</span>
                    </div>
                `).join('')}
            </div>
            
            <div style="height: 8px; background: rgba(255, 255, 255, 0.1); border-radius: 4px; margin: 1rem 0; overflow: hidden;">
                <div style="height: 100%; border-radius: 4px; background: linear-gradient(90deg, var(--link-color), #c05621); width: 0%; transition: width 0.5s ease;" id="progressBar"></div>
            </div>
        </div>
    `;
    
    // Animate progress
    let progress = 0;
    const progressBar = document.getElementById('progressBar');
    const interval = setInterval(() => {
        progress += 16.6;
        progressBar.style.width = `${progress}%`;
        if (progress >= 100) {
            clearInterval(interval);
        }
    }, 500);
}

function displayEnhancedResults(type, data, container) {
    if (data.error) {
        container.innerHTML = `
            <div class="result-item result-malicious">
                <div class="result-icon"><i class="fas fa-exclamation-triangle"></i></div>
                <div>
                    <h4>Analysis Error</h4>
                    <p>${data.error}</p>
                </div>
            </div>
        `;
        return;
    }

    const threatClass = data.risk_level === 'high' ? 'result-malicious' : 
                       data.risk_level === 'medium' ? 'result-suspicious' : 'result-clean';

    let specificContent = '';
    
    switch(type) {
        case 'url':
            specificContent = generateURLAnalysisContent(data);
            break;
        case 'ip':
            specificContent = generateIPAnalysisContent(data);
            break;
        case 'file':
            specificContent = generateFileAnalysisContent(data);
            break;
    }

    container.innerHTML = `
        <div class="analysis-report">
            <div class="report-header">
                <div class="report-title">Enhanced ${type.toUpperCase()} Threat Analysis</div>
                <div class="report-timestamp">${new Date().toLocaleString()}</div>
            </div>
            
            <div class="report-section">
                <div class="section-header">
                    <i class="fas fa-shield-alt"></i>
                    <h3>Executive Summary</h3>
                </div>
                <div class="verdict-box ${threatClass}">
                    <div class="verdict-icon">
                        <i class="fas fa-${data.risk_level === 'high' ? 'skull-crossbones' : data.risk_level === 'medium' ? 'exclamation-triangle' : 'check-circle'}"></i>
                    </div>
                    <div class="verdict-content">
                        <h3>${data.risk_level.toUpperCase()} RISK LEVEL</h3>
                        <p>Confidence: ${data.confidence}%</p>
                        <p>Analysis Type: ${type.toUpperCase()}</p>
                    </div>
                </div>
            </div>
            
            ${specificContent}
            
            <div class="report-section">
                <div class="section-header">
                    <i class="fas fa-tools"></i>
                    <h3>Security Recommendations</h3>
                </div>
                <div class="recommendation-box">
                    ${generateRecommendations(data, type)}
                </div>
            </div>
        </div>
    `;
}

function generateURLAnalysisContent(data) {
    let orgContextHTML = '';
    if (data.organization_context) {
        const org = data.organization_context;
        orgContextHTML = `
            <div class="metadata-item">
                <div class="metadata-label">Ethiopian Organization</div>
                <div class="metadata-value">${org.is_ethiopian ? 'Yes' : 'No'}</div>
            </div>
            <div class="metadata-item">
                <div class="metadata-label">Organization Type</div>
                <div class="metadata-value">${org.organization_type}</div>
            </div>
            ${org.verified ? `
            <div class="metadata-item">
                <div class="metadata-label">Verified</div>
                <div class="metadata-value">✅ Yes</div>
            </div>
            ` : ''}
        `;
    }

    let threatsHTML = '';
    if (data.threat_indicators && data.threat_indicators.length > 0) {
        threatsHTML = data.threat_indicators.map(indicator => `
            <div class="result-item ${indicator.severity === 'high' ? 'result-malicious' : indicator.severity === 'medium' ? 'result-suspicious' : 'result-clean'}">
                <div class="result-icon">
                    <i class="fas fa-${indicator.severity === 'high' ? 'exclamation-triangle' : 'info-circle'}"></i>
                </div>
                <div>
                    <h4>${indicator.type.toUpperCase()} - ${indicator.severity.toUpperCase()} severity</h4>
                    <p>${indicator.description}</p>
                    <small>Confidence: ${indicator.confidence}%</small>
                </div>
            </div>
        `).join('');
    }

    return `
        <div class="report-section">
            <div class="section-header">
                <i class="fas fa-building"></i>
                <h3>Organizational Context</h3>
            </div>
            <div class="metadata-grid">
                ${orgContextHTML}
            </div>
        </div>
        
        <div class="report-section">
            <div class="section-header">
                <i class="fas fa-exclamation-triangle"></i>
                <h3>Threat Indicators (${data.threat_indicators?.length || 0})</h3>
            </div>
            ${threatsHTML || '<p>No threat indicators detected</p>'}
        </div>
        
        <div class="report-section">
            <div class="section-header">
                <i class="fas fa-globe"></i>
                <h3>International Intelligence</h3>
            </div>
            <div class="metadata-grid">
                <div class="metadata-item">
                    <div class="metadata-label">OpenPhish</div>
                    <div class="metadata-value">${data.international_intel?.openphish || 'Not detected'}</div>
                </div>
                <div class="metadata-item">
                    <div class="metadata-label">URLhaus</div>
                    <div class="metadata-value">${data.international_intel?.urlhaus || 'Not detected'}</div>
                </div>
            </div>
        </div>
    `;
}

function generateIPAnalysisContent(data) {
    return `
        <div class="report-section">
            <div class="section-header">
                <i class="fas fa-map-marker-alt"></i>
                <h3>Geolocation Information</h3>
            </div>
            <div class="metadata-grid">
                <div class="metadata-item">
                    <div class="metadata-label">Country</div>
                    <div class="metadata-value">${data.geo_location?.country || 'Unknown'}</div>
                </div>
                <div class="metadata-item">
                    <div class="metadata-label">City</div>
                    <div class="metadata-value">${data.geo_location?.city || 'Unknown'}</div>
                </div>
                <div class="metadata-item">
                    <div class="metadata-label">ISP</div>
                    <div class="metadata-value">${data.geo_location?.isp || 'Unknown'}</div>
                </div>
            </div>
        </div>
        
        <div class="report-section">
            <div class="section-header">
                <i class="fas fa-network-wired"></i>
                <h3>Network Information</h3>
            </div>
            <div class="metadata-grid">
                <div class="metadata-item">
                    <div class="metadata-label">ASN</div>
                    <div class="metadata-value">${data.asn_info?.asn || 'Unknown'}</div>
                </div>
                <div class="metadata-item">
                    <div class="metadata-label">Organization</div>
                    <div class="metadata-value">${data.asn_info?.organization || 'Unknown'}</div>
                </div>
            </div>
        </div>
        
        ${data.ethiopian_context ? `
        <div class="report-section">
            <div class="section-header">
                <i class="fas fa-flag-et"></i>
                <h3>Ethiopian Network Context</h3>
            </div>
            <div class="metadata-grid">
                <div class="metadata-item">
                    <div class="metadata-label">Ethiopian IP</div>
                    <div class="metadata-value">✅ Yes</div>
                </div>
                <div class="metadata-item">
                    <div class="metadata-label">Provider</div>
                    <div class="metadata-value">${data.ethiopian_context.provider}</div>
                </div>
            </div>
        </div>
        ` : ''}
    `;
}

function generateFileAnalysisContent(data) {
    let threatsHTML = '';
    if (data.threat_indicators && data.threat_indicators.length > 0) {
        threatsHTML = data.threat_indicators.map(indicator => `
            <div class="result-item ${indicator.severity === 'high' ? 'result-malicious' : indicator.severity === 'medium' ? 'result-suspicious' : 'result-clean'}">
                <div class="result-icon">
                    <i class="fas fa-${indicator.severity === 'high' ? 'exclamation-triangle' : 'info-circle'}"></i>
                </div>
                <div>
                    <h4>${indicator.type.toUpperCase()}</h4>
                    <p>${indicator.description}</p>
                    <small>Confidence: ${indicator.confidence}%</small>
                </div>
            </div>
        `).join('');
    }

    return `
        <div class="report-section">
            <div class="section-header">
                <i class="fas fa-file"></i>
                <h3>File Information</h3>
            </div>
            <div class="metadata-grid">
                <div class="metadata-item">
                    <div class="metadata-label">Filename</div>
                    <div class="metadata-value">${data.filename}</div>
                </div>
                <div class="metadata-item">
                    <div class="metadata-label">File Size</div>
                    <div class="metadata-value">${(data.file_size / 1024).toFixed(2)} KB</div>
                </div>
                <div class="metadata-item">
                    <div class="metadata-label">File Type</div>
                    <div class="metadata-value">${data.file_type}</div>
                </div>
                <div class="metadata-item">
                    <div class="metadata-label">SHA256 Hash</div>
                    <div class="metadata-value" style="font-size: 0.7rem;">${data.file_hash}</div>
                </div>
            </div>
        </div>
        
        <div class="report-section">
            <div class="section-header">
                <i class="fas fa-robot"></i>
                <h3>Analysis Engines</h3>
            </div>
            <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
                ${data.analysis_engines.map(engine => `
                    <div style="background: rgba(255, 111, 0, 0.1); padding: 0.5rem 1rem; border-radius: 20px; border: 1px solid rgba(255, 111, 0, 0.3);">
                        <i class="fab fa-python"></i> ${engine}
                    </div>
                `).join('')}
            </div>
        </div>
        
        <div class="report-section">
            <div class="section-header">
                <i class="fas fa-exclamation-triangle"></i>
                <h3>Threat Indicators (${data.threat_indicators?.length || 0})</h3>
            </div>
            ${threatsHTML || '<p>No threat indicators detected</p>'}
        </div>
    `;
}

function generateRecommendations(data, type) {
    let recommendations = [];
    
    if (data.risk_level === 'high') {
        recommendations.push('Immediate action required - this poses significant security risk');
        recommendations.push('Do not interact with this resource');
        recommendations.push('Report to your security team immediately');
    } else if (data.risk_level === 'medium') {
        recommendations.push('Exercise caution when interacting with this resource');
        recommendations.push('Verify authenticity through alternative channels');
        recommendations.push('Monitor for any suspicious activity');
    } else {
        recommendations.push('This resource appears safe for normal use');
        recommendations.push('Continue practicing good security hygiene');
        recommendations.push('Report any suspicious activity to your security team');
    }
    
    // Type-specific recommendations
    if (type === 'url' && data.organization_context?.is_ethiopian) {
        recommendations.push('Verify through official Ethiopian organization channels');
    }
    
    if (type === 'ip' && data.ethiopian_context) {
        recommendations.push('This IP belongs to Ethiopian infrastructure - monitor for unauthorized access');
    }
    
    return recommendations.map(rec => `<li>${rec}</li>`).join('');
}

function updateThreatStats() {
    document.getElementById('totalScans').textContent = threatStats.totalScans;
    document.getElementById('threatsDetected').textContent = threatStats.threatsDetected;
    document.getElementById('ethiopianOrgs').textContent = threatStats.ethiopianOrgs;
    document.getElementById('confidenceRate').textContent = threatStats.confidenceRate;
}

function uploadFileForAnalysis(formData, container) {
    fetch('/api/v1/analysis/file', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        displayEnhancedResults('file', data, container);
        
        if (data.risk_level !== 'low') {
            threatStats.threatsDetected++;
            updateThreatStats();
        }
    })
    .catch(error => {
        console.error('File analysis error:', error);
        displayAnalysisError(error, container);
    });
}

function displayAnalysisError(error, container) {
    container.innerHTML = `
        <div class="result-item result-malicious">
            <div class="result-icon"><i class="fas fa-exclamation-triangle"></i></div>
            <div>
                <h4>Analysis Failed</h4>
                <p>Error: ${error.message || 'Unknown error occurred'}</p>
            </div>
        </div>
    `;
}

// Initialize threat statistics
document.addEventListener('DOMContentLoaded', function() {
    updateThreatStats();
});
