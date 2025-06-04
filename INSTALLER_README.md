# Activity Tracker Installer

This folder contains scripts to create an installer for the Activity Tracker application.

## Using the Inno Setup Script

### Option 1: Automated Process

1. Run the `build_inno_installer.py` script:
   ```
   python build_inno_installer.py
   ```

   This script will:
   - Check if Inno Setup is installed
   - If not, offer to download and install it
   - Build the installer using the Inno Setup script

2. The installer will be generated in the `installer` folder as `ActivityTracker_Setup.exe`

### Option 2: Manual Process

1. Download and install Inno Setup from [https://jrsoftware.org/isinfo.php](https://jrsoftware.org/isinfo.php)

2. Open the `ActivityTracker.iss` file with Inno Setup Compiler

3. Click on "Build" or press F9 to compile the installer

4. The installer will be generated in the `installer` folder

## Inno Setup Script Details

The `ActivityTracker.iss` file contains the following configuration:

- Default installation directory in Program Files
- Shortcuts creation options (Desktop, Start Menu)
- Proper file permissions for the screenshots folder
- Uninstallation cleanup process

## Customization

You can modify the script to customize:

- Publisher name and URL (currently set to "Your Name" and "https://yourwebsite.com/")
- Installation options
- Application version number
- Additional files to include

Just edit the `ActivityTracker.iss` file using a text editor or the Inno Setup Script Editor.
