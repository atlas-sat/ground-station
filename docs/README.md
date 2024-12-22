<div align="left" style="position: relative;">
<h1>Atlas Sat Ground Station</h1>
<p align="left">
    <em>Ground Station UI designed for Atlas Sat. Developed at DSO National Laboratories for R@YDSP</em>
</p>
<p align="left">
    <!--Latest Release Version-->
    <img src="https://img.shields.io/github/v/release/atlas-sat/ground-station?style=default&logo=github&logoColor=white&color=0080ff" alt="latest-release">
    <img src="https://img.shields.io/github/last-commit/atlas-sat/ground-station?style=default&logo=git&logoColor=white&color=0080ff" alt="last-commit">
    <img src="https://img.shields.io/github/languages/top/atlas-sat/ground-station?style=default&color=0080ff" alt="repo-top-language">
    <img src="https://img.shields.io/github/languages/count/atlas-sat/ground-station?style=default&color=0080ff" alt="repo-languages">
    <img src="https://img.shields.io/github/repo-size/atlas-sat/ground-station?style=default&color=0080ff" alt="repo-size">
</p>

<!-- insert logo here -->

</div>
<br clear="right">


## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Testing Without Hardware](#testing-without-hardware)
  - [Simulating Data](#simulating-data)
- [License](#license)

## Installation

Clone the repository to your local machine using the following command:

```bash
git clone https://github.com/atlas-sat/ground-station
```

Navigate to the project directory:

```bash
cd ground-station
```

To install the necessary dependencies, run the following command:

```bash
pip install -r requirements.txt
```

## Usage

Before starting the application, make sure to connect a USB to UART adapter to the computer. The adapter should be connected to a tranceiver (e.g. HC12).
Unfortunately, the application is not able to automatically detect the COM port of the adapter. Therefore, you will need to manually set the COM port in the `telemetry.py` and `downlink.py` file.

telemetry.py (line 14):
```python
    ser = serial.Serial(
        port='COM6', # change to the COM port of the USB to UART adapter
        baudrate=9600,
        timeout=30
    )
```

downlink.py (lines 33 and 48):
```python
    ser = serial.Serial('COM6') # change to the COM port of the USB to UART adapter
    ser.baudrate = 9600
    ser.timeout = 30
```

To start the application, use the following command:

```bash
py main.py
```

## Testing Without Hardware

If you do not have access to the CubeSat or a USB to UART bridge, you can still test the application after running `py main.py`. To do this, you will need to run the following command in a separate terminal:

```bash
py tm_sim.py
```

When running, the simulation script will append random telemetry data to telemetry.csv. The Ground Station application will read this data and display it on the GUI.

### Simulating Data

To change the data that is appended to telemetry.csv, you can modify the `start` function in `tm_sim.py`. The `start` function is responsible for appending data to the CSV file.

tm_sim.py (lines 10-11):
```python
    x = random.randint(0, 255) # change to desired value/range
    y = random.randint(0, 255) # change to desired value/range
```

## License

This project is not protected under any license. You are free to use, modify, and distribute the software as you see fit.