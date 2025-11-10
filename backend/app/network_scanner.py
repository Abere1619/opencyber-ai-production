"""
Network Scanner Module for AbEthiopia Cyber Intelligence Platform
"""

import subprocess
import socket
from typing import Dict, List, Any

class NetworkScanner:
    def __init__(self):
        self.common_ports = [21, 22, 23, 25, 53, 80, 110, 443, 993, 995, 1433, 3306, 3389, 5432, 8000, 8080, 8443, 9000, 3000]
    
    def scan_ip(self, ip_address: str) -> Dict[str, Any]:
        try:
            socket.inet_aton(ip_address)
            
            scan_results = {
                "ip": ip_address,
                "reachable": self.check_reachability(ip_address),
                "open_ports": self.scan_ports(ip_address),
                "hostname": self.reverse_dns_lookup(ip_address),
                "network_info": self.get_network_info(ip_address)
            }
            
            return scan_results
            
        except socket.error:
            return {"error": "Invalid IP address"}
    
    def check_reachability(self, ip: str) -> bool:
        try:
            result = subprocess.run(
                ["ping", "-c", "2", "-W", "1", ip],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except:
            return False
    
    def scan_ports(self, ip: str) -> List[Dict[str, Any]]:
        open_ports = []
        for port in self.common_ports:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(1)
                    result = sock.connect_ex((ip, port))
                    if result == 0:
                        service = self.get_service_name(port)
                        open_ports.append({
                            "port": port,
                            "service": service,
                            "status": "open"
                        })
            except:
                continue
        return open_ports
    
    def get_service_name(self, port: int) -> str:
        service_map = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
            80: "HTTP", 110: "POP3", 443: "HTTPS", 993: "IMAPS", 995: "POP3S",
            1433: "MSSQL", 3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL",
            8000: "HTTP-Alt", 8080: "HTTP-Proxy", 8443: "HTTPS-Alt", 
            9000: "Jenkins", 3000: "Node.js"
        }
        return service_map.get(port, "Unknown")
    
    def reverse_dns_lookup(self, ip: str) -> str:
        try:
            return socket.gethostbyaddr(ip)[0]
        except:
            return "Unknown"
    
    def get_network_info(self, ip: str) -> Dict[str, str]:
        octets = ip.split('.')
        first_octet = int(octets[0])
        
        if first_octet == 10:
            return {"type": "Private", "range": "10.0.0.0/8"}
        elif first_octet == 172 and 16 <= int(octets[1]) <= 31:
            return {"type": "Private", "range": "172.16.0.0/12"}
        elif first_octet == 192 and int(octets[1]) == 168:
            return {"type": "Private", "range": "192.168.0.0/16"}
        else:
            return {"type": "Public", "range": "Internet"}
