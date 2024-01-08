import threading
import time
import matplotlib.pyplot as plt
from datetime import datetime

# Lock for thread-safe printing
print_lock = threading.Lock()

def run_registry():
    # Run registry.py logic here
    start_time = datetime.now()
    # Simulate registry initialization
    time.sleep(5)
    end_time = datetime.now()

    with print_lock:
        print(f"Registry Initialization Time: {(end_time - start_time).total_seconds():.2f} seconds")

def read_registry_log(connection_times, index, start_time):
    # Simplified log parsing logic
    log_file_path = 'registry.log'
    
    with open(log_file_path, 'r') as log_file:
        for line in log_file:
            if "Connection from: " in line:
                timestamp_str = line.split(" at time of ")[1].strip()
                timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")
                connection_time = abs((timestamp - start_time).total_seconds())
                
                with print_lock:
                    print(f"Peer {index} Connection Time: {connection_time:.2f} seconds at {timestamp}")

                connection_times.append((timestamp, connection_time))
                return

def run_peer(index, connection_times):
    start_time = datetime.now()
    # Run peer.py logic here
    # Simulate peer connection
    time.sleep(1)

    # Simulate the log entry
    with open('registry.log', 'a') as log_file:
        log_file.write(f"Connection from: Peer{index} at time of {datetime.now()}\n")

    read_registry_log(connection_times, index, start_time)

def measure_connection_time(num_peers):
    connection_times = []

    registry_thread = threading.Thread(target=run_registry)
    registry_thread.start()

    registry_thread.join()  # Wait for registry initialization to complete

    peer_threads = []
    for i in range(num_peers):
        thread = threading.Thread(target=run_peer, args=(i, connection_times))
        peer_threads.append(thread)
        thread.start()

    for thread in peer_threads:
        thread.join()

    total_connection_time = sum(peer[1] for peer in connection_times)
    return total_connection_time

def main():
    max_num_peers = 20

    # Measure connection time for different numbers of peers
    connection_times_list = []
    for num_peers in range(1, max_num_peers + 1):
        total_connection_time = measure_connection_time(num_peers)
        connection_times_list.append((num_peers, total_connection_time))

    # Plot the results
    plt.plot([entry[0] for entry in connection_times_list], [entry[1] for entry in connection_times_list], marker='o', linestyle='-', color='b')
    plt.title('Total Connection Time vs. Number of Connected Peers')
    plt.xlabel('Number of Connected Peers')
    plt.ylabel('Total Connection Time (seconds)')
    plt.show()

if __name__ == "__main__":
    main()
