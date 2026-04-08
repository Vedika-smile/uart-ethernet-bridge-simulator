import struct

def uart_to_packet(uart_data: bytes):
    """
    Packetizes UART data into custom Ethernet-like frame
    Packet structure:
    | Header (4B) | Length (2B) | Payload | Checksum (1B) |
    """
    HEADER = b'\xDE\xAD\xBE\xEF'
    length = struct.pack('>H', len(uart_data))
    checksum = sum(uart_data) % 256
    packet = HEADER + length + uart_data + bytes([checksum])
    return packet

def parse_packet(packet: bytes):
    """Parse received packet back into UART data"""
    HEADER = b'\xDE\xAD\xBE\xEF'
    assert packet[:4] == HEADER, "Invalid header!"
    length = struct.unpack('>H', packet[4:6])[0]
    payload = packet[6:6+length]
    checksum = packet[6+length]
    assert sum(payload) % 256 == checksum, "Checksum mismatch!"
    return payload

if __name__ == "__main__":
    # Test the bridge
    original = b'VEDIKA'
    packet = uart_to_packet(original)
    print("Packet (hex):", packet.hex())
    recovered = parse_packet(packet)
    print("Recovered data:", recovered)
    print("Integrity check:", original == recovered)