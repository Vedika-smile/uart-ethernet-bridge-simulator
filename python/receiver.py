import socket
from bridge import parse_packet

def start_receiver(host="localhost", port=9000):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    print(f"Listening on port {port}...")
    conn, addr = s.accept()
    data = conn.recv(1024)
    print("Raw packet (hex):", data.hex())
    payload = parse_packet(data)
    print("Decoded UART data:", payload)
    conn.close()

if __name__ == "__main__":
    start_receiver()