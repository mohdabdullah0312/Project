import subprocess
import os
import sys
from os import system as sy

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS  # PyInstaller extracted temp directory
else:
    base_path = os.path.dirname(os.path.abspath(__file__))  # Normal script location

req_file = os.path.join(base_path, "requirements.txt")

sy(f"pip install -r \"{req_file}\"") if os.path.exists(req_file) else print("Error: requirements.txt not found!")

def install_requirements():
    """Install dependencies from requirements.txt, continuing even if some fail."""
    req_file = os.path.join(os.path.dirname(__file__), "requirements.txt")

    if not os.path.exists(req_file):
        print("Error: requirements.txt not found!")
        return

    with open(req_file, "r") as file:
        packages = [line.strip() for line in file if line.strip() and not line.startswith("#")]

    if not packages:
        print("No packages found in requirements.txt.")
        return

    for package in packages:
        try:
            print(f"Installing: {package} ...")
            subprocess.run(["pip", "install", package], check=True)
            print(f"✅ Successfully installed: {package}")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install: {package}. Continuing with next.")

    print("✅ Finished installing all packages.")

def main():
    install_requirements()

if __name__ == "__main__":
    main()
