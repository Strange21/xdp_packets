# import socket
# import os
# import time

# if __name__ == "__main__":
#     socket_path = "/home/nuc2kor/Desktop/ipc_new.sock"

#     try:
#         os.unlink(socket_path)
#     except OSError:
#         pass

#     s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
#     s.bind(socket_path)

#     s.listen()
#     result_list = []
    
#     start_time = time.time()  # Record start time
#     packet_count = 0  # Initialize packet count
    
#     while True:
#         conn, addr = s.accept()
#         try:
#             while True:
#                 data = conn.recv(25)
#                 if data:
#                     result_list.append(data)
#                     packet_count += 1  # Increment packet count for each received packet
#                     print("Received:", data)
                    
#                     # Calculate elapsed time
#                     elapsed_time = time.time() - start_time
                    
#                     # Calculate packets per second (rate)
#                     if elapsed_time > 0:
#                         packets_per_second = packet_count / elapsed_time
#                         print(f"Packets per second: {packets_per_second:.2f}")
#         finally:
#             conn.close()

import socket
import os
import time
import matplotlib.pyplot as plt
from collections import deque

if __name__ == "__main__":
    socket_path = "/home/nuc2kor/Desktop/ipc_new.sock"

    try:
        os.unlink(socket_path)
    except OSError:
        pass

    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.bind(socket_path)

    s.listen()
    # result_list = []

    # Variables for tracking packets per second
    start_time = time.time()
    packet_count = 0
    time_values = deque()  # Queue to store time values (x-axis)
    packet_rates = deque()  # Queue to store packet rates (y-axis)

    # Set up matplotlib figure and axis
    plt.figure()
    plt.xlabel("Time (seconds)")
    plt.ylabel("Packets per Second")

    try:
        while True:
            conn, addr = s.accept()
            try:
                while True:
                    data = conn.recv(25)
                    if data:
                        # result_list.append(data)
                        packet_count += 1
                        # print("Received:", data)

                        # Calculate elapsed time
                        elapsed_time = time.time() - start_time

                        # Calculate packets per second (rate)
                        if elapsed_time > 0:
                            packets_per_second = packet_count / elapsed_time

                            # Append data points to queues
                            time_values.append(elapsed_time)
                            packet_rates.append(packets_per_second)

                            # Update plot with new data points
                            plt.plot(time_values, packet_rates, color='b')
                            plt.draw()
                            plt.pause(0.001)  # Small pause to allow plot to update
            finally:
                conn.close()

    except KeyboardInterrupt:
        # Handle keyboard interrupt (Ctrl+C)
        print("Plotting stopped by user.")
        plt.show()  # Display final plot when program is terminated

