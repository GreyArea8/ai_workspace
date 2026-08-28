import os
import json
import random
from datetime import datetime

ASSET_DIR = "generated_assets"
LOG_FILE = "system_activity.json"

def generate_dynamic_assets():
    if not os.path.exists(ASSET_DIR):
        os.makedirs(ASSET_DIR)
        
    timestamp_slug = datetime.now().strftime("%Y%m%d_%H%M%S")
    tool_id = random.randint(100, 999)
    
    utility_filename = f"auto_utility_{tool_id}.py"
    guide_filename = f"guide_template_{tool_id}.md"
    
    utility_path = os.path.join(ASSET_DIR, utility_filename)
    guide_path = os.path.join(ASSET_DIR, guide_filename)
    
    # Engine 1: Generate dynamic Python utility script
    utility_code = f'''# Dynamic Utility ID: {tool_id}
# Generated automatically on {datetime.now()}
import math

def run_diagnostic():
    factor = {random.randint(1, 50)}
    result = math.sqrt(factor) * 10
    print(f"Diagnostic calculation result: {{result}}")

if __name__ == "__main__":
    run_diagnostic()
'''
    with open(utility_path, "w") as f:
        f.write(utility_code)
        
    # Engine 2: Generate dynamic Markdown technical guide
    guide_content = f'''# Technical Troubleshooting Guide #{tool_id}
## System Overview
Automated asset generated at timestamp {datetime.now()}. 
Focus parameter: Diagnostic module variant {tool_id}.

## Steps
1. Verify system logs.
2. Execute utility script `{utility_filename}`.
3. Confirm operational metrics.
'''
    with open(guide_path, "w") as f:
        f.write(guide_content)
        
    # Log execution
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "utility_generated": utility_path,
        "content_generated": guide_path,
        "status": "DUAL_ENGINE_DYNAMIC_SUCCESS"
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
        
    print(f"Dynamic dual-engine assets successfully generated: {utility_filename}, {guide_filename}")

if __name__ == "__main__":
    generate_dynamic_assets()
