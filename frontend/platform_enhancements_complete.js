// Enhanced Platform Features - Complete Version
const platformEnhancements = {
    version: "2.0.0",
    features: [
        "Enhanced URL Analysis with Ethiopian Organizational Context",
        "Advanced IP Analysis with Ethiopian Network Intelligence", 
        "Multi-engine File Analysis with AI Detection",
        "Threat Intelligence Dashboard with Statistics",
        "International Threat Feed Integration",
        "Ethiopian Organization Protection",
        "Safe Testing with Open-Source Detection Engines"
    ],
    ethiopianOrganizations: {
        financial: "Commercial Bank of Ethiopia, Dashen Bank, Awash Bank",
        government: "Federal Government, Ministry of Foreign Affairs", 
        telecom: "Ethio Telecom",
        infrastructure: "Ethiopian Airlines, Ethiopian Electric Power"
    },
    aiEngines: ["TensorFlow", "PyTorch", "OpenCTI", "Static Analysis"],
    status: "operational"
};

// Initialize enhanced platform
function initializeEnhancedPlatform() {
    console.log("🛡️ AbEthiopia Cyber Intelligence Platform v2.0 Initialized");
    console.log("🌍 International Standards + 🇪🇹 Ethiopian Focus");
    
    // Update UI with enhanced features
    updatePlatformUI();
}

function updatePlatformUI() {
    // Add enhanced feature indicators to the interface
    const featureList = document.querySelector('.platform-features');
    if (featureList) {
        featureList.innerHTML = platformEnhancements.features.map(feature => 
            '<li>✅ ' + feature + '</li>'
        ).join('');
    }
    
    // Update platform version in footer
    const footer = document.querySelector('footer');
    if (footer) {
        const versionElement = document.createElement('div');
        versionElement.style.marginTop = '1rem';
        versionElement.style.color = '#a0aec0';
        versionElement.innerHTML = 'Platform v' + platformEnhancements.version + ' | Enterprise Threat Intelligence';
        footer.appendChild(versionElement);
    }
}

// Enhanced analysis function with Ethiopian context
function performEnhancedAnalysis(type, target) {
    const analysisContext = {
        timestamp: new Date().toISOString(),
        analysisType: type,
        target: target,
        ethiopianContext: checkEthiopianContext(target),
        internationalStandards: true,
        aiEngines: platformEnhancements.aiEngines
    };
    
    console.log('Enhanced Analysis Context:', analysisContext);
    return analysisContext;
}

function checkEthiopianContext(target) {
    const ethiopianIndicators = [
        '.et', 'ethiopia', 'cbe', 'dashen', 'awash', 'ethiotelecom',
        'ethiopianairlines', 'gov.et', 'com.et'
    ];
    
    const targetLower = target.toLowerCase();
    const matches = ethiopianIndicators.filter(function(indicator) {
        return targetLower.includes(indicator);
    });
    
    return {
        isEthiopian: matches.length > 0,
        matchedIndicators: matches,
        organizationType: determineOrganizationType(matches)
    };
}

function determineOrganizationType(indicators) {
    if (indicators.includes('cbe') || indicators.includes('dashen') || indicators.includes('awash')) {
        return 'financial';
    } else if (indicators.includes('gov.et') || indicators.includes('.et')) {
        return 'government';
    } else if (indicators.includes('ethiotelecom')) {
        return 'telecom';
    } else if (indicators.includes('ethiopianairlines')) {
        return 'infrastructure';
    }
    return 'unknown';
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    initializeEnhancedPlatform();
});
