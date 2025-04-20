# drone_atc_app.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from PIL import Image
import imageio.v2 as imageio
import io

class Drone:
    def __init__(self, drone_id, path_coords, velocity):
        self.drone_id = drone_id
        self.path_coords = path_coords
        self.velocity = velocity

def detect_collision(drones, threshold=10):
    collisions = []
    for i in range(len(drones)):
        for j in range(i + 1, len(drones)):
            drone_a = drones[i]
            drone_b = drones[j]
            for p1 in drone_a.path_coords:
                for p2 in drone_b.path_coords:
                    if abs(p1[3] - p2[3]) < 60 and np.linalg.norm(p1[:3] - p2[:3]) < threshold:
                        collisions.append({'location': p1, 'label': f"{drone_a.drone_id} & {drone_b.drone_id}"})
                        break
    return collisions

def visualize_drones(drones, collisions, filename: str):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim(0, 150)
    ax.set_ylim(0, 150)
    ax.set_zlim(0, 100)
    ax.set_title("Drone Flight Paths")

    colors = plt.colormaps.get_cmap('tab10')
    paths = [np.array([coord[:3] for coord in drone.path_coords]) for drone in drones]

    scatters = [ax.plot([], [], [], 'o', label=drone.drone_id, color=colors(i % 10))[0]
                for i, drone in enumerate(drones)]
    lines = [ax.plot([], [], [], '-', alpha=0.3, color=colors(i % 10))[0]
             for i in range(len(drones))]

    flash_frames = {}
    for col in collisions:
        ts = int(col['location'][3])
        flash_frames[ts] = (col['location'][:3], col['label'])

    text_elements = []

    def update(frame):
        nonlocal text_elements
        for elem in text_elements:
            try: elem.remove()
            except: pass
        text_elements = []

        for i, path in enumerate(paths):
            if frame < len(path):
                x, y, z = path[frame]
                scatters[i].set_data([x], [y])
                scatters[i].set_3d_properties([z])
                lines[i].set_data(path[:frame + 1, 0], path[:frame + 1, 1])
                lines[i].set_3d_properties(path[:frame + 1, 2])

        if frame in flash_frames:
            (x, y, z), label = flash_frames[frame]
            txt = ax.text(x, y, z + 5, f"COLLISION\n{label}", color='red', fontsize=11, ha='center')
            marker = ax.plot([x], [y], [z], marker='x', markersize=10, color='red')[0]
            text_elements.extend([txt, marker])

    max_len = max(len(p) for p in paths)

    images = []
    for frame in range(max_len):
        update(frame)
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img = Image.open(buf)
        images.append(img.convert("RGB"))
        buf.close()

    # Save to disk
    images[0].save(filename, save_all=True, append_images=images[1:], duration=833, loop=0)

    # Save to in-memory buffer
    gif_buf = io.BytesIO()
    images[0].save(gif_buf, save_all=True, append_images=images[1:], format='GIF', duration=833, loop=0)
    gif_buf.seek(0)
    plt.close(fig)
    return gif_buf


# -------------------------------
# Streamlit App
# -------------------------------
st.set_page_config(page_title="Drone ATC Animation", layout="wide")
st.title("Drone ATC Simulation & Collision Detection")

# --- Load Data ---
df = pd.read_csv("flight_data.csv")
df['timestamp'] = pd.to_datetime(df['timestamp'])

drones = []
adjusted_drones = []

for drone_id in df['flight_id'].unique():
    df_d = df[df['flight_id'] == drone_id].sort_values(by='timestamp')
    coords = [np.array([r.x, r.y, r.z, r.timestamp.timestamp()]) for r in df_d.itertuples()]
    drones.append(Drone(drone_id, coords, 10))
    adj_coords = [np.array([x + 5, y + 5, z + 10, t]) for x, y, z, t in coords]
    adjusted_drones.append(Drone(f"{drone_id}_ML", adj_coords, 10))

# --- Collision Detection ---
collisions = detect_collision(drones)

# --- Generate GIFs ---
with st.spinner("Rendering Raw Drone Animation..."):
    gif1 = visualize_drones(drones, collisions, "drone_animation.gif")

with st.spinner("Rendering ML-Resolved Drone Animation..."):
    gif2 = visualize_drones(adjusted_drones, collisions, "drone_resolution_animation.gif")

# --- Display: Step-by-Step Mode ---
st.markdown("### 🟠 Step 1: Raw Drone Path Animation")
st.image(gif1, use_column_width=True)
st.download_button("📥 Download Raw Animation", data=gif1, file_name="drone_animation.gif")

if st.button("▶️ Show ML-Resolved Drone Animation"):
    st.markdown("### 🟢 Step 2: ML-Resolved Drone Path Animation")
    st.image(gif2, use_column_width=True)
    st.download_button("📥 Download Resolved Animation", data=gif2, file_name="drone_resolution_animation.gif")
