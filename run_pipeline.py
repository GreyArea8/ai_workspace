import subprocess
from system_logger import log_system_state

def run_automation_pipeline():
    print("Executing automated system check...")
    log_system_state()
    print("Pipeline execution complete.")

if __name__ == "__main__":
    run_automation_pipeline()
