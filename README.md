# UART to Ethernet Bridge Simulator

So I had already built a UART transceiver in Verilog for one of my projects, 
and I wanted to extend it further — basically simulate what happens when serial 
data needs to be sent over a network. That's what this project does.

The idea is simple: take UART frames, wrap them into a custom TCP packet, 
send it over a socket, and verify the data came through correctly. 
Ended up adding latency measurements too just to see how it performs.

## How it works
```
UART Layer (Verilog)  →  Bridge Logic (Python)  →  TCP/IP (Python Sockets)
```

The Verilog side handles actual UART framing — start bit, 8 data bits, stop bit. 
The Python side simulates that output, packetizes it with a custom header and 
checksum, then sends it over TCP. The receiver decodes it and verifies integrity.

## Packet structure I designed
```
| Header (4B) | Length (2B) | Payload | Checksum (1B) |
  0xDEADBEEF    payload len   UART data  sum % 256
```
Used DEADBEEF as magic header since it's commonly used in debugging.

## Files
```
uart-ethernet-bridge-simulator/
├── verilog/
│   ├── uart_tx.v        
│   ├── uart_rx.v        
│   └── uart_tb.v        
├── python/
│   ├── uart_simulator.py  
│   ├── bridge.py          
│   ├── sender.py          
│   ├── receiver.py        
│   ├── main.py            
│   └── metrics.py         
├── results/
│   ├── latency_plot.png   
│   └── pipeline_output.png
└── README.md
```

## How to run

Run the full pipeline (easiest way to see everything):
```bash
python main.py
```

Just the bridge logic test:
```bash
python bridge.py
```

Sender and receiver (need 2 terminals):
```bash
# terminal 1
python receiver.py

# terminal 2  
python sender.py
```

Latency benchmark:
```bash
python metrics.py
```

## Output I got
```
STEP 1: UART FRAMING (Verilog RTL layer)
  Byte 0x56 ('V') → [0, 0, 1, 1, 0, 1, 0, 1, 0, 1]
  Byte 0x45 ('E') → [0, 1, 0, 1, 0, 0, 0, 1, 0, 1]
  Byte 0x44 ('D') → [0, 0, 0, 1, 0, 0, 0, 1, 0, 1]
  Byte 0x49 ('I') → [0, 1, 0, 0, 1, 0, 0, 1, 0, 1]
  Byte 0x4B ('K') → [0, 1, 1, 0, 1, 0, 0, 1, 0, 1]
  Byte 0x41 ('A') → [0, 1, 0, 0, 0, 0, 0, 1, 0, 1]

STEP 2: BRIDGE LOGIC (Python translation layer)
  Input UART data  : b'VEDIKA'
  Packet header    : DEADBEEF
  Packet length    : 13 bytes
  Full packet (hex): deadbeef0006564544494b41b4

STEP 3: TCP/IP LAYER (received)
  Raw packet (hex) : deadbeef0006564544494b41b4
  Decoded payload  : b'VEDIKA'
  Integrity check  : ✅ PASS

✅ Full pipeline complete: UART → Bridge → TCP/IP
```

## Latency results (20 packets)

| Metric      | Value   |
|-------------|---------|
| Avg Latency | 0.69 ms |
| Min Latency | 0.00 ms |
| Max Latency | 1.52 ms |

![Performance Metrics](results/latency_plot.png)

## What I used
- Verilog HDL + Xilinx Vivado (UART hardware side)
- Python — socket, struct, threading, matplotlib
- Tested on Windows

## What I want to add later
- support for longer payloads
- error injection to test checksum detection
- maybe try UDP and compare latency
