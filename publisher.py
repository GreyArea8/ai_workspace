import os
import subprocess
from datetime import datetime

DIST_DIR = "release_bundles"

def publish_releases():
    # Ensure git global/local identity is set to prevent auto-detect failures
    subprocess.run(["git", "config", "--global", "user.name", "Auto Technician Bot"], check=True)
    subprocess.run(["git", "config", "--global", "user.email", "autotechnician504@penguin.local"], check=True)

    if not os.path.exists(DIST_DIR):
        print("No release bundles directory found to publish.")
        return

    print("Preparing release bundles for version control...")

    if not os.path.exists(".git"):
        subprocess.run(["git", "init"], check=True)

    subprocess.run(["git", "add", DIST_DIR, "system_activity.json"], check=True)
    commit_msg = f"Automated Release Sync: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    # Check if there are actual changes to commit to avoid exit status 1
    status_result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    if not status_result.stdout.strip():
        print("No changes to commit.")
        return

    subprocess.run(["git", "commit", "-m", commit_msg], check=True)

    print("Pushing updates to remote repository...")
    push_result = subprocess.run(["git", "push", "origin", "master"], capture_output=True, text=True)
    if push_result.returncode != 0:
        print(f"Git push warning/error: {push_result.stderr}")
    else:
        print("Successfully pushed release bundles to remote cloud.")

if __name__ == "__main__":
    publish_releases()
