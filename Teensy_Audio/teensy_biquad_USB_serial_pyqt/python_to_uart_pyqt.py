import numpy as np
import scipy.signal as signal
import pyqtgraph as pg
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QComboBox, QSlider, QPushButton, QLabel, QPlainTextEdit
from PyQt6.QtCore import Qt
from python_functions.filters import get_filter_coefficients
import serial
import json

FS = 48000  # Sampling frequency
SERIAL_SPEED = 9600   # Serial communication speed
SERIAL_PORT = "/dev/cu.usbmodem88092601"  # Serial port for Teensy board

# Class defining the main window of the filter design GUI


class IIRFilterDesigner(QMainWindow):
    def __init__(self):
        super().__init__()
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
        self.sendButton.clicked.connect(self.sendCoefficients)
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

        self.freqLabel.setText(f'frequency = {self.frequency:.2f} Hz')
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

    # Function to send filter coefficients to the Teensy board over serial
    def sendCoefficients(self):
        # Serial communication to send the coefficients in JSON format
        ser = serial.Serial(SERIAL_PORT, SERIAL_SPEED, timeout=1)
        try:
            coeffs_list = np.concatenate([self.b, self.a[1:]]).tolist()
            json_data = json.dumps(coeffs_list) + '\n'
            ser.write(json_data.encode())

            # Wait for ESP32 to process the data
        except Exception as e:
            print(f"Error: {e}")
        finally:
            ser.close()


# Main function to run the application
def main():
    app = QApplication([])
    designer = IIRFilterDesigner()
    designer.show()
    app.exec()


if __name__ == "__main__":
    main()
