import numpy as np
import scipy.signal as signal
import pyqtgraph as pg
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QComboBox, QSlider, QPushButton, QLabel, QPlainTextEdit, QMessageBox
from PyQt6.QtCore import Qt, QThread, QObject, pyqtSignal
from python_functions.filters import get_filter_coefficients
import json
import asyncio
import qasync
from dataclasses import dataclass
from functools import cached_property
from bleak import BleakScanner, BleakClient
from bleak.backends.device import BLEDevice

# Initialize the asyncio event loop
loop = asyncio.get_event_loop()

FS = 48000  # Sampling frequency
DEVICE_NAME = 'ESP32_UART'
CHARACTERISTIC_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"


class CoefficientsSenderThread(QThread):
    def __init__(self, coefficients):
        QThread.__init__(self)
        self.coefficients = coefficients

    def run(self):
        asyncio.run(self.sendCoefficients())

    async def sendCoefficients(self):
        # BLE communication to send the coefficients in JSON format
        device = await BleakScanner.find_device_by_name(DEVICE_NAME)
        print(device)

        # Connect to the ESP32
        async with BleakClient(device) as client:
            try:
                coeffs_list = np.concatenate(self.coefficients).tolist()
                json_data = json.dumps(coeffs_list) + '\n'

                connected = await client.is_connected()
                print(f"Connected: {connected}")
                # Replace with the message you want to sendç

                # Writing the message to the characteristic
                await client.write_gatt_char(CHARACTERISTIC_UUID, json_data.encode())
                print("Message sent to the ESP32")

            except Exception as e:
                print(f"An error occurred: {e}")

            finally:
                # Check if still connected, then disconnect
                if await client.is_connected():
                    await client.disconnect()
                    print("Disconnected from the ESP32")
                else:
                    print("Already disconnected from the ESP32")


# Class defining the main window of the filter design GUI
class IIRFilterDesigner(QMainWindow):
    def __init__(self):
        super().__init__()
        self._device = None
        self._client = None
        self.initUI()

    # Function to initialize the user interface
    def initUI(self):

        # Setup layout, widgets, sliders, buttons, etc.
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        layout = QVBoxLayout(self.centralWidget)

        # Graph
        self.graphWidget = pg.PlotWidget()
        self.graphWidget.showGrid(x=True, y=True)
        self.graphWidget.setLogMode(x=True, y=False)
        self.graphWidget.setLabel('left', 'Gain [dB]')
        self.graphWidget.setLabel('bottom', 'Frequency [Hz]')
        self.graphWidget.setXRange(np.log10(20), np.log10(20e3))
        self.graphWidget.setYRange(-60, 20)
        self.graphWidget.setBackground('w')
        self.plot_curve1 = self.graphWidget.plot(
            pen=pg.mkPen(color='b', width=7))  # Create a plot curve

        layout.addWidget(self.graphWidget)

        # Dropdown for filter type
        self.filterTypeComboBox = QComboBox()
        self.filterTypeComboBox.addItems(
            ["Low-pass", "High-pass", "Band-pass", "Peaking", "Low Shelf", "High Shelf", "Notch"])
        layout.addWidget(self.filterTypeComboBox)

        # Sliders
        freqLayout = QHBoxLayout()
        self.frequencySlider = self.createLogSlider(20, 20000, 1000)
        self.freqLabel = QLabel()
        self.freqLabel.setText('frequency = 1000 Hz')
        freqLayout.addWidget(self.frequencySlider, stretch=1)
        freqLayout.addWidget(self.freqLabel, stretch=1)

        QFactorLayout = QHBoxLayout()
        self.QFactorSlider = self.createLogSlider(0.01, 100, 0.707)
        self.QFactorLabel = QLabel()
        self.QFactorLabel.setText('Quality factor = 0.707')
        QFactorLayout.addWidget(self.QFactorSlider, stretch=1)
        QFactorLayout.addWidget(self.QFactorLabel, stretch=1)

        gainLayout = QHBoxLayout()
        self.gainSlider = QSlider(Qt.Orientation.Horizontal)
        self.gainSlider.setMinimum(-30)
        self.gainSlider.setMaximum(30)
        self.gainSlider.setValue(0)
        self.gainLabel = QLabel()
        self.gainLabel.setText('Gain = 0 dB')
        gainLayout.addWidget(self.gainSlider, stretch=1)
        gainLayout.addWidget(self.gainLabel, stretch=1)

        layout.addLayout(freqLayout)
        layout.addLayout(QFactorLayout)
        layout.addLayout(gainLayout)

        # Button
        self.sendButton = QPushButton("Send filter coefficients")
        self.sendButton.setFixedHeight(50)
        layout.addWidget(self.sendButton)

        # Setup signal-slot connections for GUI elements
        # When a slider value changes, update the filter coefficients and send them to the Teensy board
        self.filterTypeComboBox.currentIndexChanged.connect(self.updateFilter)
        self.frequencySlider.valueChanged.connect(self.updateFilter)
        self.QFactorSlider.valueChanged.connect(self.updateFilter)
        self.gainSlider.valueChanged.connect(self.updateFilter)

        # Default values
        self.filterType = 'Low-pass'
        self.frequency = 1000
        self.QFactor = 0.707
        self.dBgain = 0
        self.b = np.array([1.0, 0, 0])
        self.a = np.array([1.0, 0, 0])
        self.updateFilter()

        # Thread for coefficients
        self.coefficients_thread = CoefficientsSenderThread(
            [self.b, self.a[1:]])
        self.sendButton.clicked.connect(self.send_coefficients_thread)

    def createLogSlider(self, minValue, maxValue, defaultValue):
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setMinimum(int(np.log10(minValue) * 100))
        slider.setMaximum(int(np.log10(maxValue) * 100))
        slider.setValue(int(np.log10(defaultValue) * 100))
        slider.setSingleStep(1)
        return slider

    def logSliderValue(self, slider):
        return 10 ** (slider.value() / 100)

    def updateFilter(self):
        self.filterType = self.filterTypeComboBox.currentText()
        self.frequency = self.logSliderValue(self.frequencySlider)
        self.QFactor = self.logSliderValue(self.QFactorSlider)
        self.dBgain = self.gainSlider.value()

        self.freqLabel.setText(f'frequency = {self.frequency:.1f} Hz')
        self.QFactorLabel.setText(f'Quality factor = {self.QFactor:.2e}')
        self.gainLabel.setText(f'Gain = {self.dBgain} dB')

        # Enable or disable the gain slider based on the filter type
        if self.filterType in ['Low-pass', 'High-pass', 'Band-pass', 'Notch']:
            self.gainSlider.setEnabled(False)
        else:
            self.gainSlider.setEnabled(True)

        self.calculateCoefficients()
        self.plotFRF()

    def calculateCoefficients(self):
        self.b, self.a = get_filter_coefficients(
            self.filterType, Fc=self.frequency, Q=self.QFactor, dBgain=self.dBgain, fs=FS)

    def plotFRF(self):
        f_axis = np.logspace(np.log10(20), np.log10(20e3), 1000)
        _, H = signal.freqz(self.b, self.a, worN=f_axis, fs=FS)
        self.plot_curve1.setData(f_axis, 20 * np.log10(abs(H)))

    @qasync.asyncSlot()
    async def connect(self):
        print("connecting...")
        self._device = await BleakScanner.find_device_by_name(DEVICE_NAME)
        if isinstance(self._device, BLEDevice):
            self._client = BleakClient(self._device)
            try:
                # Explicitly connect to the device
                await self._client.connect()
                connected = await self._client.is_connected()
                print(f"Connected: {connected}")
            except Exception as e:
                print(f"Failed to connect: {e}")
                return  # Ensure to exit if connection fails

    # Synchronous wrapper function

    @qasync.asyncSlot()
    async def send_coefficients_thread(self):
        print('sending...')
        try:
            if await self._client.is_connected():
                coeffs_list = np.concatenate([self.b, self.a[1:]]).tolist()
                json_data = json.dumps(coeffs_list) + '\n'

                # Writing the message to the characteristic
                await self._client.write_gatt_char(CHARACTERISTIC_UUID, json_data.encode())
                print("Message sent to the ESP32")

        except Exception as e:
            print(f"An error occurred: {e}")

    # @qasync.asyncSlot()
    # async def closeEvent(self, event):
    #     # print('closing...')
    #     # if self._client is not None and await self._client.is_connected():
    #     #     await self._client.disconnect()
    #     #     print("Disconnected")
    #     event.accept()

# Main function to run the application


def main():
    app = QApplication([])
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)

    designer = IIRFilterDesigner()
    designer.connect()
    designer.show()

    with loop:
        loop.run_forever()


if __name__ == "__main__":
    main()
