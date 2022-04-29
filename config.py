from datetime import date

# NI DAQ
dev_name = 'PXI1Slot3'
# ai_channels = {'Bx': 'ai5', 'By': 'ai4', 'Bz': 'ai3'}
# The orientation of the magnetometer probe is not aliged with our axes for magnetic field measurements
# According to Fig 3-6 in Lakeshore 460 manual
# (https://www.lakeshore.com/docs/default-source/product-downloads/manuals/460_manual.pdf?sfvrsn=72e8e1c4_1)
# The positive direction of field is into the stickers
ai_channels = {'Bx': 'ai3', 'By': 'ai5', 'Bz': 'ai4'}

# Voltage mapping
MagnetometerMaxVoltage = 3 # Volts
MagnetometerMaxField = 3 # Tesla

# Locations
directions = ['x', 'y', 'z']

# Offsets on measuring tape to get to 0, 0, 0, in cm
# NB that +x points west, +y points up, +z points north
offsets = {'x': 40, 'y': 70, 'z': 30}

# GUI config
userInputPadding = 30 # pixels
labelPadding = 30 # pixels
userInputWidth = 8
framePadding = 20 #pixels
topLevelWidth = 30
topLevelWrapLength = 275

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
