import tkinter as tk
from tkinter import ttk
import speedtest as st
import threading
import time

# Font setting for the GUI
FONT_NAME = "Comic Sans MS"


class NetworkSpeedMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Speed Monitor")
        self.root.geometry("500x300")
        self.root.configure(bg="#2C2F33")  # Dark theme

        # Customize progress bar
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TProgressbar", thickness=15, troughcolor="#23272A", background="#7289DA")

        # UI Components
        self.setup_ui()

    def setup_ui(self):
        # Title Label
        title_label = tk.Label(self.root, text="Network Speed Monitor", font=(FONT_NAME, 18, "bold"), bg="#2C2F33",
                               fg="white")
        title_label.pack(pady=10)

        # Speed Labels
        self.download_label = tk.Label(self.root, text="Download Speed: -- Mbps", font=(FONT_NAME, 12), bg="#2C2F33",
                                       fg="white")
        self.download_label.pack(pady=5)

        self.upload_label = tk.Label(self.root, text="Upload Speed: -- Mbps", font=(FONT_NAME, 12), bg="#2C2F33",
                                     fg="white")
        self.upload_label.pack(pady=5)

        # Start Test Button
        self.start_button = tk.Button(self.root, text="Start Test", font=(FONT_NAME, 12, "bold"), bg="#7289DA",
                                      fg="white",
                                      activebackground="#99AAB5", activeforeground="white", cursor="hand2",
                                      command=self.start_test)
        self.start_button.pack(pady=10)

        # Smooth Progress Bar
        self.progress_bar = ttk.Progressbar(self.root, style="TProgressbar", orient="horizontal", length=400,
                                            mode="determinate")
        self.progress_bar.pack(pady=10)

    def start_test(self):
        # Disable button and reset progress
        self.start_button.config(state="disabled", text="Testing...")
        self.progress_bar["value"] = 0
        self.download_label.config(text="Download Speed: -- Mbps")  # Reset download speed
        self.upload_label.config(text="Upload Speed: -- Mbps")  # Reset upload speed

        # Start the speed test in a new thread
        threading.Thread(target=self.run_speed_test).start()

    def run_speed_test(self):
        try:
            st_test = st.Speedtest()

            # Update progress for download
            download_speed = st_test.download() / 1_000_000  # Convert to Mbps
            self.update_progress_bar(0, 50, 15)  # Fill to 50% for download over 60 seconds
            self.update_ui(download_speed=download_speed)

            # Ensure progress bar reaches 50% after download
            self.progress_bar["value"] = 50

            # Update progress for upload
            upload_speed = st_test.upload() / 1_000_000  # Convert to Mbps
            self.update_progress_bar(50, 100, 15)  # Fill from 50% to 100% over 60 seconds
            self.update_ui(upload_speed=upload_speed)

            # Ensure progress bar reaches 100% after upload
            self.progress_bar["value"] = 100

        except Exception as e:
            print("Error during speed test:", e)

        # Re-enable button after test
        self.start_button.config(state="normal", text="Restart Test")

    def update_ui(self, download_speed=None, upload_speed=None):
        if download_speed is not None:
            self.download_label.config(text=f"Download Speed: {download_speed:.2f} Mbps")
        if upload_speed is not None:
            self.upload_label.config(text=f"Upload Speed: {upload_speed:.2f} Mbps")

    def update_progress_bar(self, start_value, end_value, duration):
        """Update progress bar smoothly from start_value to end_value."""
        total_steps = 100  # Total steps for smooth progress
        increment = (end_value - start_value) / total_steps  # Increment per step
        delay = duration / total_steps  # Calculate delay per step

        for step in range(total_steps + 1):
            value = start_value + step * increment
            self.progress_bar["value"] = value
            self.root.update_idletasks()
            time.sleep(delay)  # Control speed of progress


# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkSpeedMonitor(root)
    root.mainloop()
