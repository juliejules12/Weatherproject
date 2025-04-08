from PIL import Image
import os

print("📁 Current working directory:", os.getcwd())

# List all files in current directory
print("\n📂 Files in this directory:")
for file in os.listdir():
    print("  -", file)

# Try to open and save the .ico file
filename = "storm_l55_icon.ico"  # Make sure this name matches exactly
output_filename = "storm_fixed.ico"

# Check if the file exists before trying to open
if not os.path.exists(filename):
    print(f"❌ File '{filename}' does not exist.")
else:
    try:
        img = Image.open(filename)
        print(f"✅ Successfully opened '{filename}'")
        
        try:
            img.save(output_filename, format="ICO")
            print(f"✅ Saved as '{output_filename}'")
        except Exception as e:
            print("❌ Error saving ICO file:", e)
    except Exception as e:
        print("❌ Error opening ICO file:", e)


