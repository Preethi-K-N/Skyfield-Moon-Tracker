import datetime
from skyfield.api import load
import numpy as np
import matplotlib.pyplot as plt
import requests
import os


class MoonPhaseCalculator:
    def __init__(self, base_save_path=r"----Your file path to save the files----"):
        """Initialize with custom base save path for images"""
        self.base_save_path = base_save_path
        
        # Create base directory if it doesn't exist
        os.makedirs(self.base_save_path, exist_ok=True)
        
        self.ts = load.timescale()
        try:
            self.eph = load('de421.bsp')
        except Exception as e:
            print(f"❌ Error loading ephemeris: {e}")
            raise

    def create_date_folder(self, date_obj):
        """Create a folder for the specific date"""
        date_folder_name = date_obj.strftime("%Y-%m-%d_%A")  # e.g., "2024-07-01_Monday"
        date_folder_path = os.path.join(self.base_save_path, date_folder_name)
        
        # Create the date folder if it doesn't exist
        os.makedirs(date_folder_path, exist_ok=True)
        
        return date_folder_path

    def calculate_moon_phase(self, date_obj):
        """Enhanced moon phase calculation with multiple parameters"""
        t = self.ts.utc(date_obj.year, date_obj.month, date_obj.day)

        sun = self.eph['sun']
        earth = self.eph['earth'] 
        moon = self.eph['moon']

        # Get positions
        geocentric_sun = earth.at(t).observe(sun).apparent()
        geocentric_moon = earth.at(t).observe(moon).apparent()

        # Calculate elongation (angle between Sun and Moon as seen from Earth)
        elongation = geocentric_sun.separation_from(geocentric_moon).degrees

        # Calculate illumination fraction more precisely
        # This uses the actual astronomical formula
        phase_angle = np.radians(elongation)
        illumination = (1 + np.cos(phase_angle)) / 2

        # Age of moon (days since new moon) - simplified
        moon_age = (elongation / 360.0) * 29.53  # synodic month

        # Determine phase name with precise boundaries
        phase_names = {
            (0, 1): "New Moon",
            (1, 7): "Waxing Crescent", 
            (7, 8): "First Quarter",
            (8, 14): "Waxing Gibbous",
            (14, 15): "Full Moon",
            (15, 22): "Waning Gibbous", 
            (22, 23): "Last Quarter",
            (23, 29.53): "Waning Crescent"
        }

        phase_name = "Unknown"
        for (start, end), name in phase_names.items():
            if start <= moon_age < end:
                phase_name = name
                break

        return {
            'phase': phase_name,
            'illumination': illumination,
            'elongation': elongation,
            'moon_age': moon_age,
            'date': date_obj
        }

    def create_matplotlib_moon(self, moon_data, date_folder_path):
        """Create detailed matplotlib moon visualization in date folder"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 12))
        fig.patch.set_facecolor('black')

        # Main moon visualization
        ax1.set_xlim(-1.2, 1.2)
        ax1.set_ylim(-1.2, 1.2)
        ax1.set_aspect('equal')
        ax1.set_facecolor('black')

        # Draw moon outline
        moon_outline = plt.Circle((0, 0), 1, color='white', fill=False, linewidth=2)
        ax1.add_patch(moon_outline)

        # Calculate terminator position
        illumination = moon_data['illumination']
        elongation = moon_data['elongation']

        # Create realistic moon phase shape
        theta = np.linspace(0, 2*np.pi, 1000)
        x_circle = np.cos(theta)
        y_circle = np.sin(theta)

        if illumination > 0.5:
            # Gibbous or Full Moon
            ax1.fill(x_circle, y_circle, color='lightgray', alpha=0.8)

            if illumination < 0.99:  # Not quite full
                # Add terminator shadow
                shadow_pos = 2 * (illumination - 0.5)  # -1 to 1
                if "Waning" in moon_data['phase']:
                    shadow_x = np.linspace(-1, shadow_pos, 100)
                    shadow_y_pos = np.sqrt(1 - shadow_x**2)
                    shadow_y_neg = -shadow_y_pos

                    shadow_x_full = np.concatenate([shadow_x, shadow_x[::-1]])
                    shadow_y_full = np.concatenate([shadow_y_pos, shadow_y_neg[::-1]])

                    ax1.fill(shadow_x_full, shadow_y_full, color='black', alpha=0.8)
        else:
            # Crescent or New Moon
            if illumination > 0.01:  # Visible crescent
                crescent_pos = 2 * illumination - 1  # -1 to 1

                if "Waxing" in moon_data['phase']:
                    # Right side illuminated
                    x_right = np.linspace(crescent_pos, 1, 100)
                    y_right_pos = np.sqrt(1 - x_right**2) 
                    y_right_neg = -y_right_pos

                    x_crescent = np.concatenate([x_right, x_right[::-1]])
                    y_crescent = np.concatenate([y_right_pos, y_right_neg[::-1]])

                    ax1.fill(x_crescent, y_crescent, color='lightgray', alpha=0.8)

        ax1.set_title(f"{moon_data['phase']}\nIllumination: {illumination:.1%}", 
                     color='white', fontsize=14)
        ax1.axis('off')

        # Orbital diagram
        ax2.set_xlim(-1.5, 1.5) 
        ax2.set_ylim(-1.5, 1.5)
        ax2.set_aspect('equal')
        ax2.set_facecolor('black')

        # Draw orbit
        orbit_theta = np.linspace(0, 2*np.pi, 100)
        orbit_x = 1.3 * np.cos(orbit_theta)
        orbit_y = 1.3 * np.sin(orbit_theta)
        ax2.plot(orbit_x, orbit_y, 'gray', alpha=0.5, linestyle='--')

        # Earth
        earth = plt.Circle((0, 0), 0.1, color='blue')
        ax2.add_patch(earth)
        ax2.text(0, -0.2, 'Earth', color='white', ha='center', fontsize=10)

        # Moon position based on age
        moon_angle = (moon_data['moon_age'] / 29.53) * 2 * np.pi
        moon_x = 1.3 * np.cos(moon_angle)
        moon_y = 1.3 * np.sin(moon_angle)
        moon_dot = plt.Circle((moon_x, moon_y), 0.05, color='lightgray')
        ax2.add_patch(moon_dot)

        # Sun direction
        ax2.arrow(-1.4, 0, 0.3, 0, head_width=0.05, fc='yellow', ec='yellow')
        ax2.text(-1.5, 0.1, 'Sun', color='yellow', ha='center', fontsize=10)

        ax2.set_title('Moon Orbit Position', color='white', fontsize=14)
        ax2.axis('off')

        # Phase timeline
        ax3.set_xlim(0, 29.53)
        ax3.set_ylim(-0.5, 0.5)
        ax3.set_facecolor('black')

        # Draw phase timeline
        phases_timeline = [
            (0, "New"),
            (7.4, "First Quarter"), 
            (14.8, "Full"),
            (22.1, "Last Quarter"),
            (29.53, "New")
        ]

        for age, name in phases_timeline:
            ax3.axvline(age, color='white', alpha=0.5)
            ax3.text(age, 0.3, name, rotation=45, color='white', fontsize=8, ha='center')

        # Current position
        ax3.axvline(moon_data['moon_age'], color='yellow', linewidth=3)
        ax3.scatter(moon_data['moon_age'], 0, color='yellow', s=100, zorder=5)

        ax3.set_xlabel('Moon Age (days)', color='white')
        ax3.set_title('Phase Timeline', color='white', fontsize=14)
        ax3.tick_params(colors='white')
        ax3.spines['bottom'].set_color('white')
        ax3.spines['top'].set_visible(False)
        ax3.spines['right'].set_visible(False)
        ax3.spines['left'].set_visible(False)

        # Information panel
        ax4.set_xlim(0, 1)
        ax4.set_ylim(0, 1) 
        ax4.set_facecolor('black')

        info_text = f"""Moon Phase Information

Date: {moon_data['date']}
Phase: {moon_data['phase']}
Illumination: {moon_data['illumination']:.1%}
Moon Age: {moon_data['moon_age']:.1f} days
Elongation: {moon_data['elongation']:.1f}°

Next New Moon: ~{29.53 - moon_data['moon_age']:.1f} days
Next Full Moon: ~{14.8 - moon_data['moon_age'] if moon_data['moon_age'] < 14.8 else 29.53 + 14.8 - moon_data['moon_age']:.1f} days
"""

        ax4.text(0.05, 0.95, info_text, transform=ax4.transAxes, 
                fontsize=10, color='white', verticalalignment='top',
                fontfamily='monospace')
        ax4.axis('off')

        plt.tight_layout()

        # Save to date-specific folder
        filename = f"01_Comprehensive_Moon_Analysis.png"
        filepath = os.path.join(date_folder_path, filename)
        plt.savefig(filepath, facecolor='black', dpi=200, bbox_inches='tight')
        plt.close()

        return filepath

    def try_nasa_image(self, date_obj, date_folder_path):
        """Attempt to get NASA SVS moon image and save to date folder"""
        try:
            # Calculate approximate image number
            # NASA SVS images start from a base date
            base_date = datetime.date(2000, 1, 1)
            days_since = (date_obj - base_date).days

            # Try different image number calculations
            for offset in [0, 1, -1, 365, -365]:
                image_num = str((days_since + offset) % 8760 + 1).zfill(4)

                urls_to_try = [
                    f"https://svs.gsfc.nasa.gov/vis/a000000/a004400/a004442/frames/730x730_1x1_30p/moon.{image_num}.jpg",
                    f"https://svs.gsfc.nasa.gov/vis/a000000/a004700/a004768/frames/730x730_1x1_30p/moon.{image_num}.jpg",
                    f"https://svs.gsfc.nasa.gov/vis/a000000/a005000/a005048/frames/730x730_1x1_30p/moon.{image_num}.jpg"
                ]

                for url in urls_to_try:
                    try:
                        response = requests.get(url, timeout=5)
                        if response.status_code == 200:
                            filename = f"02_NASA_Moon_Image.jpg"
                            filepath = os.path.join(date_folder_path, filename)
                            with open(filepath, 'wb') as f:
                                f.write(response.content)
                            return filepath
                    except:
                        continue

            return None

        except Exception as e:
            return None

    def create_info_file(self, moon_data, date_folder_path):
        """Create a text file with detailed moon information"""
        info_content = f"""🌙 MOON PHASE INFORMATION 🌙
═══════════════════════════════════════════════════════

📅 Date: {moon_data['date'].strftime('%A, %B %d, %Y')}
🌙 Phase: {moon_data['phase']}
💡 Illumination: {moon_data['illumination']:.2%} ({moon_data['illumination']*100:.1f}%)
📏 Moon Age: {moon_data['moon_age']:.2f} days since new moon
📐 Elongation: {moon_data['elongation']:.2f}°

🔮 UPCOMING PHASES:
═══════════════════════════════════════════════════════
Next New Moon: ~{29.53 - moon_data['moon_age']:.1f} days
Next Full Moon: ~{14.8 - moon_data['moon_age'] if moon_data['moon_age'] < 14.8 else 29.53 + 14.8 - moon_data['moon_age']:.1f} days

📊 TECHNICAL DATA:
═══════════════════════════════════════════════════════
Synodic Month: 29.53 days (average)
Current Position in Cycle: {(moon_data['moon_age']/29.53)*100:.1f}%
Phase Angle: {moon_data['elongation']:.2f}°

📁 FILES IN THIS FOLDER:
═══════════════════════════════════════════════════════
• 01_Comprehensive_Moon_Analysis.png - Detailed 4-panel visualization
• 02_NASA_Moon_Image.jpg - Real NASA moon photograph (if available)
• 03_Moon_Info.txt - This information file

Generated on: {datetime.datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}
"""
        
        filename = "03_Moon_Info.txt"
        filepath = os.path.join(date_folder_path, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(info_content)
        
        return filepath


def main():
    print("🌙 Comprehensive Moon Phase Calculator 🌙")
    print("=" * 50)

    # Initialize calculator
    base_save_path = r"___your_file_path_to_save_files___"
    calculator = MoonPhaseCalculator(base_save_path)

    while True:
        date_input = input("\nEnter date (YYYY-MM-DD) or 'quit': ").strip()

        if date_input.lower() == 'quit':
            print("🌙 Thank you for using the Moon Phase Calculator!")
            break

        try:
            date_obj = datetime.datetime.strptime(date_input, "%Y-%m-%d").date()

            print(f"\n🔍 Calculating moon phase for {date_obj}...")

            # Create date-specific folder
            date_folder_path = calculator.create_date_folder(date_obj)

            # Calculate moon phase
            moon_data = calculator.calculate_moon_phase(date_obj)

            # Display results
            print("="*50)
            print(f"📅 Date: {moon_data['date']}")
            print(f"🌙 Phase: {moon_data['phase']}")
            print(f"💡 Illumination: {moon_data['illumination']:.1%}")
            print(f"📏 Moon Age: {moon_data['moon_age']:.1f} days")
            print(f"📐 Elongation: {moon_data['elongation']:.1f}°")
            print("="*50)

            # Create comprehensive visualization
            matplotlib_file = calculator.create_matplotlib_moon(moon_data, date_folder_path)
            print(f"🎨 Generated comprehensive visualization")

            # Try to get NASA image
            nasa_file = calculator.try_nasa_image(date_obj, date_folder_path)
            if nasa_file:
                print(f"🛰️ NASA image downloaded")

            # Create info file
            info_file = calculator.create_info_file(moon_data, date_folder_path)

            print(f"✨ All files saved in organized folder")

        except ValueError:
            print("❌ Invalid date format. Please use YYYY-MM-DD")
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()