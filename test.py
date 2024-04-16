# # import socket
# # import os
# # import time

# # if __name__ == "__main__":
# #     socket_path = "/home/nuc2kor/Desktop/ipc_new.sock"

# #     try:
# #         os.unlink(socket_path)
# #     except OSError:
# #         pass

# #     s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
# #     s.bind(socket_path)

# #     s.listen()
# #     result_list = []
    
# #     start_time = time.time()  # Record start time
# #     packet_count = 0  # Initialize packet count
    
# #     while True:
# #         conn, addr = s.accept()
# #         try:
# #             while True:
# #                 data = conn.recv(25)
# #                 if data:
# #                     result_list.append(data)
# #                     packet_count += 1  # Increment packet count for each received packet
# #                     print("Received:", data)
                    
# #                     # Calculate elapsed time
# #                     elapsed_time = time.time() - start_time
                    
# #                     # Calculate packets per second (rate)
# #                     if elapsed_time > 0:
# #                         packets_per_second = packet_count / elapsed_time
# #                         print(f"Packets per second: {packets_per_second:.2f}")
# #         finally:
# #             conn.close()

# import socket
# import os
# import time
# import matplotlib.pyplot as plt
# from collections import deque

# if __name__ == "__main__":
#     socket_path = "/home/nuc2kor/Desktop/ipc_new.sock"

#     try:
#         os.unlink(socket_path)
#     except OSError:
#         pass

#     s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
#     s.bind(socket_path)

#     s.listen()
#     # result_list = []

#     # Variables for tracking packets per second
#     start_time = time.time()
#     packet_count = 0
#     time_values = deque()  # Queue to store time values (x-axis)
#     packet_rates = deque()  # Queue to store packet rates (y-axis)

#     # Set up matplotlib figure and axis
#     plt.figure()
#     plt.xlabel("Time (seconds)")
#     plt.ylabel("Packets per Second")

#     try:
#         while True:
#             conn, addr = s.accept()
#             try:
#                 while True:
#                     data = conn.recv(25)
#                     if data:
#                         # result_list.append(data)
#                         packet_count += 1
#                         # print("Received:", data)

#                         # Calculate elapsed time
#                         elapsed_time = time.time() - start_time

#                         # Calculate packets per second (rate)
#                         if elapsed_time > 0:
#                             print("Elapsed time: "+ str(elapsed_time) + "Packet count" + str(packet_count))
#                             packets_per_second = packet_count / elapsed_time

#                             # Append data points to queues
#                             time_values.append(elapsed_time)
#                             packet_rates.append(packets_per_second)

#                             # Update plot with new data points
#                             plt.plot(time_values, packet_rates, color='b')
#                             plt.draw()
#                             plt.pause(0.1)  # Small pause to allow plot to update
#                             # packet_count = 0
#             finally:
#                 conn.close()

#     except KeyboardInterrupt:
#         # Handle keyboard interrupt (Ctrl+C)
#         print("Plotting stopped by user.")
#         plt.show()  # Display final plot when program is terminated

import socket
import os
import time
import matplotlib.pyplot as plt

if __name__ == "__main__":
    socket_path = "/home/nuc2kor/Desktop/ipc_new.sock"

    try:
        os.unlink(socket_path)
    except OSError:
        pass

    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.bind(socket_path)

    s.listen()
    
    # Variables for tracking packets received per second
    start_time = time.time()
    current_second = int(start_time)
    packets_per_second = {}  # Dictionary to store packets received per second
    
    # Set up matplotlib figure and axis
    plt.figure()
    plt.xlabel("Time (seconds)")
    plt.ylabel("Packets Received per Second")

    try:
        while True:
            conn, addr = s.accept()
            try:
                while True:
                    data = conn.recv(25)
                    if data:
                        # Update current second based on elapsed time
                        elapsed_time = time.time() - start_time
                        current_second = int(start_time + elapsed_time)
                        
                        # Update packets received count for the current second
                        if current_second in packets_per_second:
                            packets_per_second[current_second] += 1
                        else:
                            packets_per_second[current_second] = 1
                        
                        # Prepare data for plotting
                        x_values = list(packets_per_second.keys())
                        y_values = list(packets_per_second.values())
                        
                        # Update plot with new data points
                        plt.clf()  # Clear existing plot
                        plt.plot(x_values, y_values, color='b')
                        plt.xlabel("Time (seconds)")
                        plt.ylabel("Packets Received per Second")
                        plt.draw()
                        plt.pause(0.1)  # Small pause to allow plot to update
            finally:
                conn.close()

    except KeyboardInterrupt:
        # Handle keyboard interrupt (Ctrl+C)
        print("Plotting stopped by user.")
        plt.show()  # Display final plot when program is terminated
