#!/usr/bin/env python3
import socket
import requests
import json
import ipaddress
import subprocess
import os  # Tambahan untuk clear terminal

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def whois_lookup(ip):
    try:
        result = subprocess.check_output(["whois", ip], stderr=subprocess.DEVNULL, text=True)
        return result
    except Exception as e:
        return f"WHOIS Error: {e}"

def geoip_lookup(ip):
    try:
        response = requests.get(f"http://ipinfo.io/{ip}/json", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "GeoIP lookup failed"}
    except Exception as e:
        return {"error": str(e)}

def scan_ports(ip, ports=[21,22,23,25,53,80,110,143,443,3306,8080]):
    open_ports = []
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
            sock.close()
        except:
            pass
    return open_ports

if __name__ == "__main__":
    clear_screen()  # Clear terminal sebelum input
    ip_target = input("Input IP Target: ").strip()

    try:
        ipaddress.ip_address(ip_target)
    except ValueError:
        print("IP tidak valid!")
        exit()

    print(f"\n[+] Mapping IP: {ip_target}\n")

    # WHOIS
    whois_info = whois_lookup(ip_target)
    print("=== WHOIS ===")
    print(whois_info)

    # GEOIP
    geo_info = geoip_lookup(ip_target)
    print("\n=== GEOIP ===")
    print(json.dumps(geo_info, indent=2))

    # PORT SCAN
    ports = scan_ports(ip_target)
    print("\n=== OPEN PORTS ===")
    if ports:
        print(", ".join(map(str, ports)))
    else:
        print("No Open Ports Detected.")

    # Simpan ke file
    with open("hasil_mapping.txt", "w") as f:
        f.write(f"IP: {ip_target}\n\n")
        f.write("=== WHOIS ===\n")
        f.write(whois_info + "\n\n")
        f.write("=== GEOIP ===\n")
        f.write(json.dumps(geo_info, indent=2) + "\n\n")
        f.write("=== OPEN PORTS ===\n")
        f.write(", ".join(map(str, ports)) if ports else "No Open Ports\n")

    print("\n[+] Result saved in 'result_mapping.txt'")
