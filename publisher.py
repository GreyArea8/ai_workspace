import os
import subprocess
from datetime import datetime

DIST_DIR = "release_bundles"

def publish_releases():
    if not os.path.exists(DIST_DIR):
        print("No release bundles directory found to publish.")
        return

    print("Preparing release bundles for version control...")
    
if not os.path.exists(".git"):
    subprocess.run(["git", "init"], check=True)
    subprocess.run(["git", "config", "--local", "user.name", "Auto Technician Bot"], check=True)
    subprocess.run(["git", "config", "--local", "user.email", "autotechnician504@penguin.local"], check=True)subprocess.run(["git", "add", DIST_DIR, "system_activity.json"], check=True)
commit_msg = f"Automated Release Sync: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
subprocess.run(["git", "commit", "-m", commit_msg], check=True)    
    # Push changes to remote repository (ensure remote 'origin' is configured)
    print("Pushing updates to remote repository...")
    push_result = subprocess.run(["git", "push", "origin", "master"], capture_output=True, text=True)
    if push_result.returncode != 0:
        print(f"Git push warning/error: {push_result.stderr}")
    else:
        print("Successfully pushed release bundles to remote cloud.")

if __name__ == "__main__":
    publish_releases()
