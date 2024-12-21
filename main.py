import tkinter as tk
from tkinter import ttk
import threading
import os
import telemetry
import downlink
import time
import ctypes
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
ctypes.windll.shcore.SetProcessDpiAwareness(True)

# Placeholder functions for satellite operations
def start_imaging():
    telemetry.stop()  # meow Remove when two HC12s are available
    print("Stopped listening for telemetry data.")  # meow Remove when two HC12s are available

    print("Imaging mission started.")
    imaging_button.config(state="disabled")
    downlink.start()

    start_telemetry()  # meow Remove when two HC12s are available

def find_newest_file(directory):
    files = os.listdir(directory)
    paths = [os.path.join(directory, basename) for basename in files]
    return max(paths, key=os.path.getctime)

def downlink_process():
    print("Downlink process started.")
    downlink.downlink_start()
    current_directory = os.getcwd()
    print(f"Downlinked data saved to {current_directory}")
    imaging_button.config(state="enabled")
    downlink_button.config(state="enabled")
    
    popup = tk.Tk()
    popup.title("Downlink Complete")
    label = ttk.Label(popup, text=f"Downlinked data saved to:\n {current_directory}.")
    label.pack(padx=10, pady=10)
    close_button = ttk.Button(popup, text="Close", command=popup.destroy)
    close_button.pack(padx=10, pady=10)
    popup.mainloop()

    start_telemetry()  # meow Remove when two HC12s are available

def start_downlink():
    telemetry.stop()  # meow Remove when two HC12s are available
    print("Stopped listening for telemetry data.")  # meow Remove when two HC12s are available
    print("Downlink requested.")
    downlink_button.config(state="disabled")
    threading.Thread(target=downlink_process).start()

def update_telemetry_gui():
    try:
        if os.path.exists("telemetry.csv"):
            with open("telemetry.csv", 'r') as file:
                lines = file.readlines()
                if lines:
                    last_line = lines[-1].strip()
                    values = last_line.split(',')
                    if len(values) >= 2:
                        current = values[0]
                        temperature = values[1]
                        current_value.config(text=f"{current} A")
                        temperature_value.config(text=f"{temperature} °C")
                        telemetry_status.config(text=f"{time.ctime(os.path.getmtime('telemetry.csv'))}")
    except Exception as e:
        print(f"Error updating telemetry: {e}")
    finally:
        root.after(1000, update_telemetry_gui)

def start_telemetry():
    try:
        telemetry_thread = threading.Thread(target=telemetry.start, daemon=True)
        telemetry_thread.start()
        print("Telemetry listener started.")
    except Exception as e:
        print(f"Error starting telemetry listener: {e}")

def update_telemetry_graph():
    try:
        if os.path.exists("telemetry.csv"):
            with open("telemetry.csv", 'r') as file:
                lines = file.readlines()
                if lines:
                    currents = []
                    temperatures = []
                    for line in lines[-10:]:
                        values = line.strip().split(',')
                        if len(values) >= 2:
                            currents.append(float(values[0]))
                            temperatures.append(float(values[1]))
                    
                    current_line.set_data(range(len(currents)), currents)
                    temperature_line.set_data(range(len(temperatures)), temperatures)
                    
                    ax.relim()
                    ax.autoscale_view()
                    ax2.relim()
                    ax2.autoscale_view()
                    
                    canvas.draw()
    except Exception as e:
        print(f"Error updating telemetry graph: {e}")
    finally:
        root.after(1000, update_telemetry_graph)

root = tk.Tk()
root.title("Satellite Ground Station")

graph_frame = ttk.LabelFrame(root, text="Telemetry Graph", padding=(20, 20))
graph_frame.grid(row=2, column=0, padx=20, pady=20, sticky="ew")

root.after(1000, update_telemetry_graph)

fig = Figure(figsize=(6, 4), dpi=100, constrained_layout=True, facecolor='none')
ax = fig.add_subplot(111, facecolor='none')
fig.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
# ax.set_title("Telemetry Data", fontsize=14, fontweight='bold', color="black")
ax.set_xlabel("Time", fontsize=12, color="black")
ax.set_ylabel("Current (A)", fontsize=12, color="black", labelpad=10)
ax.grid(True, which='both', linestyle='--', linewidth=0.5)
ax.minorticks_on()
ax.tick_params(axis='both', which='major', labelsize=10, colors="black")
ax.tick_params(axis='both', which='minor', labelsize=8, colors="black")

ax2 = ax.twinx()
ax2.set_ylabel("Temperature (°C)", fontsize=12, color="black", labelpad=10)
ax2.tick_params(axis='y', labelcolor="black")

ax.set_xticklabels([])

current_line, = ax.plot([], [], label="Current (A)", color="blue")
temperature_line, = ax2.plot([], [], label="Temperature (°C)", color="red")

# Combine legends
handles, labels = ax.get_legend_handles_labels()
handles2, labels2 = ax2.get_legend_handles_labels()

# Add the handles and labels from both axes
handles.extend(handles2)
labels.extend(labels2)

# Create a single legend
ax.legend(handles, labels, loc='upper left', bbox_to_anchor=(0, 1), ncol=1)

canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas.draw()

s = ttk.Style()
bg = s.lookup("TFrame", "background")
bg_16bit = root.winfo_rgb(bg)
bg_string = "#" + "".join([hex(bg_color >> 8)[2:] for bg_color in bg_16bit])
canvas.get_tk_widget().config(bg=bg_string)

canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

ax.set_ylim([0, 3]) # axis limits for current
ax2.set_ylim([0, 50]) # axis limits for temperature

button_frame = ttk.LabelFrame(root, text="Operations", padding=(20, 20))
button_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

button_frame.grid_columnconfigure(0, weight=1)
button_frame.grid_columnconfigure(1, weight=1)

imaging_button = ttk.Button(button_frame, text="Start Imaging Mission", command=start_imaging, takefocus=False)
imaging_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

downlink_button = ttk.Button(button_frame, text="Request Downlink", command=start_downlink, takefocus=False)
downlink_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

telemetry_frame = ttk.LabelFrame(root, text="Telemetry", padding=(20, 20))
telemetry_frame.grid(row=1, column=0, padx=20, pady=20, sticky="ew")

current_label = ttk.Label(telemetry_frame, text="Current (A):")
current_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
current_value = ttk.Label(telemetry_frame, text="N/A")
current_value.grid(row=0, column=1, padx=5, pady=5, sticky="w")

temperature_label = ttk.Label(telemetry_frame, text="Temperature (°C):")
temperature_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
temperature_value = ttk.Label(telemetry_frame, text="N/A")
temperature_value.grid(row=1, column=1, padx=5, pady=5, sticky="w")

telemetry_status_label = ttk.Label(telemetry_frame, text="Last Received:")
telemetry_status_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
telemetry_status = ttk.Label(telemetry_frame, text="Never")
telemetry_status.grid(row=2, column=1, padx=5, pady=5, sticky="w")

start_telemetry()
root.after(1000, update_telemetry_gui)

print("GUI started.")

root.mainloop()
