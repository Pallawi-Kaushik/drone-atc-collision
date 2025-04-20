# 🛰️ Drone ATC Collision Simulation

This project simulates Air Traffic Control for drones with 3D collision detection and ML-based path adjustments.

---

## 🎯 Features

- 7 drones flying simultaneously  
- 3 intentional collisions (A↔B, C↔D, E↔F)  
- 1 collision-free drone (G)  
- 3-minute animation duration  
- Collision markers with red 'X' and labels  

---

## 📁 Files Included

| File                      | Description                           |
|---------------------------|---------------------------------------|
| `Drone_ATC_Animation.py`  | Python script to simulate and animate |
| `flight_data.csv`         | Simulated flight paths and timestamps |

---

## ▶️ How to Use

### 📍 Run Locally (Python)

> ⚠️ **Note**: Ensure `ffmpeg` is installed. It’s required to generate `.mp4` animations from the script. See install instructions below.

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Ensure FFmpeg is installed:

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows (via Chocolatey)
choco install ffmpeg
```

3. Run the simulation:

```bash
python Drone_ATC_Animation.py
```

This generates:
- `drone_animation.mp4`: Original flight paths  
- `drone_resolution_animation.mp4`: ML-adjusted deconflicted paths  

---

## 📽️ Sample Preview

- Red markers indicate collision zones  
- Labels like `COLLISION: A & B` highlight impact points  

---

## 🖼️ Animation Previews

### Collision Scenario: Original Paths  
![Original Animation Preview](preview_original.png)

### ML-Suggested Path Correction  
![Adjusted Animation Preview](preview_adjusted.png)

> These visuals demonstrate where conflicts occur and how ML resolves them dynamically.

---

## 👨‍💻 Author

Built by a Robotics & AI enthusiast. Focused on drone path safety through predictive ML-powered route deconfliction.

---

## 📄 License

Licensed under **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)**.

You may:
- ✅ Use, copy, remix, and adapt the code  
- ❌ Not use it for commercial purposes  

> For commercial licensing, [contact the author](mailto:pallawikaushik7@gmail.com).
