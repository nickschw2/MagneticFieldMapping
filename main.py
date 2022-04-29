from ni_daq import *
from plots import *
from config import *
from messages import *
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import pandas as pd
import os

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # This line of code is customary to quit the application when it is closed
        self.protocol('WM_DELETE_WINDOW', self.on_closing)

        # self.chargePlot = CanvasPlot(self)

        # self.chargeVoltageAxis = self.chargePlot.ax
        # self.chargeCurrentAxis = self.chargePlot.ax.twinx()
        #
        # self.chargePlot.ax.set_xlim(0, 10)
        # self.chargeVoltageAxis.set_ylim(-1.2, 1.2)
        # self.chargeCurrentAxis.set_ylim(-1.2, 1.2)
        #
        # self.chargeVoltageLine, = self.chargeVoltageAxis.plot([],[]) #Create line object on plot
        # self.chargeCurrentLine, = self.chargeCurrentAxis.plot([],[]) #Create line object on plot
        #
        # self.chargePlot.pack()

        # Initialize data frame to store results if there is not already a mapping from today
        if folder not in os.listdir():
            os.mkdir(folder)

        if filename not in os.listdir(folder):
            self.results = pd.DataFrame(columns=columns)
            self.results.to_csv(filepath, columns=columns, index=False)
        else:
            self.results = pd.read_csv(filepath)

        # Initialize Daq
        self.daq = NI_DAQ(dev_name, ai_channels)

        # Frame for user input location
        self.locationFrame = ttk.LabelFrame(self, text='Location (cm)', **frame_opts)
        self.locationFrame.pack(side='top')

        self.locationLabels = {}
        self.locationVariables = {}
        self.locationEntries = {}
        for direction in directions:
            self.locationLabels[direction] = ttk.Label(self.locationFrame, text=direction, **text_opts)
            self.locationEntries[direction] = ttk.Entry(self.locationFrame, **entry_opts)

            self.locationLabels[direction].pack(side='left')
            self.locationEntries[direction].pack(side='left', padx=(0, userInputPadding))

        # Frame for magnetic field readings
        self.labels = ttk.LabelFrame(self, text='B-Field Values (T)', **frame_opts)
        self.labels.pack(side='top')

        self.fieldVariables = {}
        self.fieldLabels = {}
        for channel in ai_channels:
            self.fieldVariables[channel] = tk.StringVar(value=f'{channel}: 0.00 T')
            self.fieldLabels[channel] = ttk.Label(self.labels, textvariable=self.fieldVariables[channel], **text_opts)
            self.fieldLabels[channel].pack(side='left', padx=(0, labelPadding))

        # Add measure button
        self.measureButton = tk.Button(self, text='Measure', command=self.measure, **button_opts)
        self.measureButton.pack(side='bottom')

        # self.bm = BlitManager(self.chargePlot.canvas, [self.chargeVoltageLine, self.chargeCurrentLine, self.chargePlot.ax.xaxis])

    def measure(self):

        def append_result(result):
            # Add result to data frame results
            self.results = pd.concat([self.results, result], ignore_index=True)
            result.to_csv(filepath, mode='a', index=False, header=False)

        result = {}
        location = []

        # Get locations
        numericLocation = True
        for i, direction in enumerate(directions):
            axisPosition = self.locationEntries[direction].get()
            if axisPosition.isnumeric():
                # Include the offsets from the measuring tape
                # There is a minus sign because the measuring tape is in the opposite direction of the axes
                result[direction] = -(float(axisPosition) - offsets[direction])
                location.append(axisPosition)
            else:
                incorrectLocationName = 'Invalid Location'
                incorrectLocationText = 'Please input a valid location.'
                incorrectLocationWindow = MessageWindow(self, incorrectLocationName, incorrectLocationText)
                numericLocation = False

        if numericLocation:
            # Read daq
            values = self.daq.read()
            # initialize magnitude to 0
            magnitudeSquared = 0
            for channel in ai_channels:
                value = values[channel] * MagnetometerMaxField / MagnetometerMaxVoltage
                self.fieldVariables[channel].set(f'{channel}: {value:.2f}')
                result[channel] = value
                magnitudeSquared += value**2
                # calculate magnitude!!!!!

            magnitude = np.sqrt(magnitudeSquared)
            result['magnitude'] = magnitude

            # Convert to data frame
            result = pd.DataFrame(result, index=[0])

            if not self.results.empty:
                overwrite_row = (self.results[directions] == location).all(1)
                if overwrite_row.any():
                    self.results.loc[overwrite_row] = result.to_numpy()
                    self.results.to_csv(filepath, mode='w', index=False, columns=columns)
                else:
                    append_result(result)

            else:
                append_result(result)

    # def start_plot(self):
    #     self.plotting = True
    #     self.startTime = time.time()
    #     self.time = np.array([])
    #     self.voltage = np.array([])
    #     self.current = np.array([])
    #     self.plot_data()
    #     print('Start')

    # def stop_plot(self):
    #     self.plotting = False
    #     print('Stop')
    #
    # def clear_plot(self):
    #     self.time = np.array([])
    #     self.voltage = np.array([])
    #     self.current = np.array([])
    #     self.chargeVoltageLine.set_data(self.time, self.voltage)
    #     self.chargeCurrentLine.set_data(self.time, self.current)
    #     self.bm.update()

    # def plot_data(self):
    #     if self.plotting:
    #         timestamp = time.time() - self.startTime
    #         self.time = np.append(self.time, timestamp)
    #         self.voltage = np.append(self.voltage, np.sin(timestamp))
    #         self.current = np.append(self.current, np.cos(timestamp))
    #
    #         self.chargeVoltageLine.set_data(self.time, self.voltage)
    #         self.chargeCurrentLine.set_data(self.time, self.current)
    #
    #         if timestamp > self.timeLimit:
    #             self.chargePlot.ax.set_xlim(timestamp - self.timeLimit, timestamp)
    #         else:
    #             self.chargePlot.ax.set_xlim(0, self.timeLimit)
    #
    #         self.bm.update()
    #
    #         self.after(1, self.plot_data)

    # Special function for closing the window and program
    def on_closing(self):
        # close DAQ
        self.daq.close()

        # Close window
        plt.close('all')
        self.quit()
        self.destroy()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
