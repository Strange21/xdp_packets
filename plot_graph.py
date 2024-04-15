# import matplotlib.pyplot as plt
# import numpy as np
# import time

# # Initialize plot
# plt.ion()  # Turn on interactive mode
# fig, ax = plt.subplots()
# line, = ax.plot([], [])

# # Update function
# def update_plot():
#     xdata = np.arange(100)
#     ydata = np.random.randn(100)
#     line.set_data(xdata, ydata)
#     ax.relim()  # Recalculate limits
#     ax.autoscale_view()  # Autoscale
#     time.sleep(1)
#     fig.canvas.draw()
#     fig.canvas.flush_events()

# # Continuously update and plot
# while True:
#     update_plot()


import subprocess
import time





if __name__ == "__main__":
    # Define the command to run (e.g., 'ping' command to continuously ping a host)
    command = ['sudo', 'RUST_LOG=info', './target/debug/myapp']

    # Launch the subprocess and capture its stdout as a pipe
    process = subprocess.Popen(command, stdout=subprocess.PIPE, universal_newlines=True)

    # Continuously read and process the output from the subprocess
    while True:
        a = []
        print("Entered in while loop")
        output = process.stdout.readline()  # Read a line of output from the subprocess
        print("Output reading done")
        if output == '' and process.poll() is not None:
            break  # Break the loop if there's no more output and the subprocess has exited
        if output:
            print("output.strip:" + output.strip())  # Process the output (e.g., print or further processing)
            a.append(output.strip)
        # time.sleep(1)

    # Wait for the subprocess to exit and get its return code
    return_code = process.wait()
    print(f"Subprocess exited with return code: {return_code}") 