# flrig-hf-scanner
An HF scanner that interfaces with FLRig to automate frequency scanning for phone QSOs.

See wiki for config and usage instructions: https://github.com/jrobertfisher/flrig-hf-scanner/wiki

FLRig HF Scanner 1.0 Release Notes

scanner-gui.py – GUI interface that controls radio transceivers via FLRig using XML-RPC. The code implements several functions for setting the transceiver's frequency to different bands, such as 80m, 60m, 40m, etc., within the limits of General Class ham radio operators. Functions connect FLRig HF Scanner to a FLRig server using a configurable hostname and port number and set the transceiver's mode, bandwidth, and initial frequency according to the band. The code uses threading to run functions in the background. If the connection is successful, the program enables new or continued scans and has a function to stop scanning. You can also tune the scan's sensitivity to a specific dB the scan will stop on. You can also control the step size of the scan in 100 Hz increments from 100 to 1000 Hz.

scanner.py – The command-line interface establishes a connection to a FLRig server running on the localhost:12345. It sets up XML-RPC calls to retrieve and configure radio transceiver parameters such as version, RF power, S-meter reading, bandwidth, and frequency. It uses the phone band limits for General Class ham radio operators and queries the user to set the band or uses the current frequency to select the mode, start, and end frequency. If the current frequency or the user input doesn't match the supported bands, the program exits with an error message. The band limits and step size define the scanning configuration. The sensitivity is set to 20 by default.