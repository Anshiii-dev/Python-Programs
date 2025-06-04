# Script to download, install Inno Setup and build the Activity Tracker installer
import os
import sys
import subprocess
import winreg
import urllib.request
import time
import platform

# Configuration settings
INNO_SETUP_URL = "https://jrsoftware.org/download.php/is.exe"
INNO_SETUP_INSTALLER = "inno_setup_installer.exe"
ISS_SCRIPT_PATH = "ActivityTracker.iss"

def is_inno_setup_installed():
    """Check if Inno Setup is installed by looking for its registry key"""
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Inno Setup 6_is1") as key:
            return True
    except WindowsError:
        return False

def get_inno_setup_compiler_path():
    """Get the path to the Inno Setup compiler (ISCC.exe)"""
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Inno Setup 6_is1") as key:
            install_path = winreg.QueryValueEx(key, "InstallLocation")[0]
            compiler_path = os.path.join(install_path, "ISCC.exe")
            if os.path.exists(compiler_path):
                return compiler_path
            
    except WindowsError:
        pass
        
    # Try common installation paths
    common_paths = [
        r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
        r"C:\Program Files\Inno Setup 6\ISCC.exe"
    ]
    
    for path in common_paths:
        if os.path.exists(path):
            return path
    
    return None

def download_inno_setup():
    """Download the Inno Setup installer"""
    print("Downloading Inno Setup installer...")
    try:
        urllib.request.urlretrieve(INNO_SETUP_URL, INNO_SETUP_INSTALLER)
        return True
    except Exception as e:
        print(f"Error downloading Inno Setup: {e}")
        return False

def install_inno_setup():
    """Install Inno Setup"""
    if os.path.exists(INNO_SETUP_INSTALLER):
        print("Installing Inno Setup...")
        try:
            # Run the installer with the /VERYSILENT flag for a silent installation
            subprocess.run([INNO_SETUP_INSTALLER, "/VERYSILENT", "/SUPPRESSMSGBOXES"], check=True)
            
            # Give it a moment to complete
            print("Waiting for installation to complete...")
            time.sleep(5)
            
            # Check if the installation was successful
            if is_inno_setup_installed():
                print("Inno Setup was installed successfully!")
                return True
            else:
                print("Inno Setup installation may have failed. Please install it manually.")
                return False
        except subprocess.SubprocessError as e:
            print(f"Error installing Inno Setup: {e}")
            return False
    else:
        print(f"Error: {INNO_SETUP_INSTALLER} not found")
        return False

def build_installer():
    """Build the Activity Tracker installer using Inno Setup"""
    if not os.path.exists(ISS_SCRIPT_PATH):
        print(f"Error: Inno Setup script {ISS_SCRIPT_PATH} not found")
        return False

    iscc_path = get_inno_setup_compiler_path()
    if iscc_path:
        print(f"Building installer using Inno Setup script: {ISS_SCRIPT_PATH}")
        try:
            subprocess.run([iscc_path, ISS_SCRIPT_PATH], check=True)
            
            # Check if the installer was created
            installer_path = os.path.join("installer", "ActivityTracker_Setup.exe")
            if os.path.exists(installer_path):
                print(f"\nSuccess! Installer created at: {os.path.abspath(installer_path)}")
                return True
            else:
                print(f"Error: Could not find installer at {installer_path}")
                return False
        except subprocess.CalledProcessError as e:
            print(f"Error building installer: {e}")
            return False
    else:
        print("Error: Inno Setup compiler (ISCC.exe) not found")
        return False

def main():
    """Main function"""
    if platform.system() != 'Windows':
        print("Error: This script requires Windows")
        return
    
    # Check if Inno Setup is already installed
    if not is_inno_setup_installed():
        print("Inno Setup is not installed.")
        
        # Ask user if they want to download and install Inno Setup
        response = input("Do you want to download and install Inno Setup now? (y/n): ")
        if response.lower() == 'y':
            if download_inno_setup() and install_inno_setup():
                build_installer()
            else:
                print("Failed to install Inno Setup. Please install it manually and then run this script again.")
        else:
            print("Please install Inno Setup and then run this script again.")
    else:
        # Inno Setup is already installed, proceed with building the installer
        print("Inno Setup is already installed.")
        build_installer()

if __name__ == "__main__":
    main()
