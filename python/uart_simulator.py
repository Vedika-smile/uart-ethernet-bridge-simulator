def simulate_uart_frame(data_byte):
    """Simulates UART framing: start bit + 8 data bits + stop bit"""
    frame = []
    frame.append(0)                        # start bit
    for i in range(8):
        frame.append((data_byte >> i) & 1) # data bits LSB first
    frame.append(1)                        # stop bit
    return frame

def uart_bytes_to_frames(data: bytes):
    """Convert multiple bytes into UART frames"""
    frames = []
    for byte in data:
        frames.append(simulate_uart_frame(byte))
    return frames

if __name__ == "__main__":
    test_data = b'NVIDIA'
    frames = uart_bytes_to_frames(test_data)
    for i, frame in enumerate(frames):
        print(f"Byte {test_data[i]:02X} -> UART Frame: {frame}")