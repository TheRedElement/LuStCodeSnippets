#script to install `requirements`
#   ignores errors during installation

import subprocess

# Open requirements file
with open("requirements.txt", "r") as file:
    lines = file.readlines()

for line in lines:
    package = line.strip()
    if package:  # Skip empty lines
        print(f"Installing {package}...")
        try:
            subprocess.check_call([f"pip", "install", package])
        except subprocess.CalledProcessError:
            print(f"Failed to install {package}, skipping...")