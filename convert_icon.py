# Script to convert PNG to ICO for Inno Setup
from PIL import Image
import os

def convert_png_to_ico(png_path, ico_path):
    """Convert a PNG file to ICO format with multiple sizes"""
    try:
        # Open the PNG image
        img = Image.open(png_path)
        
        # Create multiple sizes for the icon (Windows typically uses these sizes)
        sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128)]
        
        # Convert and save as ICO
        img.save(ico_path, format='ICO', sizes=sizes)
        
        print(f"Successfully converted {png_path} to {ico_path}")
        return True
    except Exception as e:
        print(f"Error converting image: {e}")
        return False

def update_inno_script(script_path, ico_path):
    """Update the Inno Setup script to use the ICO file"""
    try:
        # Read the script file
        with open(script_path, 'r') as file:
            content = file.read()
        
        # Replace the commented icon line with a proper icon setting
        content = content.replace('; Removed SetupIconFile line as PNG is not supported - needs ICO format',
                                 f'SetupIconFile={ico_path}')
        
        # Write the updated content back to the file
        with open(script_path, 'w') as file:
            file.write(content)
            
        print(f"Updated {script_path} to use {ico_path}")
        return True
    except Exception as e:
        print(f"Error updating script: {e}")
        return False

if __name__ == "__main__":
    # Paths
    png_path = "tracking-app.png"
    ico_path = "tracking-app.ico"
    script_path = "ActivityTracker.iss"
    
    # Convert PNG to ICO
    if convert_png_to_ico(png_path, ico_path):
        # Update the Inno Setup script
        update_inno_script(script_path, ico_path)
        
    print("\nDone!")
    print("You can now compile your Inno Setup script to create the installer.")
