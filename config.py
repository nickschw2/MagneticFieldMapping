from datetime import date

# NI DAQ
dev_name = 'PXI1Slot3'
ai_channels = {'Bx': 'ai3', 'By': 'ai4', 'Bz': 'ai5'}

# Voltage mapping
MagnetometerMaxVoltage = 1 # Volts
MagnetometerMaxField = 3 # Tesla

# Locations
directions = ['x', 'y', 'z']

# GUI config
userInputPadding = 30 # pixels
labelPadding = 30 # pixels
userInputWidth = 8

button_opts = {'font':('Helvetica', 12), 'state':'normal'}
text_opts = {'font':('Helvetica', 12)}
entry_opts = {'font':('Helvetica', 12), 'width':userInputWidth}
frame_opts = {'borderwidth': 3, 'relief': 'raised', 'padding': 12}

# Saving results
columns = directions + list(ai_channels.keys()) + ['magnitude']
today = date.today().strftime("%Y_%m_%d")
folder = 'results'
filename = f'{today}_Bfield.csv'
filepath = f'{folder}/{filename}'
