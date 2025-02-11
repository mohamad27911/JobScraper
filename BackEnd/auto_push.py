import os
import subprocess
from datetime import datetime

# Set repo path
repo_path = "C:/Users/User/Desktop/WEB/AI-Web-Integration/Jobs-Scraper"
os.chdir(repo_path)

# Timestamp for commit message
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Git commands
commands = [
    "git add .",
    f'git commit -m "Auto-update: {timestamp}"',
    "git push origin dev"
]

# Run Git commands
for cmd in commands:
    process = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(process.stdout, process.stderr)
