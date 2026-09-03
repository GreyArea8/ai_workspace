import os
import json
import random
from datetime import datetime

ASSET_DIR = "generated_assets"
LOG_FILE = "system_activity.json"
PAYPAL_LINK = "https://www.paypal.me/CornellEugene"

def generate_dynamic_assets():
    if not os.path.exists(ASSET_DIR):
        os.makedirs(ASSET_DIR)
        
    timestamp_slug = datetime.now().strftime("%Y%m%d_%H%M%S")
    tool_id = random.randint(100, 999)
    
    asset_content = {
        "asset_id": tool_id,
        "timestamp": timestamp_slug,
        "offer": "Professional Automotive Diagnostic & Technical Guide",
        "payment_portal": PAYPAL_LINK,
        "status": "ready_for_monetization"
    }
    
    filepath = os.path.join(ASSET_DIR, f"commercial_asset_{tool_id}.json")
    with open(filepath, "w") as f:
        json.dump(asset_content, f, indent=4)
        
    print(f"Generated commercial asset {tool_id} with PayPal checkout hook.")

if __name__ == "__main__":
    generate_dynamic_assets()
