import xmlrpc.client
import time

# Connect to the flrig server on localhost port 12345
server_url = "http://localhost:12345"
flrig = xmlrpc.client.ServerProxy(server_url)

version = flrig.main.get_version
print("Connected to flrig version:",version())
power = flrig.rig.get_power
print("RF Power:",power())
#frequency = flrig.rig.get_vfo()
#print("Current frequency:", frequency)
smeter = flrig.rig.get_smeter()
print("Current S Meter:",smeter)
Sunits = flrig.rig.get_Sunits()
print("Current S Units:",Sunits)

# Set radio bandwidth for phone
#bandwidth = 3000
#flrig.rig.set_bandwidth(int(bandwidth))

# Set scanning config
step_size = 500
sensitivity = 20

# Band Frequencies for General Class
bands_80m_start = 3700000
bands_80m_stop = 4000100

bands_60m_start = 5354000
bands_60m_stop = 5366100

bands_40m_start = 7175000
bands_40m_stop = 7300100

bands_20m_start = 14225000
bands_20m_stop = 14350100

bands_17m_start = 18110000
bands_17m_stop = 18168100

bands_15m_start = 21275000
bands_15m_stop = 21450100

bands_12m_start = 24930000
bands_12m_stop = 24990100

bands_10m_start = 28300000
bands_10m_stop = 29700100

# Get current frequency
current_freq = flrig.rig.get_vfo()

# Ask user to set the band manually or use the current frequency
band_choice = input(f"Current frequency is {current_freq}. Press enter to scan this band, or enter a band (80m, 60m, 40m, 30m, 20m, 17m, 15, 12m, 10m): ")

# Determine which band we are in based on user input or current frequency
if band_choice == "":
    if float(current_freq) >= bands_80m_start and float(current_freq) <= bands_80m_stop:
        # We are in the 80m band
        mode = "LSB"
        start_freq = float(current_freq)
        end_freq = bands_80m_stop
    elif float(current_freq) >= bands_60m_start and float(current_freq) <= bands_60m_stop:
        # We are in the 60m band
        mode = "USB"
        start_freq = float(current_freq)
        end_freq = bands_60m_stop
    elif float(current_freq) >= bands_40m_start and float(current_freq) <= bands_40m_stop:
        # We are in the 40m band
        mode = "LSB"
        start_freq = float(current_freq)
        end_freq = bands_40m_stop
    elif float(current_freq) >= bands_20m_start and float(current_freq) <= bands_20m_stop:
        # We are in the 20m band
        mode = "USB"
        start_freq = float(current_freq)
        end_freq = bands_20m_stop
    elif float(current_freq) >= bands_17m_start and float(current_freq) <= bands_17m_stop:
        # We are in the 17m band
        mode = "USB"
        start_freq = float(current_freq)
        end_freq = bands_17m_stop
    elif float(current_freq) >= bands_15m_start and float(current_freq) <= bands_15m_stop:
        # We are in the 15m band
        mode = "USB"
        start_freq = float(current_freq)
        end_freq = bands_15m_stop
    elif float(current_freq) >= bands_12m_start and float(current_freq) <= bands_12m_stop:
        # We are in the 12m band
        mode = "USB"
        start_freq = float(current_freq)
        end_freq = bands_12m_stop
    elif float(current_freq) >= bands_10m_start and float(current_freq) <= bands_10m_stop:
        # We are in the 10m band
        mode = "USB"
        start_freq = float(current_freq)
        end_freq = bands_10m_stop
    else:
        # We are not in a supported band
        print("Current frequency is not in a supported band.")
        exit()
else:
    if band_choice == "80m":
        mode = "LSB"
        start_freq = bands_80m_start
        end_freq = bands_80m_stop
    elif band_choice == "60m":
        mode = "USB"
        start_freq = bands_60m_start
        end_freq = bands_60m_stop
    elif band_choice == "40m":
        mode = "LSB"
        start_freq = bands_40m_start
        end_freq = bands_40m_stop
    elif band_choice == "20m":
        mode = "USB"
        start_freq = bands_20m_start
        end_freq = bands_20m_stop
    elif band_choice == "17m":
        mode = "USB"
        start_freq = bands_17m_start
        end_freq = bands_17m_stop
    elif band_choice == "15m":
        mode = "USB"
        start_freq = bands_15m_start
        end_freq = bands_15m_stop
    elif band_choice == "12m":
        mode = "USB"
        start_freq = bands_12m_start
        end_freq = bands_12m_stop
    elif band_choice == "10m":
        mode = "USB"
        start_freq = bands_10m_start
        end_freq = bands_10m_stop
    else:
        # Invalid band selection
        print("Invalid band selection.")
        exit()

# Scan from current frequency to the end of the band
while True:
    for freq in range(int(start_freq), end_freq, step_size):
        flrig.rig.set_mode(mode)
        freq = freq + step_size
        flrig.rig.set_vfo(float(freq))
        time.sleep(0.1)

        smeter = flrig.rig.get_smeter()
        if int(smeter) >= sensitivity:
            print(f"Signal strength above {sensitivity} detected. Scanning stopped. Current frequency is {current_freq}")
            break
    else:
        # end of the band reached, loop back to starting frequency
        if float(current_freq) >= bands_80m_start and float(current_freq) <= bands_80m_stop:
            # We are in the 80m band
            mode = "LSB"
            start_freq = bands_80m_start
            end_freq = bands_80m_stop
        elif float(current_freq) >= bands_60m_start and float(current_freq) <= bands_60m_stop:
            # We are in the 60m band
            mode = "USB"
            start_freq = bands_60m_start
            end_freq = bands_60m_stop
        elif float(current_freq) >= bands_40m_start and float(current_freq) <= bands_40m_stop:
            # We are in the 40m band
            mode = "LSB"
            start_freq = bands_40m_start
            end_freq = bands_40m_stop
        elif float(current_freq) >= bands_20m_start and float(current_freq) <= bands_20m_stop:
            # We are in the 20m band
            mode = "USB"
            start_freq = bands_20m_start
            end_freq = bands_20m_stop
        elif float(current_freq) >= bands_17m_start and float(current_freq) <= bands_17m_stop:
            # We are in the 17m band
            mode = "USB"
            start_freq = bands_17m_start
            end_freq = bands_17m_stop
        elif float(current_freq) >= bands_15m_start and float(current_freq) <= bands_15m_stop:
            # We are in the 15m band
            mode = "USB"
            start_freq = bands_15m_start
            end_freq = bands_15m_stop
        elif float(current_freq) >= bands_12m_start and float(current_freq) <= bands_12m_stop:
            # We are in the 12m band
            mode = "USB"
            start_freq = bands_12m_start
            end_freq = bands_12m_stop
        elif float(current_freq) >= bands_10m_start and float(current_freq) <= bands_10m_stop:
            # We are in the 10m band
            mode = "USB"
            start_freq = bands_10m_start
            end_freq = bands_10m_stop
        else:
            # We are not in a supported band
            print("Current frequency is not in a supported band.")
            exit()
        continue
    # break out of the infinite loop when a signal is detected
    break