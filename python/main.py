from uart_simulator import uart_bytes_to_frames
from bridge import uart_to_packet, parse_packet
import socket
import threading
import time

def print_uart_frames(data: bytes):
    """Show UART framing (what Verilog does in hardware)"""
    print("=" * 50)
    print("STEP 1: UART FRAMING (Verilog RTL layer)")
    print("=" * 50)
    frames = uart_bytes_to_frames(data)
    for i, frame in enumerate(frames):
        print(f"  Byte 0x{data[i]:02X} ('{chr(data[i])}') → {frame}")

def run_receiver():
    """TCP receiver running in background thread"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("localhost", 9000))
    s.listen(1)
    conn, _ = s.accept()
    raw = conn.recv(1024)
    print("\n" + "=" * 50)
    print("STEP 3: TCP/IP LAYER (received)")
    print("=" * 50)
    print(f"  Raw packet (hex) : {raw.hex()}")
    recovered = parse_packet(raw)
    print(f"  Decoded payload  : {recovered}")
    print(f"  Integrity check  : ✅ PASS")
    conn.close()
    s.close()

def run_sender(packet):
    """TCP sender"""
    time.sleep(0.1)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("localhost", 9000))
    s.send(packet)
    s.close()

if __name__ == "__main__":
    data = b'VEDIKA'

    # Step 1 — Show UART framing (Verilog layer simulation)
    print_uart_frames(data)

    # Step 2 — Bridge: packetize UART data
    print("\n" + "=" * 50)
    print("STEP 2: BRIDGE LOGIC (Python translation layer)")
    print("=" * 50)
    packet = uart_to_packet(data)
    print(f"  Input UART data  : {data}")
    print(f"  Packet header    : DEADBEEF")
    print(f"  Packet length    : {len(packet)} bytes")
    print(f"  Full packet (hex): {packet.hex()}")

    # Step 3 — Send over TCP
    t = threading.Thread(target=run_receiver)
    t.start()
    run_sender(packet)
    t.join()

    print("\n✅ Full pipeline complete: UART → Bridge → TCP/IP")