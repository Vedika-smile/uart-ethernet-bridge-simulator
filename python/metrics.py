import socket
import time
import struct
import matplotlib.pyplot as plt
from bridge import uart_to_packet, parse_packet

# server (receiver) running in background
def run_receiver_once(host="localhost", port=9001):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(1)
    conn, _ = s.accept()
    data = conn.recv(1024)
    conn.close()
    s.close()
    return data

#  measure latency over N packets 

def measure_latency(n=20):
    latencies = []
    packet_sizes = []

    for i in range(n):
        # vary payload each iteration
        payload = f"UART_PACKET_{i}".encode()
        packet  = uart_to_packet(payload)

        # --- receiver thread ---
        import threading
        t = threading.Thread(target=run_receiver_once)
        t.start()
        time.sleep(0.05)          # give receiver time to bind

        # --- sender ---
        start = time.time()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("localhost", 9001))
        s.send(packet)
        s.close()
        t.join()
        end = time.time()

        latency_ms = (end - start) * 1000
        latencies.append(latency_ms)
        packet_sizes.append(len(packet))
        print(f"Packet {i+1:02d} | Size: {len(packet):3d}B | "
              f"Latency: {latency_ms:.2f} ms")

    return latencies, packet_sizes

#  plot results 

def plot_results(latencies, packet_sizes):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7))
    fig.suptitle("UART to TCP Bridge — Performance Metrics", fontsize=14)

    # Latency plot
    ax1.plot(latencies, marker='o', color='steelblue', linewidth=2)
    ax1.axhline(sum(latencies)/len(latencies), color='red',
                linestyle='--', label=f"Avg: {sum(latencies)/len(latencies):.2f} ms")
    ax1.set_title("Per-Packet Latency")
    ax1.set_xlabel("Packet #")
    ax1.set_ylabel("Latency (ms)")
    ax1.legend()
    ax1.grid(True)

    # Packet size plot
    ax2.bar(range(len(packet_sizes)), packet_sizes, color='darkorange')
    ax2.set_title("Packet Size per Transmission")
    ax2.set_xlabel("Packet #")
    ax2.set_ylabel("Size (Bytes)")
    ax2.grid(True, axis='y')

    plt.tight_layout()
    plt.savefig("results/latency_plot.png")
    print("\nGraph saved to results/latency_plot.png")
    plt.show()

#  main 

if __name__ == "__main__":
    print("Running UART Bridge Metrics...\n")
    latencies, sizes = measure_latency(n=20)
    print(f"\nAvg Latency : {sum(latencies)/len(latencies):.2f} ms")
    print(f"Min Latency : {min(latencies):.2f} ms")
    print(f"Max Latency : {max(latencies):.2f} ms")
    plot_results(latencies, sizes)