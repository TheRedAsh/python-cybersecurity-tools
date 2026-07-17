#!/usr/bin/env python3
"""
PhoneTracker Ultimate — Pakistan SIM Database OSINT Tool
📞 Phone Number → Name • CNIC • Address • Carrier
🆔 CNIC → All SIMs + Names + Numbers + Addresses
⚡ No API key required — 100% Free Sources
Authorized Pentesting Use Only
"""

import requests
import json
import re
import sys
from datetime import datetime

BANNER = """
╔══════════════════════════════════════════════════════════════╗
║        PhoneTracker Ultimate — PAKISTAN                      ║
║   Phone → Owner Name • CNIC • Address • Carrier • Province   ║
║                Zero API Keys Required                        ║
║               Authorized Pentesting Use Only                 ║
╚══════════════════════════════════════════════════════════════╝
"""

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
    "Accept": "application/json"
}

def fmt_number(num):
    """Normalize to 03XXXXXXXXX format"""
    num = re.sub(r'[\s\-\(\)\+]', '', num)
    if num.startswith('00'): num = num[2:]
    if num.startswith('92') and len(num) == 12: return '0' + num[2:]
    if num.startswith('3') and len(num) == 10: return '0' + num
    if num.startswith('03') and len(num) == 11: return num
    return num

def fmt_cnic(cnic):
    """Normalize CNIC to 13 digits"""
    cnic = re.sub(r'[\s\-]', '', cnic)
    return cnic if len(cnic) == 13 else None

def detect_carrier(number):
    """Detect carrier from prefix"""
    clean = fmt_number(number)
    prefix = clean[1:3] if len(clean) >= 3 else ""
    carriers = {
        "30":"Jazz","31":"Jazz","32":"Jazz","33":"Jazz","34":"Jazz",
        "35":"Jazz","36":"Jazz","37":"Jazz","38":"Jazz","39":"Jazz",
        "40":"Telenor","41":"Telenor","42":"Telenor","43":"Telenor",
        "44":"Telenor","45":"Telenor","46":"Telenor","47":"Telenor",
        "48":"Telenor","49":"Telenor",
        "50":"Zong","51":"Zong","52":"Zong","53":"Zong","54":"Zong",
        "55":"Zong","56":"Zong","57":"Zong","58":"Zong","59":"Zong",
        "60":"Ufone","61":"Ufone","62":"Ufone","63":"Ufone","64":"Ufone",
        "65":"Ufone","66":"Ufone","67":"Ufone","68":"Ufone","69":"Ufone"
    }
    return carriers.get(prefix, "PTCL/SCOM/Landline")

def get_province(cnic):
    """Detect province from CNIC first digit"""
    c = str(cnic)[0] if cnic else ""
    return {
        "1": "Khyber Pakhtunkhwa", "2": "Punjab (Rawalpindi)",
        "3": "Punjab (Sargodha)", "4": "Punjab (Faisalabad)",
        "5": "Punjab (Lahore)", "6": "Punjab (Gujranwala)",
        "7": "Punjab (Multan)", "8": "Sindh (Sukkur/Larkana)",
        "9": "Sindh (Karachi/Hyderabad)", "0": "Balochistan/Islamabad/GB"
    }.get(c, "Unknown")

# ═══════════════════════════════════════════════════════════════
# SOURCE 1: adeel.app — FREE, No API Key Required
# Returns: Name, CNIC, Address, Mobile
# ═══════════════════════════════════════════════════════════════

def source_adeel_phone(number):
    """Lookup phone number on adeel.app — returns Name, CNIC, Address"""
    clean = fmt_number(number)
    # adeel.app expects format without 0 prefix
    search = clean[1:] if clean.startswith('0') else clean
    
    try:
        url = f"https://adeel.app/api/search?phone={search}"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        
        if resp.status_code == 200:
            data = resp.json()
            if data.get("success") and data.get("data"):
                return data["data"]
            return None
        return None
    except Exception as e:
        return {"error": str(e)}

def source_adeel_cnic(cnic):
    """Lookup CNIC on adeel.app — returns all SIMs registered"""
    try:
        url = f"https://adeel.app/api/search?cnic={cnic}"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        
        if resp.status_code == 200:
            data = resp.json()
            if data.get("success") and data.get("data"):
                return data
            return None
        return None
    except Exception as e:
        return {"error": str(e)}

# ═══════════════════════════════════════════════════════════════
# SOURCE 2: sychosimdatabase.vercel.app — Free, sometimes works
# ═══════════════════════════════════════════════════════════════

def source_sycho(query):
    """Try Syco SIM database"""
    try:
        url = f"https://sychosimdatabase.vercel.app/api/lookup/{query}"
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            return resp.json()
        return None
    except:
        return None

# ═══════════════════════════════════════════════════════════════
# SOURCE 3: Web Scraping from free SIM lookup sites
# ═══════════════════════════════════════════════════════════════

def source_web_scrape(number):
    """Try multiple free Pakistan SIM lookup sites"""
    clean = fmt_number(number)
    search = clean[1:] if clean.startswith('0') else clean
    
    urls = [
        f"https://simtrackings.com/search?number={search}",
        f"https://simdataupdates.com/api?number={search}",
    ]
    
    results = {}
    for url in urls:
        try:
            resp = requests.get(url, headers=HEADERS, timeout=10)
            if resp.status_code == 200:
                try:
                    results[url.split('/')[2]] = resp.json()
                except:
                    results[url.split('/')[2]] = resp.text[:300]
        except:
            pass
    
    return results if results else None

# ═══════════════════════════════════════════════════════════════
# GENERATE GOOGLE DORKS
# ═══════════════════════════════════════════════════════════════

def google_dorks(number, name=None, cnic=None):
    """Generate Pakistan-specific OSINT search queries"""
    clean = fmt_number(number)
    search = clean[1:] if clean.startswith('0') else clean
    dorks = []
    
    dorks.append(f'site:facebook.com "{search}"')
    dorks.append(f'site:instagram.com "{search}"')
    dorks.append(f'site:twitter.com "{search}"')
    dorks.append(f'site:linkedin.com "{search}"')
    dorks.append(f'site:olx.com.pk "{search}"')
    dorks.append(f'site:zameen.com "{search}"')
    dorks.append(f'site:pakwheels.com "{search}"')
    dorks.append(f'site:daraz.pk "{search}"')
    dorks.append(f'site:foodpanda.pk "{search}"')
    dorks.append(f'site:whatsapp.com "{search}"')
    
    if name:
        name_part = name.split()[0] if name.split() else name
        dorks.append(f'"{name_part}" "{search}"')
    
    if cnic:
        dorks.append(f'"{cnic}" Pakistan')
        dorks.append(f'site:facebook.com "{cnic}"')
    
    return dorks

# ═══════════════════════════════════════════════════════════════
# DISPLAY HELPERS
# ═══════════════════════════════════════════════════════════════

def section(title):
    print(f"\n{'═'*55}")
    print(f"   📌 {title}")
    print(f"{'═'*55}")

def show(data, indent=""):
    if isinstance(data, dict):
        for k, v in data.items():
            if v and str(v).strip() and v not in ["N/A", "", "None"]:
                print(f"{indent}   • {k}: {v}")
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                for k, v in item.items():
                    if v and str(v).strip():
                        print(f"{indent}   • {k}: {v}")
                print(f"{indent}   {'—'*30}")
            else:
                print(f"{indent}   • {item}")
    elif data:
        print(f"{indent}   {data}")

# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    print(BANNER)
    
    print("   [1] Phone Number → Name • CNIC • Address")
    print("   [2] CNIC → All Registered SIMs")
    print()
    choice = input("   [?] Select (1/2): ").strip()
    
    all_data = {"timestamp": datetime.now().isoformat()}
    
    # ─── PHONE NUMBER LOOKUP ───
    if choice == "1":
        number = input("   [?] Enter Pakistani mobile number (03XXXXXXXXX): ").strip()
        query = fmt_number(number)
        
        if not re.match(r'^03\d{9}$', query):
            print("   [!] Invalid. Use format: 03XXXXXXXXX")
            return
        
        carrier = detect_carrier(query)
        print(f"\n   [ℹ] Number: {query} | Carrier: {carrier}")
        all_data["query"] = query
        all_data["carrier"] = carrier
        
        # SOURCE 1: adeel.app (Name + CNIC + Address)
        section("Source 1: adeel.app [Name + CNIC + Address]")
        print("   [*] Querying free API (no key required)...")
        
        result1 = source_adeel_phone(query)
        all_data["adeel_app"] = result1
        
        if result1 and "error" not in result1:
            # SAFETY FIX: Parse checks if response returned is a list or dictionary
            if isinstance(result1, list):
                result_data = result1[0] if len(result1) > 0 and isinstance(result1[0], dict) else {}
            else:
                result_data = result1 if isinstance(result1, dict) else {}

            name = result_data.get("Name") or result_data.get("name", "N/A")
            cnic = result_data.get("CNIC") or result_data.get("cnic", "N/A")
            addr = result_data.get("ADDRESS") or result_data.get("address", "N/A")
            mob = result_data.get("Mobile") or result_data.get("mobile", "N/A")
            
            print(f"\n   ✅ PERSON DETAILS FOUND!")
            print(f"\n   {'—'*35}")
            print(f"   👤 Name:    {name}")
            print(f"   🆔 CNIC:    {cnic}")
            print(f"   📍 Address: {addr}")
            print(f"   📱 Mobile:  {mob}")
            print(f"   🏢 Carrier: {carrier}")
            print(f"   {'—'*35}")
            
            if cnic and cnic != "N/A":
                cnic_clean = re.sub(r'\D', '', str(cnic))
                if len(cnic_clean) >= 1:
                    province = get_province(cnic_clean)
                    print(f"   🗺️ Province: {province}")
            
            all_data["name"] = name
            all_data["cnic"] = cnic
            all_data["address"] = addr
            
            # Google dorks with name
            section("OSINT Google Dorks")
            dorks = google_dorks(query, name, cnic)
            all_data["google_dorks"] = dorks
            for i, d in enumerate(dorks, 1):
                print(f"   {i:2d}. {d}")
        else:
            print("   [✗] No data from adeel.app")
        
        # SOURCE 2: Syco DB (backup)
        section("Source 2: sychosimdatabase (Backup)")
        result2 = source_sycho(query)
        all_data["sycho_db"] = result2
        if result2 and "error" not in result2:
            print("   [✓] Data found:")
            show(result2)
        else:
            print("   [–] No data from this source")
        
        # SOURCE 3: Web scrape
        section("Source 3: Web Scrape (Backup)")
        result3 = source_web_scrape(query)
        all_data["web_scrape"] = result3
        if result3:
            print("   [✓] Data found from web sources")
            for src, data in result3.items():
                print(f"\n   [{src}]:")
                show(data)
        else:
            print("   [–] No data from web scraping")
    
    # ─── CNIC LOOKUP ───
    elif choice == "2":
        cnic = input("   [?] Enter CNIC (13 digits): ").strip()
        query = fmt_cnic(cnic)
        
        if not query:
            print("   [!] Invalid CNIC. Enter 13 digits.")
            return
        
        province = get_province(query)
        print(f"\n   [ℹ] CNIC: {query[:5]}-{query[5:9]}-{query[9:]}")
        print(f"   [ℹ] Province: {province}")
        all_data["query"] = query
        all_data["province"] = province
        
        # SOURCE 1: adeel.app CNIC lookup
        section("Source 1: adeel.app [All SIMs on this CNIC]")
        print("   [*] Querying free API (no key required)...")
        
        result1 = source_adeel_cnic(query)
        all_data["adeel_app"] = result1
        
        if result1 and "error" not in result1 and result1.get("success"):
            total = result1.get("total", 0)
            sims = result1.get("data", [])
            
            # Parse safety for list object types
            if isinstance(sims, list):
                print(f"\n   ✅ {total} SIM(s) found on this CNIC!")
                print(f"   {'—'*45}")
                
                for i, sim in enumerate(sims, 1):
                    if isinstance(sim, dict):
                        print(f"\n   SIM #{i}")
                        print(f"   👤 Name:    {sim.get('Name', 'N/A')}")
                        print(f"   📱 Mobile:  0{sim.get('Mobile', 'N/A')}")
                        print(f"   📍 Address: {sim.get('ADDRESS', 'N/A')}")
                        print(f"   🏢 Carrier: {detect_carrier('0' + str(sim.get('Mobile', '')))}")
                        print(f"   {'—'*30}")
            else:
                print("   [✗] Received invalid database format from Source 1")
            
            # Google dorks for first SIM
            if isinstance(sims, list) and len(sims) > 0:
                first_sim = sims[0]
                if isinstance(first_sim, dict):
                    first_mob = first_sim.get('Mobile', '')
                    if first_mob:
                        section("OSINT Google Dorks")
                        dorks = google_dorks('0' + str(first_mob))
                        all_data["google_dorks"] = dorks
                        for i, d in enumerate(dorks, 1):
                            print(f"   {i:2d}. {d}")
        else:
            print("   [✗] No data from adeel.app")
        
        # SOURCE 2: Syco DB
        section("Source 2: sychosimdatabase (Backup)")
        result2 = source_sycho(query)
        all_data["sycho_db"] = result2
        if result2 and "error" not in result2:
            print("   [✓] Data found:")
            show(result2)
        else:
            print("   [–] No data from this source")
    
    else:
        print("   [!] Invalid option")
        return
    
    # ─── SAVE REPORT ───
    print(f"\n{'═'*55}")
    save = input("   [?] Save full report to file? (y/n): ").strip().lower()
    
    if save == 'y':
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        fname = f"PhoneTracker_{query}_{ts}.json"
        with open(fname, "w") as f:
            json.dump(all_data, f, indent=2, default=str)
        print(f"   ✅ Report saved: {fname}")
        
        # Also save readable TXT
        txtname = f"PhoneTracker_{query}_{ts}.txt"
        with open(txtname, "w") as f:
            f.write(f"PhoneTracker Ultimate - Investigation Report\n")
            f.write(f"{'='*55}\n")
            f.write(f"Query: {query}\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"{'='*55}\n\n")
            f.write(json.dumps(all_data, indent=2, default=str))
        print(f"   ✅ Text report saved: {txtname}")
    
    print(f"\n{'═'*55}")
    print("   🎯 Investigation Complete!")
    print(f"{'═'*55}")

if __name__ == "__main__":
    main()
