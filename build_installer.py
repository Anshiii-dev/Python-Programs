# Script to build the Activity Tracker installer
import os
import sys
import subprocess
import platform

def build_installer():
    print("Building Activity Tracker Installer...")
    
    if platform.system() == 'Windows':
        try:
            # Run pynsist to build the installer
            result = subprocess.run(['pynsist', 'installer.cfg'], check=True)
            
            if result.returncode == 0:
                installer_path = os.path.join('installer', 'ActivityTracker-1.0-Setup.exe')
                if os.path.exists(installer_path):
                    print(f"\nSuccess! Installer created at: {os.path.abspath(installer_path)}")
                    return True
                else:
                    print(f"Error: Could not find installer at {installer_path}")
                    return False
            else:
                print("Error: Failed to build installer")
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"Error running pynsist: {e}")
            return False
        except FileNotFoundError:
            print("Error: pynsist not found. Make sure it's installed (pip install pynsist)")
            return False
    else:
        print("Error: This script requires Windows")
        return False

if __name__ == "__main__":
    build_installer()
