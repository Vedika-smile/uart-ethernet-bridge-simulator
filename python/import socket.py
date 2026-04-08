import socket
from bridge import uart_to_packet

def send_uart_data(data: bytes, host="localhost", port=9000):
    packet = uart_to_packet(data)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.send(packet)
    print(f"Sent {len(packet)} bytes -> {data}")
    s.close()

if __name__ == "__main__":
    send_uart_data(b'VEDIKA')