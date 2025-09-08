# 🌙 Skyfield-Moon-Tracker

<img width="2048" height="1747" alt="Moon tracker" src="https://github.com/user-attachments/assets/a4da5093-582d-435a-adcc-70b9d3dd43f7" />

*<p align="center">A high-precision command-line tool for calculating and visualizing the phase of the Moon for any given date.</p>*

This project uses the powerful **Skyfield** astronomical library to ensure calculations are based on the professional-grade JPL DE421 ephemeris. It generates a detailed multi-panel analysis image, a summary text file, and attempts to download a NASA photograph of the Moon for the specified day.

🔭 **Use Case**: Perfect for astronomy enthusiasts, educators, developers, and anyone curious about the precise state of the Moon on a particular day.

🧠 **Technologies**:
![Skyfield](https://img.shields.io/badge/Skyfield-1.x-blue.svg)
![NumPy](https://img.shields.io/badge/NumPy-1.x-yellow.svg)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.x-purple.svg)
![Requests](https://img.shields.io/badge/Requests-2.x-brightgreen.svg)

---

## 🦄 _**Code Requirements**_
- Python 3.8 or later
- A working virtual environment (`venv`) for isolation
- Required libraries: `skyfield`, `numpy`, `matplotlib`, `requests`

---

## 🔍 _**Problem Statement**_

While many websites show the Moon's phase, they often lack detailed astronomical data or comprehensive visualizations. This project provides an accurate, offline-capable tool that generates a rich, multi-faceted report for any date, combining precise scientific data with an easy-to-understand visual format.

---

## 🎯 _**Key Features**_

- 🛰️ **High-Precision Calculations:** Uses Skyfield and the JPL DE421 ephemeris for professional-grade accuracy.
- 📊 **Comprehensive Visualization:** Generates a 4-panel chart showing the Moon's appearance, orbital position, timeline status, and detailed data.
- 🚀 **NASA Image Fetching:** Attempts to download a real photograph of the Moon for the given day from NASA's SVS database.
- 📝 **Detailed Text Summary:** Creates a `.txt` file with all key data points, including illumination, elongation, moon age, and upcoming phase estimates.
- 📂 **Organized Output:** Automatically creates a date-stamped folder for each query to keep all generated files tidy.

---

## 🛠️ _**Tech Stack**_
- **Python 3.x** - Core programming language.
- **Skyfield** - Performs all core astronomical calculations for celestial body positions.
- **NumPy** - Handles numerical operations and array manipulation for calculations.
- **Matplotlib** - Creates the detailed 4-panel data visualization chart.
- **Requests** - Manages HTTP requests to fetch the NASA Moon image.

---

## 📌 _**How It Works**_
- The user provides a date in `YYYY-MM-DD` format.
- `Skyfield` calculates the geocentric positions of the Sun and Moon.
- The **elongation angle** and **illumination percentage** are derived from these positions.
- `Matplotlib` uses this data to construct the four-part visualization.
- The script attempts to find and download a matching NASA SVS image.
- All outputs (PNG chart, JPG image, TXT summary) are saved into a new, date-specific folder.

---

## 👨‍🔬 _**Algorithm Overview**_
The system's accuracy relies on fundamental principles of positional astronomy.

### 🪐 _**JPL Ephemeris**_
The project loads the **DE421 ephemeris** from the Jet Propulsion Laboratory (JPL). This is a high-precision data file that provides the exact positions of planets and other celestial bodies over time.

### 📐 _**Geocentric Elongation**_
The core of the phase calculation is determining the **elongation**, which is the angle between the Sun and the Moon as seen from the center of the Earth.
* **0° Elongation** = New Moon
* **Waxing Crescent**: 0° to 90°
* **90° Elongation** = First Quarter
* **Waxing Gibbous**: 90° to 180°
* **180° Elongation** = Full Moon
* **Waning Gibbous**: 180° to 270°
* **270° Elongation** = Last Quarter
* **Waning Crescent**: 270° to 360°

### 💡 _**Illumination Formula**_
The fraction of the Moon's visible surface that is illuminated is calculated using the phase angle ($i$, which is equivalent to the elongation).

**Formula:**
```latex
k = (1 + cos(i)) / 2
```
Where `k` is the illuminated fraction (0 to 1) and `i` is the phase angle in radians.

---

## 🐉 _**Execution Steps**_

1. **Clone the repository and install requirements**
   ```bash
   git clone [https://github.com/your-username/Skyfield-Moon-Tracker.git](https://github.com/your-username/Skyfield-Moon-Tracker.git)
   cd Skyfield-Moon-Tracker
   pip install -r requirements.txt
   ```

2. **Run the Tracker**
   The script runs in an interactive command-line mode.
   ```bash
   python moon_tracker.py
   ```
   > Enter a date when prompted (e.g., `2025-09-07`). The output files will be saved in the `generated_images/` directory.

---

## 🗂 _**Folder Structure**_
```
Skyfield-Moon-Tracker
│
├── python moon_tracker.py           # Main executable script
├── requirements.txt                 # Project dependencies
├── generated_images/                # Automatically created output directory
│   └── 2025-09-07_Sunday/           # Example date-stamped folder
│       ├── 01_Comprehensive_Moon_Analysis.png
│       ├── 02_NASA_Moon_Image.jpg
│       └── 03_Moon_Info.txt
│
├── architecture.md                  # System architecture diagram and details
├── LICENSE                          # Project license file
└── README.md                        # This file
```

---

## ⚖️ _**License**_

This project is licensed under the **MIT License**. This means you are free to use, copy, modify, merge, publish, distribute, and sell copies of the software. The only requirement is to include the original copyright notice and a copy of the license in any substantial portions of the software.

For more details, see the [LICENSE](LICENSE) file in the repository.
