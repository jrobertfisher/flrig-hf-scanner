import tkinter as tk
import xmlrpc.client
import time
import threading
from tkinter import messagebox

class App:
    def __init__(self, master):
        self.master = master
        master.title("FLRig HF Scanner Ver. 1.0")
        self.start_freq = None
        self.end_freq = None
        self.flrig = None

        # Create labels for status, hostname, port, bands, scan, and signal
        tk.Label(master, text="Status:").grid(row=0, sticky="W")
        tk.Label(master, text="Hostname:").grid(row=1, sticky="W")
        tk.Label(master, text="Port:").grid(row=2, sticky="W")
        tk.Label(master, text="").grid(row=3, sticky="W")
        tk.Label(master, text="Bands:").grid(row=4, sticky="W")
        tk.Label(master, text="").grid(row=5, sticky="W")
        tk.Label(master, text="dB Sensitivity:").grid(row=6, sticky="W")
        tk.Label(master, text="Step Size:").grid(row=6, column=2, sticky="W")
        tk.Label(master, text="").grid(row=7, column=2, sticky="W")
        tk.Label(master, text="Scan:").grid(row=9, sticky="W")

        # Create flrig server version text after connection
        self.version_label = tk.Label(master, text="Disconnected")
        self.version_label.grid(row=0, column=1, columnspan=5, sticky="W")

        # Create signal label
        self.signal_label = tk.Label(master, text="Signal:")
        self.signal_label.grid(row=8, sticky="W")

        # Create entry fields for hostname and port
        self.hostname_entry = tk.Entry(master)
        self.hostname_entry.insert(0,"127.0.0.1")
        self.hostname_entry.grid(row=1, column=1)
        self.port_entry = tk.Entry(master)
        self.port_entry.insert(0,"12345")
        self.port_entry.grid(row=2, column=1)

        # Create a button to connect to FLRig and display the version
        self.connect_button = tk.Button(master, text="Connect", command=self.run_connect)
        self.connect_button.grid(row=1, rowspan=2, column=2, sticky="E")

        # Create a button to disconnect FLRig Server
        self.disconnect_button = tk.Button(master, text="Disconnect", command=self.run_disconnect)
        self.disconnect_button.grid(row=1, rowspan=2, column=3, sticky="W")
        self.disconnect_button.config(state=tk.DISABLED)

        # Create a button to change the frequency to 80m
        self.freq_80m_button = tk.Button(master, text="80m", command=self.freq_80m)
        self.freq_80m_button.place(x=61, y=84)

        # Create a button to change the frequency to 60m
        self.freq_60m_button = tk.Button(master, text="60m", command=self.freq_60m)
        self.freq_60m_button.place(x=95, y=84)

        # Create a button to change the frequency to 40m
        self.freq_40m_button = tk.Button(master, text="40m", command=self.freq_40m)
        self.freq_40m_button.place(x=129, y=84)

        # Create a button to change the frequency to 20m
        self.freq_20m_button = tk.Button(master, text="20m", command=self.freq_20m)
        self.freq_20m_button.place(x=163, y=84)

        # Create a button to change the frequency to 17m
        self.freq_17m_button = tk.Button(master, text="17m", command=self.freq_17m)
        self.freq_17m_button.place(x=197, y=84)

        # Create a button to change the frequency to 15m
        self.freq_15m_button = tk.Button(master, text="15m", command=self.freq_15m)
        self.freq_15m_button.place(x=231, y=84)

        # Create a button to change the frequency to 12m
        self.freq_12m_button = tk.Button(master, text="12m", command=self.freq_12m)
        self.freq_12m_button.place(x=265, y=84)

        # Create a button to change the frequency to 10m
        self.freq_10m_button = tk.Button(master, text="10m", command=self.freq_10m)
        self.freq_10m_button.place(x=299, y=84)

        # Create a label to show sensitivity
        self.sensitivity_label = tk.Label(master)

        # Create a label to show step size
        self.step_size_label = tk.Label(master)

        # Create a scale widget to select the sensitivity
        self.sensitivity_scale = tk.Scale(master, from_=1, to=100, orient=tk.HORIZONTAL, command=self.sensitivity)
        self.sensitivity_scale.set(20)
        self.sensitivity_scale.grid(row=6, column=1)

        # Create a scale widget to select the sensitivity
        self.step_size_scale = tk.Scale(master, from_=100, to=1000, resolution=100, orient=tk.HORIZONTAL, command=self.step_size)
        self.step_size_scale.set(500)
        self.step_size_scale.grid(row=6, column=3)

        # Create a button to scan the currently selected frequency
        self.scan_button = tk.Button(master, text="New Scan", command=self.run_scan_band)
        self.scan_button.grid(row=9, column=1, sticky="E")
        self.scan_button.config(state=tk.DISABLED)
        
        # Create a button to scan the currently selected frequency
        self.continue_button = tk.Button(master, text="Continue Scan", command=self.run_continue_band)
        self.continue_button.grid(row=9, column=2, sticky="E")
        self.continue_button.config(state=tk.DISABLED)

        # Create a button to stop the scan
        self.stop_button = tk.Button(master, text="Stop Scan", command=self.run_scan_band)
        self.stop_button.grid(row=9, column=3, sticky="W")

    def run_connect(self):
        threading.Thread(target=self.connect).start()
        # Disable the scan button
                
    def connect(self):
        # Get the hostname and port number from the entry fields
        hostname = self.hostname_entry.get()
        port = int(self.port_entry.get())

        # Connect to FLRig using XML-RPC
        self.flrig = xmlrpc.client.ServerProxy(f"http://{hostname}:{port}/RPC2")

        # Get the FLRig version and display it
        version = self.flrig.main.get_version()
        try:
            self.version_label.config(text=f"Connected to FLRig Server Ver.: {version}")
            self.connect_button.config(state=tk.DISABLED)
            self.disconnect_button.config(state=tk.NORMAL)
            self.scan_button.config(state=tk.NORMAL)
            self.continue_button.config(state=tk.NORMAL)
        except Exception as e:
            self.version_label.config(text=f"Failed to connect to FLRig server: {e}")
        

    def run_disconnect(self):
        threading.Thread(target=self.disconnect).start()
        # Disable the scan button
        
    def disconnect(self):
        if self.flrig is None:
            messagebox.showerror("Error", "Not connected to FLRig Server")
            return
        #self.flrig.system.close()
        self.flrig = xmlrpc.client.ServerProxy("http://localhost:0/RPC2")
        self.version_label.config(text="Disconnected")
        self.connect_button.config(state=tk.NORMAL)
        self.disconnect_button.config(state=tk.DISABLED)
        self.scan_button.config(state=tk.DISABLED)
        self.continue_button.config(state=tk.DISABLED)


    def freq_80m(self):
        if self.flrig is None:
            messagebox.showerror("Error", "Not connected to FLRig Server")
            return
        # Set the frequency to 3.700 MHz
        self.flrig.rig.set_mode("LSB")
        self.flrig.rig.set_bandwidth(3000)
        self.flrig.rig.set_vfo(float(3700000))
        self.start_freq = 3700000
        self.end_freq = 4000000

    def freq_60m(self):
        if self.flrig is None:
            messagebox.showerror("Error", "Not connected to FLRig Server")
            return
        # Set the frequency to 5.354 MHz
        self.flrig.rig.set_mode("USB")
        self.flrig.rig.set_bandwidth(3000)
        self.flrig.rig.set_vfo(float(5354000))
        self.start_freq = 5354000
        self.end_freq = 5366000

    def freq_40m(self):
        if self.flrig is None:
            messagebox.showerror("Error", "Not connected to FLRig Server")
            return
        # Set the frequency to 3.700 MHz
        self.flrig.rig.set_mode("LSB")
        self.flrig.rig.set_bandwidth(3000)
        self.flrig.rig.set_vfo(float(7175000))
        self.start_freq = 7175000
        self.end_freq = 7300000

    def freq_20m(self):
        if self.flrig is None:
            messagebox.showerror("Error", "Not connected to FLRig Server")
            return
        # Set the frequency to 14.225 MHz
        self.flrig.rig.set_mode("USB")
        self.flrig.rig.set_bandwidth(3000)
        self.flrig.rig.set_vfo(float(14225000))
        self.start_freq = 14225000
        self.end_freq = 14350000

    def freq_17m(self):
        if self.flrig is None:
            messagebox.showerror("Error", "Not connected to FLRig Server")
            return
        # Set the frequency to 18.110 MHz
        self.flrig.rig.set_mode("USB")
        self.flrig.rig.set_bandwidth(3000)
        self.flrig.rig.set_vfo(float(18110000))
        self.start_freq = 18110000
        self.end_freq = 18168000
    
    def freq_15m(self):
        if self.flrig is None:
            messagebox.showerror("Error", "Not connected to FLRig Server")
            return
        # Set the frequency to 21.275 MHz
        self.flrig.rig.set_mode("USB")
        self.flrig.rig.set_bandwidth(3000)
        self.flrig.rig.set_vfo(float(21275000))
        self.start_freq = 21275000
        self.end_freq = 21450000

    def freq_12m(self):
        if self.flrig is None:
            messagebox.showerror("Error", "Not connected to FLRig Server")
            return
        # Set the frequency to 24.930 MHz
        self.flrig.rig.set_mode("USB")
        self.flrig.rig.set_bandwidth(3000)
        self.flrig.rig.set_vfo(float(24930000))
        self.start_freq = 24930000
        self.end_freq = 24990000

    def freq_10m(self):
        if self.flrig is None:
            messagebox.showerror("Error", "Not connected to FLRig Server")
            return
        # Set the frequency to 28.300 MHz
        self.flrig.rig.set_mode("USB")
        self.flrig.rig.set_bandwidth(3000)
        self.flrig.rig.set_vfo(float(28300000))
        self.start_freq = 28300000
        self.end_freq = 29700000

    def sensitivity(self, value):
        #Set the signal sensitivity
        self.sensitivity_label.config(text=f"dB Sensitivity: {value}")

    def step_size(self, value):
        #Set scan step size
        self.step_size_label.config(text=f"Step Size: {value}")

    def run_scan_band(self):
        # Create an event object
        stop_event=threading.Event()
        #Create a thread
        threading.Thread(target=self.scan_band, args=(stop_event,)).start()

        # Disable the scan button
        self.scan_button.config(state=tk.DISABLED)
        self.continue_button.config(state=tk.DISABLED)
        
        # Enable the stop button
        self.stop_button.config(state=tk.NORMAL)

        # Set the stop event when the stop button is pressed
        self.stop_button.config(command=lambda: stop_event.set())

    def scan_band(self, stop_event):
        if self.flrig is None:
            messagebox.showerror("Error", "Not connected to FLRig Server")
            return

        # Define band frequencies as tuples
        bands = [
            ("80m", 3700000, 4000100, "LSB"),
            ("60m", 5354000, 5366100, "USB"),
            ("40m", 7175000, 7300100, "LSB"),
            ("20m", 14225000, 14350100, "USB"),
            ("17m", 18110000, 18168100, "USB"),
            ("15m", 21275000, 21450100, "USB"),
            ("12m", 24930000, 24990100, "USB"),
            ("10m", 28300000, 29700100, "USB"),
        ]

        # Get the current frequency from FLRig
        frequency = float(self.flrig.rig.get_vfo())

        # Determine the current band
        for band, start, stop, mode in bands:
            if start <= frequency <= stop:
                #self.start_freq = frequency
                self.start_freq = start
                self.end_freq = stop
                break
        else:
            # Frequency is not within any defined band
            messagebox.showerror("Error", "Current frequency is not within any defined band")
            return

        # Get the current sensitivity and step size from the scales
        sensitivity = self.sensitivity_scale.get()
        step_size = self.step_size_scale.get()
        frequency = self.start_freq

        # Call the scan method with the current frequency, sensitivity, and step size
        #while True:
        while not stop_event.is_set():
            for frequency in range(int(self.start_freq), self.end_freq, step_size):
                if stop_event.is_set():
                    self.scan_button.config(state=tk.NORMAL)
                    self.continue_button.config(state=tk.NORMAL)
                    break
                self.flrig.rig.set_vfo(float(frequency))
                time.sleep(0.1)

                smeter = self.flrig.rig.get_smeter()
                self.signal_label.config(text=f"Signal: {smeter} dB")
                #print(smeter)
                if int(smeter) >= sensitivity:
                    #print(f"Signal strength above {sensitivity} detected. Scanning stopped. Current frequency is {frequency}")
                    # Re-enable the scan button
                    self.scan_button.config(state=tk.NORMAL)
                    self.continue_button.config(state=tk.NORMAL)
                    break
            else:
                # End of the band reached, loop back to starting frequency
                for band, start, stop, mode in bands:
                    if start <= frequency <= stop:
                        self.start_freq = start
                        self.end_freq = stop
                continue
            break

    # def run_continue_band(self):
    #     threading.Thread(target=self.continue_band).start()
    #     # Disable the scan button
    #     self.scan_button.config(state=tk.DISABLED)
    #     self.continue_button.config(state=tk.DISABLED)

    def run_continue_band(self):
        # Create an event object
        stop_event=threading.Event()
        #Create a thread
        threading.Thread(target=self.continue_band, args=(stop_event,)).start()

        # Disable the scan button
        self.scan_button.config(state=tk.DISABLED)
        self.continue_button.config(state=tk.DISABLED)
        
        # Enable the stop button
        self.stop_button.config(state=tk.NORMAL)

        # Set the stop event when the stop button is pressed
        self.stop_button.config(command=lambda: stop_event.set())

        #self.frequency += step_size # +step_size forces the vfo to move forward

    def continue_band(self, stop_event):
        if self.flrig is None:
            messagebox.showerror("Error", "Not connected to FLRig Server")
            return

        # Define band frequencies as tuples
        bands = [
            ("80m", 3700000, 4000100, "LSB"),
            ("60m", 5354000, 5366100, "USB"),
            ("40m", 7175000, 7300100, "LSB"),
            ("20m", 14225000, 14350100, "USB"),
            ("17m", 18110000, 18168100, "USB"),
            ("15m", 21275000, 21450100, "USB"),
            ("12m", 24930000, 24990100, "USB"),
            ("10m", 28300000, 29700100, "USB"),
        ]

        # Get the current frequency from FLRig
        frequency = float(self.flrig.rig.get_vfo())
        
        # Determine the current band
        for band, start, stop, mode in bands:
            if start <= frequency <= stop:
                self.start_freq = frequency
                #self.start_freq = start
                self.end_freq = stop
                break
        else:
            # Frequency is not within any defined band
            messagebox.showerror("Error", "Current frequency is not within any defined band")
            return

        # Get the current sensitivity and step size from the scales
        sensitivity = self.sensitivity_scale.get()
        step_size = self.step_size_scale.get()
        frequency = self.start_freq 

        # Forces vfo to move forward
        self.start_freq = int(self.start_freq) + int(step_size)

        # Call the scan method with the current frequency, sensitivity, and step size
        while not stop_event.is_set():
            for frequency in range(int(self.start_freq), self.end_freq, step_size):
                if stop_event.is_set():
                    self.scan_button.config(state=tk.NORMAL)
                    self.continue_button.config(state=tk.NORMAL)
                    break
                self.flrig.rig.set_vfo(float(frequency))
                time.sleep(0.1)

                smeter = self.flrig.rig.get_smeter()
                self.signal_label.config(text=f"Signal: {smeter} dB")
                #print(smeter)
                if int(smeter) >= sensitivity:
                    #print(f"Signal strength above {sensitivity} detected. Scanning stopped. Current frequency is {frequency}")
                    self.scan_button.config(state=tk.NORMAL)
                    self.continue_button.config(state=tk.NORMAL)
                    break
            else:
                # End of the band reached, loop back to starting frequency
                for band, start, stop, mode in bands:
                    if start <= frequency <= stop:
                        self.start_freq = start
                        self.end_freq = stop
                continue
            break

root = tk.Tk()
root.geometry("425x270")
app = App(root)
root.mainloop()