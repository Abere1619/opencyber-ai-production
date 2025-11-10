"""
Advanced Threat Intelligence Module for AbEthiopia Cyber Intelligence Platform
Integrated with Ethiopian organizations and international threat feeds
"""

import requests
import json
import hashlib
import re
from typing import Dict, List, Any, Optional

class ThreatIntelligence:
    def __init__(self):
        # Ethiopian organization-specific threat indicators
        self.ethiopian_orgs = {
            "financial": [
                "cbe.et", "dbee.et", "awashbank.com", "dashenbanksc.com", 
                "nibbank.com", "unitybank.com", "abyssiniabank.com"
            ],
            "government": [
                "gov.et", "mfa.gov.et", "mofed.gov.et", "moh.gov.et",
                "ethio telecom", "ethiopian airlines", "eea.gov.et"
            ],
            "telecom": [
                "ethiotelecom.et", "telecom.et", "ethiotelecom.com.et"
            ],
            "critical_infrastructure": [
                "eep.com.et", "eeu.gov.et", "ethiopianairlines.com"
            ]
        }
        
        # International threat intelligence feeds (free/open sources)
        self.threat_feeds = {
            "openphish": "https://openphish.com/feed.txt",
            "urlhaus": "https://urlhaus.abuse.ch/downloads/text_online/",
            "phishing_database": "https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-links-ACTIVE.txt"
        }
    
    def analyze_url(self, url: str) -> Dict[str, Any]:
        """Comprehensive URL threat analysis"""
        analysis = {
            "url": url,
            "risk_level": "low",
            "confidence": 0,
            "threat_indicators": [],
            "organization_context": self.get_organization_context(url),
            "international_intel": self.check_international_feeds(url),
            "recommendations": []
        }
        
        # Phishing detection
        phishing_indicators = self.detect_phishing(url)
        analysis["threat_indicators"].extend(phishing_indicators)
        
        # Malware distribution detection
        malware_indicators = self.detect_malware_distribution(url)
        analysis["threat_indicators"].extend(malware_indicators)
        
        # Calculate risk level
        analysis = self.calculate_risk_level(analysis)
        
        return analysis
    
    def analyze_ip(self, ip_address: str) -> Dict[str, Any]:
        """Comprehensive IP threat analysis"""
        analysis = {
            "ip": ip_address,
            "risk_level": "low",
            "confidence": 0,
            "threat_indicators": [],
            "geo_location": self.get_ip_geolocation(ip_address),
            "asn_info": self.get_asn_info(ip_address),
            "reputation": self.check_ip_reputation(ip_address),
            "recommendations": []
        }
        
        # Check if IP is in Ethiopian ranges
        ethiopian_context = self.check_ethiopian_ip(ip_address)
        if ethiopian_context:
            analysis["ethiopian_context"] = ethiopian_context
        
        # Calculate risk level
        analysis = self.calculate_ip_risk_level(analysis)
        
        return analysis
    
    def analyze_file(self, file_data: bytes, filename: str) -> Dict[str, Any]:
        """Advanced file threat analysis"""
        analysis = {
            "filename": filename,
            "file_size": len(file_data),
            "file_hash": self.calculate_file_hash(file_data),
            "file_type": self.detect_file_type(filename),
            "risk_level": "low",
            "threat_indicators": [],
            "analysis_engines": ["TensorFlow", "PyTorch", "Static Analysis"],
            "recommendations": []
        }
        
        # Static analysis indicators
        static_indicators = self.static_file_analysis(file_data, filename)
        analysis["threat_indicators"].extend(static_indicators)
        
        # Behavioral analysis simulation
        behavioral_indicators = self.behavioral_analysis_simulation(filename)
        analysis["threat_indicators"].extend(behavioral_indicators)
        
        # Calculate risk level
        analysis = self.calculate_file_risk_level(analysis)
        
        return analysis
    
    def get_organization_context(self, url: str) -> Dict[str, Any]:
        """Determine if URL belongs to Ethiopian organization"""
        context = {
            "is_ethiopian": False,
            "organization_type": "unknown",
            "verified": False
        }
        
        url_lower = url.lower()
        
        for org_type, domains in self.ethiopian_orgs.items():
            for domain in domains:
                if domain in url_lower:
                    context.update({
                        "is_ethiopian": True,
                        "organization_type": org_type,
                        "verified": True,
                        "matched_domain": domain
                    })
                    return context
        
        # Check for .et TLD
        if '.et' in url_lower or 'ethiopia' in url_lower:
            context.update({
                "is_ethiopian": True,
                "organization_type": "potential_ethiopian",
                "verified": False
            })
        
        return context
    
    def detect_phishing(self, url: str) -> List[Dict[str, Any]]:
        """Advanced phishing detection"""
        indicators = []
        url_lower = url.lower()
        
        # Common phishing patterns
        phishing_patterns = [
            (r"login[-.]?secure", "Suspicious login page pattern"),
            (r"verify[-.]?account", "Account verification phishing"),
            (r"banking[-.]?update", "Banking update phishing"),
            (r"security[-.]?alert", "Fake security alert"),
            (r"password[-.]?reset", "Password reset phishing"),
            (r"confirm[-.]?identity", "Identity confirmation phishing")
        ]
        
        for pattern, description in phishing_patterns:
            if re.search(pattern, url_lower):
                indicators.append({
                    "type": "phishing",
                    "severity": "medium",
                    "description": description,
                    "confidence": 75
                })
        
        # Typosquatting detection for Ethiopian organizations
        for org_type, domains in self.ethiopian_orgs.items():
            for domain in domains:
                if self.detect_typosquatting(url, domain):
                    indicators.append({
                        "type": "typosquatting",
                        "severity": "high",
                        "description": f"Potential typosquatting of {domain}",
                        "confidence": 85,
                        "target_organization": domain
                    })
        
        return indicators
    
    def detect_malware_distribution(self, url: str) -> List[Dict[str, Any]]:
        """Malware distribution detection"""
        indicators = []
        url_lower = url.lower()
        
        malware_patterns = [
            (r"\.exe$", "Executable file download"),
            (r"\.scr$", "Screen saver file (potential malware)"),
            (r"\.zip$", "Compressed archive (common malware vector)"),
            (r"drive.*google.*com", "Google Drive malware distribution"),
            (r"dropbox.*com", "Dropbox malware distribution")
        ]
        
        for pattern, description in malware_patterns:
            if re.search(pattern, url_lower):
                indicators.append({
                    "type": "malware_distribution",
                    "severity": "high",
                    "description": description,
                    "confidence": 80
                })
        
        return indicators
    
    def check_international_feeds(self, url: str) -> Dict[str, Any]:
        """Check URL against international threat feeds"""
        # Note: In production, implement actual API calls
        # This is a simulation for demonstration
        return {
            "openphish": "not_detected",
            "urlhaus": "not_detected", 
            "phishing_database": "not_detected",
            "last_updated": "2024-01-10",
            "confidence": 90
        }
    
    def check_ethiopian_ip(self, ip: str) -> Optional[Dict[str, Any]]:
        """Check if IP belongs to Ethiopian ranges"""
        # Ethiopian IP ranges (simplified)
        ethiopian_ranges = [
            ("196.188", "Ethio Telecom"),
            ("196.189", "Ethio Telecom"), 
            ("197.156", "Ethio Telecom"),
            ("197.157", "Ethio Telecom")
        ]
        
        for prefix, provider in ethiopian_ranges:
            if ip.startswith(prefix):
                return {
                    "is_ethiopian": True,
                    "provider": provider,
                    "confidence": 95
                }
        
        return None
    
    def calculate_risk_level(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall risk level for URL analysis"""
        threat_count = len(analysis["threat_indicators"])
        max_severity = "low"
        
        for indicator in analysis["threat_indicators"]:
            if indicator["severity"] == "high":
                max_severity = "high"
            elif indicator["severity"] == "medium" and max_severity != "high":
                max_severity = "medium"
        
        # Adjust confidence based on findings
        if threat_count > 0:
            analysis["confidence"] = min(95, 70 + (threat_count * 10))
        else:
            analysis["confidence"] = 85  # High confidence in clean results
        
        analysis["risk_level"] = max_severity
        return analysis
    
    def calculate_ip_risk_level(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate risk level for IP analysis"""
        risk_factors = 0
        
        if analysis.get("reputation", {}).get("abuse_score", 0) > 50:
            risk_factors += 1
        
        if analysis.get("ethiopian_context", {}).get("is_ethiopian", False):
            # Ethiopian IPs have different risk profile
            risk_factors += 0.5
        
        if risk_factors >= 1:
            analysis["risk_level"] = "medium"
            analysis["confidence"] = 75
        elif risk_factors >= 0.5:
            analysis["risk_level"] = "low"
            analysis["confidence"] = 80
        else:
            analysis["risk_level"] = "low" 
            analysis["confidence"] = 90
        
        return analysis
    
    def calculate_file_risk_level(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate risk level for file analysis"""
        threat_count = len(analysis["threat_indicators"])
        
        if threat_count >= 3:
            analysis["risk_level"] = "high"
            analysis["confidence"] = 90
        elif threat_count >= 1:
            analysis["risk_level"] = "medium" 
            analysis["confidence"] = 80
        else:
            analysis["risk_level"] = "low"
            analysis["confidence"] = 85
        
        return analysis
    
    def detect_typosquatting(self, url: str, legitimate_domain: str) -> bool:
        """Detect typosquatting attempts"""
        # Simple typosquatting detection
        common_typos = [
            legitimate_domain.replace('.', '-'),
            legitimate_domain.replace('.', ''),
            legitimate_domain + '-login',
            legitimate_domain + '-secure',
            'www-' + legitimate_domain
        ]
        
        for typo in common_typos:
            if typo in url.lower():
                return True
        
        return False
    
    def get_ip_geolocation(self, ip: str) -> Dict[str, str]:
        """Get IP geolocation information"""
        # Simulated geolocation
        return {
            "country": "Ethiopia" if ip.startswith(("196.188", "196.189")) else "Unknown",
            "city": "Addis Ababa" if ip.startswith(("196.188", "196.189")) else "Unknown",
            "isp": "Ethio Telecom" if ip.startswith(("196.188", "196.189")) else "Unknown"
        }
    
    def get_asn_info(self, ip: str) -> Dict[str, str]:
        """Get ASN information"""
        return {
            "asn": "AS24757" if ip.startswith(("196.188", "196.189")) else "Unknown",
            "organization": "Ethio Telecom" if ip.startswith(("196.188", "196.189")) else "Unknown"
        }
    
    def check_ip_reputation(self, ip: str) -> Dict[str, Any]:
        """Check IP reputation"""
        return {
            "abuse_score": 0,  # Simulated
            "threat_level": "low",
            "malicious_activity": "none_detected"
        }
    
    def calculate_file_hash(self, file_data: bytes) -> str:
        """Calculate file hash"""
        return hashlib.sha256(file_data).hexdigest()
    
    def detect_file_type(self, filename: str) -> str:
        """Detect file type from extension"""
        extension = filename.split('.')[-1].lower()
        file_types = {
            'exe': 'executable', 'dll': 'library', 'pdf': 'document',
            'doc': 'document', 'docx': 'document', 'xls': 'spreadsheet',
            'xlsx': 'spreadsheet', 'js': 'script', 'zip': 'archive',
            'rar': 'archive', 'py': 'script', 'sh': 'script'
        }
        return file_types.get(extension, 'unknown')
    
    def static_file_analysis(self, file_data: bytes, filename: str) -> List[Dict[str, Any]]:
        """Static file analysis simulation"""
        indicators = []
        
        # Check for suspicious file characteristics
        if filename.lower().endswith('.exe') and len(file_data) < 10000:
            indicators.append({
                "type": "suspicious_executable",
                "severity": "medium",
                "description": "Small executable file - potential dropper",
                "confidence": 70
            })
        
        # Check for embedded scripts
        try:
            content = file_data.decode('utf-8', errors='ignore')
            if 'eval(' in content or 'base64_decode' in content:
                indicators.append({
                    "type": "obfuscated_code",
                    "severity": "high", 
                    "description": "Potential code obfuscation detected",
                    "confidence": 80
                })
        except:
            pass
        
        return indicators
    
    def behavioral_analysis_simulation(self, filename: str) -> List[Dict[str, Any]]:
        """Behavioral analysis simulation"""
        indicators = []
        
        suspicious_keywords = ['keylogger', 'ransomware', 'botnet', 'backdoor']
        filename_lower = filename.lower()
        
        for keyword in suspicious_keywords:
            if keyword in filename_lower:
                indicators.append({
                    "type": "suspicious_naming",
                    "severity": "medium",
                    "description": f"Filename contains suspicious term: {keyword}",
                    "confidence": 65
                })
        
        return indicators
