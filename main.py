import pyautogui
import time
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
from datetime import datetime
from PIL import Image, ImageTk

class TrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Activity Tracker")
        self.root.geometry("600x500")  # Increased default size for better visibility
        self.root.minsize(500, 400)    # Set minimum window size
        self.root.resizable(True, True)
        
        # Set application icon - multiple methods for better compatibility
        try:
            # Method 1: iconphoto (works on most Unix systems)
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tracking-app.png")
            if os.path.exists(icon_path):
                icon_image = ImageTk.PhotoImage(Image.open(icon_path))
                self.root.iconphoto(True, icon_image)
                
                # Method 2: iconbitmap (works better on Windows)
                if os.name == 'nt':  # Windows
                    try:
                        # Convert to ICO format temporarily in memory if using PNG
                        from PIL import Image
                        icon = Image.open(icon_path)
                        icon_ico = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp_icon.ico")
                        icon.save(icon_ico, format='ICO', sizes=[(32, 32)])
                        self.root.iconbitmap(icon_ico)
                        # Clean up temporary file
                        if os.path.exists(icon_ico):
                            os.remove(icon_ico)
                    except Exception:
                        pass
        except Exception as e:
            print(f"Could not load icon: {e}")
        
        # Initialize variables
        self.is_tracking = False
        self.tracking_thread = None
        self.interval = tk.IntVar(value=10)  # Default 10 seconds
        self.save_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "screenshots")
        # Create save directory if it doesn't exist
        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)
        
        self.create_widgets()
        
    def create_widgets(self):
        # Create main frame with padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure row and column weights to make the frame responsive
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Title with improved styling
        title_label = ttk.Label(main_frame, text="Activity Tracker", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        settings_frame = ttk.LabelFrame(main_frame, text="Settings")
        settings_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Interval setting
        interval_frame = ttk.Frame(settings_frame)
        interval_frame.pack(fill=tk.X, pady=5)
        
        interval_label = ttk.Label(interval_frame, text="Screenshot Interval (seconds):")
        interval_label.pack(side=tk.LEFT, padx=5)
        
        interval_entry = ttk.Entry(interval_frame, textvariable=self.interval, width=5)
        interval_entry.pack(side=tk.LEFT, padx=5)
        
        # Directory setting
        dir_frame = ttk.Frame(settings_frame)
        dir_frame.pack(fill=tk.X, pady=5)
        
        dir_label = ttk.Label(dir_frame, text="Save Directory:")
        dir_label.pack(side=tk.LEFT, padx=5)
        
        self.dir_entry = ttk.Entry(dir_frame)
        self.dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.dir_entry.insert(0, self.save_directory)
        
        browse_button = ttk.Button(dir_frame, text="Browse", command=self.browse_directory)
        browse_button.pack(side=tk.LEFT, padx=5)
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="Status")
        status_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.status_label = ttk.Label(status_frame, text="Tracking: Not started")
        self.status_label.pack(pady=5)
        
        self.last_screenshot_label = ttk.Label(status_frame, text="Last Screenshot: None")
        self.last_screenshot_label.pack(pady=5)
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.start_button = ttk.Button(button_frame, text="Start Tracking", command=self.start_tracking)
        self.start_button.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        self.stop_button = ttk.Button(button_frame, text="Stop Tracking", command=self.stop_tracking, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        # Bottom buttons frame
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(fill=tk.X, padx=10, pady=(10, 0), side=tk.BOTTOM)
        
        # Open folder button
        open_folder_button = ttk.Button(main_frame, text="Open Screenshots Folder", command=self.open_folder)
        open_folder_button.pack(fill=tk.X, padx=10, pady=5)
        
        # Exit button
        exit_button = ttk.Button(main_frame, text="Exit", command=self.confirm_exit)
        exit_button.pack(fill=tk.X, padx=10, pady=5)
        
    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.save_directory = directory
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, directory)
    
    def open_folder(self):
        try:
            os.startfile(self.save_directory)
        except:
            messagebox.showerror("Error", "Could not open the folder.")
    
    def start_tracking(self):
        # Update UI state
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_label.config(text="Tracking: Active")
        
        # Get settings
        try:
            interval = self.interval.get()
            if interval < 1:
                raise ValueError("Interval must be at least 1 second")
                
            # Update save directory from entry
            self.save_directory = self.dir_entry.get()
            if not os.path.exists(self.save_directory):
                os.makedirs(self.save_directory)
                
        except Exception as e:
            messagebox.showerror("Invalid Settings", str(e))
            self.stop_tracking()
            return
        
        # Set tracking flag and start thread
        self.is_tracking = True
        self.tracking_thread = threading.Thread(target=self.tracking_loop)
        self.tracking_thread.daemon = True
        self.tracking_thread.start()
    
    def stop_tracking(self):
        self.is_tracking = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="Tracking: Stopped")
    
    def tracking_loop(self):
        while self.is_tracking:
            try:
                # Take screenshot
                screen = pyautogui.screenshot()
                
                # Generate filename with timestamp
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                filename = f"screenshot_{timestamp}.png"
                filepath = os.path.join(self.save_directory, filename)
                
                # Save screenshot
                screen.save(filepath)
                
                # Update last screenshot label on the main thread
                self.root.after(0, self.update_last_screenshot_label, timestamp)
                
                # Sleep for the specified interval
                time.sleep(self.interval.get())
                
            except Exception as e:
                # Update status label on the main thread
                self.root.after(0, self.show_error, str(e))
                break
    
    def update_last_screenshot_label(self, timestamp):
        self.last_screenshot_label.config(text=f"Last Screenshot: {timestamp}")
    
    def show_error(self, error_message):
        messagebox.showerror("Error", f"An error occurred: {error_message}")
        self.stop_tracking()
    
    def confirm_exit(self):
        if self.is_tracking:
            if messagebox.askyesno("Confirm Exit", "Tracking is active. Are you sure you want to exit?"):
                self.root.destroy()
        else:
            self.root.destroy()

def main_entry_point():
    # Create the main window
    root = tk.Tk()
    app = TrackerApp(root)
    
    # Start the main event loop
    root.mainloop()

if __name__ == "__main__":
    main_entry_point()