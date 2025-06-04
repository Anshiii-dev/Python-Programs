# Computer Activity Tracker

A simple application that takes periodic screenshots of your computer screen for activity tracking purposes.

## Features

- User-friendly GUI interface
- Customizable screenshot interval (in seconds)
- Choose where to save screenshots
- View status of tracking
- Open screenshots folder directly from the app
- Timestamps in screenshot filenames

## How to Run

1. Ensure you have Python installed on your computer
2. Navigate to the app directory in your terminal/command prompt
3. Run the application with:
   ```
   python main.py
   ```

## Creating an Executable

If you want to create a standalone executable:

1. Install PyInstaller:
   ```
   pip install pyinstaller
   ```

2. Create the executable:
   ```
   pyinstaller --onefile --windowed main.py
   ```

3. Find the executable in the `dist` folder

## Usage

1. Set your desired screenshot interval (in seconds)
2. Choose where to save the screenshots
3. Click "Start Tracking" to begin
4. Click "Stop Tracking" to stop the process
5. Use "Open Screenshots Folder" to view your captured screenshots

## Note

This application runs in the background after you start tracking. It will continue to take screenshots until you stop tracking or close the application.
