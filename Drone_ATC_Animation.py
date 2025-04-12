# Drone ATC Animation (Offline Script)

# pip install matplotlib pandas

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from datetime import datetime

class Drone:
    def __init__(self, drone_id, path_coords, velocity):
        self.drone_id = drone_id
        self.path_coords = path_coords
        self.velocity = velocity

def detect_collision(drones, threshold=10):
    collisions = []
    for i in range(len(drones)):
        for j in range(i+1, len(drones)):
            drone_a = drones[i]
            drone_b = drones[j]
            for p1 in drone_a.path_coords:
                for p2 in drone_b.path_coords:
                    if abs(p1[3] - p2[3]) < 60 and np.linalg.norm(p1[:3] - p2[:3]) < threshold:
                        collisions.append({'location': p1, 'label': f"{drone_a.drone_id} & {drone_b.drone_id}"})
                        break
    return collisions

def visualize_drones(drones, collisions, save_path):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim(0, 150)
    ax.set_ylim(0, 150)
    ax.set_zlim(0, 100)
    ax.set_title("Drone Flight Paths")

    colors = plt.cm.get_cmap('tab10', len(drones))
    paths = [np.array([coord[:3] for coord in drone.path_coords]) for drone in drones]
    scatters = [ax.plot([], [], [], 'o', label=drone.drone_id, color=colors(i))[0] for i, drone in enumerate(drones)]
    lines = [ax.plot([], [], [], '-', alpha=0.3, color=colors(i))[0] for i in range(len(drones))]

    flash_frames = {}
    for col in collisions:
        ts = int(col['location'][3])
        flash_frames[ts] = (col['location'][:3], col['label'])

    def update(frame):
        ax.collections.clear()
        for i, path in enumerate(paths):
            if frame < len(path):
                scatters[i].set_data([path[frame][0]], [path[frame][1]])
                scatters[i].set_3d_properties([path[frame][2]])
                lines[i].set_data(path[:frame+1, 0], path[:frame+1, 1])
                lines[i].set_3d_properties(path[:frame+1, 2])

        if frame in flash_frames:
            (x, y, z), label = flash_frames[frame]
            ax.text(x, y, z + 5, f"COLLISION\n{label}", color='red', fontsize=11, ha='center')
            ax.plot([x], [y], [z], marker='x', markersize=10, color='red')

        return scatters + lines

    max_len = max(len(p) for p in paths)
    ani = animation.FuncAnimation(fig, update, frames=max_len, interval=833, blit=False)
    ani.save(save_path, writer='ffmpeg', fps=1)
    plt.close()

df = pd.read_csv("flight_data.csv")
df['timestamp'] = pd.to_datetime(df['timestamp'])

drones, adjusted_drones = [], []
for drone_id in df['flight_id'].unique():
    df_d = df[df['flight_id'] == drone_id].sort_values(by='timestamp')
    coords = [np.array([r.x, r.y, r.z, r.timestamp.timestamp()]) for r in df_d.itertuples()]
    drones.append(Drone(drone_id, coords, 10))
    adj_coords = [np.array([x+5, y+5, z+10, t]) for x, y, z, t in coords]
    adjusted_drones.append(Drone(drone_id+"_ML", adj_coords, 10))

collisions = detect_collision(drones)
visualize_drones(drones, collisions, "drone_animation.mp4")
visualize_drones(adjusted_drones, collisions, "drone_resolution_animation.mp4")
