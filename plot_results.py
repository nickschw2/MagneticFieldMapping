import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import plotly.graph_objects as go

## Field maps at constant z faces
folder = 'results/both_magnets'
files = [file for file in os.listdir(folder) if file.endswith('.csv')]
results = pd.DataFrame()
for file in files:
    filename = f'{folder}/{file}'
    results = pd.concat([results, pd.read_csv(filename)])
    # truncated_results = results[np.abs(results['x']) <= 16]
    # truncated_results = truncated_results[np.abs(results['y']) <= 16]

# Sort results by x, y, and z coordinates
results = results.sort_values(['x', 'y', 'z'])

# Add columns for normal and tangential values
results['r'] = np.sqrt(results['x'] ** 2 + results['y'] ** 2)
results['theta'] = np.arctan(results['y'] / results['x'])
results['Br'] = (results['Bx'] * results['x'] + results['By'] * results['y']) / results['r']
results['Btheta'] = (results['By'] * results['x'] - results['Bx'] * results['y']) / results['r']

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
        plt.savefig(f'images/{field}_z={z}_cm.png', dpi=150)
        
test = results[results['x'] == 0.8]
x = np.linspace(-43.2, 44.8, 23)
y = np.linspace(-16.5, 43.5, 16)
z = [-35, 0, 35]
X, Y = np.meshgrid(x, y)
Z, Y = np.meshgrid(z, y)
# Bx = np.reshape(test['Bx'].to_numpy(), (16, 23))
By = np.reshape(test['By'].to_numpy(), (16, 3))
Bz = np.reshape(test['Bz'].to_numpy(), (16, 3))
## Flux lines
plt.streamplot(Z, Y, Bz, By, density=0.5)
plt.title('Flux lines at x=0.8')
plt.xlabel('z (cm)')
plt.ylabel('y (cm)')
plt.savefig('images/flux_lines.png', dpi=150)

## Isocontours
fig = go.Figure(data=go.Isosurface(
    x=results['x'].to_numpy(),
    y=results['y'].to_numpy(),
    z=results['z'].to_numpy(),
    value=results['Br'].to_numpy(),
    opacity=0.6,
    surface_count=6,
    caps=dict(x_show=False, y_show=False, z_show=False),
    colorscale='BlueRed',
    colorbar={'title': 'Br'}
))

fig.show()
