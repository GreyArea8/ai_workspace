import os
import shutil
import json
from datetime import datetime

ASSET_DIR = "generated_assets"
DIST_DIR = "release_bundles"
LOG_FILE = "system_activity.json"

def package_release():
    if not os.path.exists(DIST_DIR):
        os.makedirs(DIST_DIR)
        
    timestamp_slug = datetime.now().strftime("%Y%m%d_%H%M%S")
    bundle_name = f"release_{timestamp_slug}"
    bundle_path = os.path.join(DIST_DIR, bundle_name)
    
    # Copy generated assets into a clean release folder
    if os.path.exists(ASSET_DIR):
        shutil.copytree(ASSET_DIR, bundle_path)
        print(f"Release bundle created at: {bundle_path}")
        
        # Log distribution event
        log_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "release_bundle": bundle_path,
            "status": "ASSETS_PACKAGED"
        }
        
        logs = []
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                try:
                    logs = json.load(f)
                except json.JSONDecodeError:
                    logs = []
                    
        logs.append(log_entry)
        with open(LOG_FILE, "w") as f:
            json.dump(logs, f, indent=4)
    else:
        print("No assets found to package.")

if __name__ == "__main__":
    package_release()
