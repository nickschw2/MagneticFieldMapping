import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import plotly.graph_objects as go
from scipy import interpolate

## Field maps at constant z faces
folder = 'results/both_magnets'
files = [file for file in os.listdir(folder) if file.endswith('Bfield.csv')]

def compileResults(files):
    results = pd.DataFrame()
    for file in files:
        filename = f'{folder}/{file}'
        results = pd.concat([results, pd.read_csv(filename)])

    # Sort results by x, y, and z coordinates
    results = results.sort_values(['x', 'y', 'z'])

    # Add columns for normal and tangential values
    results['r'] = np.sqrt(results['x'] ** 2 + results['y'] ** 2)
    results['theta'] = np.arctan(results['y'] / results['x'])
    results['Br'] = (results['Bx'] * results['x'] + results['By'] * results['y']) / results['r']
    results['Btheta'] = (results['By'] * results['x'] - results['Bx'] * results['y']) / results['r']

    return results

results = compileResults(files)
results.to_csv('results/compiledResults.csv')

fields = ['Bx', 'By', 'Bz', 'magnitude', 'Br', 'Btheta']

for z, z_grp in results.groupby('z'):
    x = z_grp['x'].to_numpy()
    y = z_grp['y'].to_numpy()
    r = z_grp['r'].to_numpy()
    theta = z_grp['theta'].to_numpy()

    for field in fields:
        B = z_grp[field].to_numpy()

        fig = plt.figure()
        ax = fig.add_subplot()
        ax.set_aspect('equal', adjustable='box')
        plt.tricontourf(x, y, B, levels=20)
        plt.colorbar(label=f'{field} (T)')
        plt.axhline(color='white')
        plt.axvline(color='white')
        plt.xlabel('x (cm)')
        plt.ylabel('y (cm)')
        plt.title(f'z={z} cm')
        plt.grid('on')
        plt.savefig(f'images/{field}_z={z}_cm.png', dpi=200)

        ## Interpolate to find the location of the field center
        if field == 'Br' or field == 'Bz':
            B_function = interpolate.interp2d(np.unique(x), np.unique(y), B, kind='cubic')
            x_interp = np.linspace(min(x), max(x), 200)
            y_interp = np.linspace(min(y), max(y), 200)
            B_interp = B_function(x_interp, y_interp)

            if field == 'Br':
                yMaxIndex, xMaxIndex = np.where(np.abs(B_interp) == np.amin(np.abs(B_interp)))
            if field == 'Bz':
                yMaxIndex, xMaxIndex = np.where(np.abs(B_interp) == np.amax(np.abs(B_interp)))
            xMax = x_interp[xMaxIndex]
            yMax = y_interp[yMaxIndex]
            print(f'The {field}-field interpolated center of the plane z={z} cm is at (x, y) = {xMax}, {yMax}')

        ## Plots showing symmetry
        if field == 'Bz':
            xLim = 32
            yLim = 16
            xSteps = int(xLim / 2 + 1) # spacing of 4 cm
            ySteps = int(yLim / 2 + 1) # spacing of 4 cm
            x_interp = np.linspace(-xLim, xLim, xSteps)
            y_interp = np.linspace(-yLim, yLim, ySteps)
            B_interp = B_function(x_interp, y_interp)

            # Delta B is the difference between opposite points around the center
            DeltaB = B_interp - np.flip(B_interp)
            DeltaBNormalized = DeltaB / B_interp
            fig = plt.figure()
            ax = fig.add_subplot()
            ax.set_aspect('equal', adjustable='box')
            plt.contourf(x_interp, y_interp, DeltaBNormalized, levels=10)
            plt.colorbar(label=f'Normalized symmetry $\Delta${field}/{field}')
            plt.axhline(color='white')
            plt.axvline(color='white')
            plt.xlabel('x (cm)')
            plt.ylabel('y (cm)')
            plt.title(f'z={z} cm')
            plt.grid('on')
            plt.savefig(f'images/Delta{field}_z={z}_cm.png', dpi=200)

## Flux lines streamplot
z_plane = 0.0 # cm
streamplotResults = results[results['x'] == 0.8]
x = np.linspace(min(streamplotResults['x']), max(streamplotResults['x']), 23)
y = np.linspace(min(streamplotResults['y']), max(streamplotResults['y']), 16)
z = np.linspace(min(streamplotResults['z']), max(streamplotResults['z']), 5)
Z, Y = np.meshgrid(z, y)
By = np.reshape(streamplotResults['By'].to_numpy(), (16, 5))
Bz = np.reshape(streamplotResults['Bz'].to_numpy(), (16, 5))
## Flux lines
plt.figure()
plt.streamplot(Z, Y, Bz, By, density=0.5)
ax.set_aspect('equal', adjustable='box')
plt.title('Flux lines at x=0.8')
plt.xlabel('z (cm)')
plt.ylabel('y (cm)')
plt.savefig('images/flux_lines.png', dpi=200)

## Isocontours
isocontourFields = ['Br', 'Bz']
for field in isocontourFields:
    fig = go.Figure(data=go.Isosurface(
        x=results['x'].to_numpy(),
        y=results['y'].to_numpy(),
        z=results['z'].to_numpy(),
        value=results[field].to_numpy(),
        opacity=0.6,
        surface_count=20,
        caps=dict(x_show=False, y_show=False, z_show=False),
        colorscale='BlueRed',
        colorbar={'title': field}
    ))

    fig.show()


## Linear plot along central axis
os.listdir(folder)
linearFiles = [file for file in os.listdir(folder) if file.endswith('Bfield_linear.csv')]
linearResults = compileResults(linearFiles)
linearResults.to_csv('results/linearResultsCompiled.csv')

linearResults['dBdz'] = linearResults['Bz'].diff()/linearResults['z'].diff() * 20
linearFields = ['Bx', 'By', 'Bz', 'magnitude', 'dBdz']


for (x, y), xy_grp in linearResults.groupby(['x', 'y']):
    fig, ax = plt.subplots()
    for field in linearFields:
        xy_grp.plot(ax=ax, x='z', y=field)

    ax.axvline(color='black')
    ax.set_xlabel('z (cm)')
    ax.set_ylabel('Magnetic Field (T)')
    ax.set_title(f'(x, y)=({x}, {y}) cm')
    ax.grid('on')
    fig.savefig('images/linearField.png', dpi=200)
