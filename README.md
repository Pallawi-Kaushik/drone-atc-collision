# 🛰️ Drone ATC Collision Simulation

This project simulates Air Traffic Control for drones with 3D collision detection and ML-based path adjustments.

## 🎯 Features

- 7 drones flying simultaneously
- 3 intentional collisions (A↔B, C↔D, E↔F)
- 1 collision-free drone (G)
- 3-minute animation duration
- Collision markers with red 'X' and labels

## 📁 Files Included

| File                             | Description                                |
|----------------------------------|--------------------------------------------|
| `Drone_ATC_Animation.py`         | Python script to simulate and animate      |
| `Drone_ATC_Animation_Colab.ipynb`| Google Colab-compatible notebook           |
| `flight_data.csv`               | Simulated flight paths and timestamps      |

## ▶️ How to Use

### 📍 Option 1: Local (Python)

> ⚠️ **Note**: Make sure you have `ffmpeg` installed on your system. It's required to save the `.mp4` animation files from the `.py` script. See installation instructions below.

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Make sure FFmpeg is installed (`sudo apt install ffmpeg` or use your OS equivalent).

3. Run the simulation:

```bash
python Drone_ATC_Animation.py
```

This generates:
- `drone_animation.mp4`: original flights
- `drone_resolution_animation.mp4`: ML-adjusted paths

---

### 🌐 Option 2: Google Colab

1. Upload the notebook and CSV to [Colab](https://colab.research.google.com/)
2. Run all cells to simulate and download both MP4 animations

---

## 📽️ Sample Preview

- Red markers show collision zones
- Labels like `COLLISION: A & B` appear at impact

---

## 👨‍💻 Author

Built by a Robotics & AI enthusiast. Supports drone path safety via ML-predicted route deconfliction.



---

## 🛠 FFmpeg Installation

### For Windows:
- Use Chocolatey: `choco install ffmpeg`
- Or download manually from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) and add the `/bin` folder to PATH

### For macOS:
```bash
brew install ffmpeg
```

### For Ubuntu/Debian:
```bash
sudo apt update
sudo apt install ffmpeg
```

### To Verify:
Run in terminal or CMD:
```bash
ffmpeg -version
```


## 🖼️ Animation Previews

### Collision Scenario: Original Paths
![Original Animation Preview](preview_original.png)

### ML-Suggested Path Correction
![Adjusted Animation Preview](preview_adjusted.png)

> These previews show how collisions are marked with a red X and labeled with the conflicting drones.


## 📄 License

This project is licensed under the **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)**.

You may:
- ✅ Use, copy, remix, and adapt the code
- ❌ But NOT use it for commercial purposes

> For commercial licensing, please [contact the author](mailto:youremail@example.com).
