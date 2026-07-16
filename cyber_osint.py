# =======================================================
# TOOL: DYNAMIC CYBER OSINT IP INTELLIGENCE
# AUTHOR: Class 10 Student (Cyber Security Analyst)
# =======================================================

import urllib.request  # Public URL web requests headers access karne ke liye
import json           # Raw public JSON data structures ko dictionary format dene ke liye

# Step 1: Professional Interactive Hacking Terminal Interface
print("==================================================")
print("    🕵️‍♂️ CYBER SECURITY OSINT DETECTOR v2.0 🕵️‍♂️     ")
print("==================================================")

# Step 2: User Input Gathering (IP address request prompt)
target_ip = input("\n[?] Enter Target IP to Investigate (e.g. 8.8.8.8): ")

print(f"\n[*] Querying Public Databases for Recon Data: {target_ip}...")

# Step 3: API Request Initialization using Public Endpoint
public_url = "http://ip-api.com/json/" + target_ip

try:
    # Internet traffic channel execution
    request_flow = urllib.request.urlopen(public_url, timeout=5)
    raw_response = request_flow.read().decode('utf-8')
    
    # Text strings ko standard Python data format me dump karna
    data_cluster = json.loads(raw_response)
    
    # Conditional logic output handling
    if data_cluster.get("status") == "success":
        print("\n[+] 📊 ----------- OSINT INTELLIGENCE REPORT -----------")
        print("[+] Targeted Country  : " + data_cluster.get("country", "N/A"))
        print("[+] Country Code      : " + data_cluster.get("countryCode", "N/A"))
        print("[+] Region / State    : " + data_cluster.get("regionName", "N/A"))
        print("[+] City Location     : " + data_cluster.get("city", "N/A"))
        print("[+] ZIP Code          : " + data_cluster.get("zip", "N/A"))
        print("[+] Latitude Coordinate: " + str(data_cluster.get("lat", "N/A")))
        print("[+] Longitude Coords  : " + str(data_cluster.get("lon", "N/A")))
        print("[+] Network ISP Owner : " + data_cluster.get("isp", "N/A"))
        print("[+] Organization Name : " + data_cluster.get("org", "N/A"))
        print("[+] Autonomous System : " + data_cluster.get("as", "N/A"))
        print("-------------------------------------------------------")
        print("[!] Status: Footprinting Analysis Complete! 🔥")
    else:
        print("\n[-] DATA ERROR: Provided target parameter is not a public IP route.")
        print("[-] Server Message: " + data_cluster.get("message", "Unknown Fail"))

except Exception as network_fault:
    print(f"\n[!] Network Failure Exception Triggered: {network_fault}")
    print("[!] Action Required: Verify internet connection routing on Kali Linux.")
