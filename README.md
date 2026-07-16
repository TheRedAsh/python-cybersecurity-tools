# 🕵️‍♂️ CYBER OSINT DETECTOR v2.0 📡

A lightweight and powerful command-line interface (CLI) OSINT utility written in Python. This tool queries public threat intelligence databases to perform instant IP reconnaissance, gathering geographic footprints, network metadata, and ISP details of any target.

---

## 🔥 Key Features
- **Real-time IP Tracking:** Instantly pulls precise data from public network registries.
- **Detailed Geolocation:** Extracts Target Country, City, Latitude, and Longitude.
- **Network Profiling:** Identifies the target's active ISP (Internet Service Provider) and Organization.
- **Fail-safe Engine:** Structured with dynamic error exception handling (`try-except`) to bypass socket timeout and network dropouts.

---

## 🛠️ Installation & Setup (Kali Linux)

Open your terminal and run the following commands to clone and set up the workspace:

```bash
# 1. System packages ko update karein
sudo apt update && sudo apt install git python3 -y

# 2. Repository ko clone karein
git clone [https://github.com/TheRedAsh/python-cybersecurity-tools.git](https://github.com/TheRedAsh/python-cybersecurity-tools.git)

# 3. Repository ke folder me dakhil hon
cd python-cybersecurity-tools
