import os
import subprocess

def configure_cron():
    script_path = os.path.abspath("run_full_cycle.py")
    python_path = "python3"
    
    # Create a cron entry that runs every hour (or adjust as needed)
    cron_command = f"0 * * * * cd {os.path.dirname(script_path)} && {python_path} -B {script_path} >> cron_output.log 2>&1"
    
    # Export current crontab, append new job, and reload
    current_cron = subprocess.run(["crontab", "-l"], capture_output=True, text=True).stdout
    if cron_command not in current_cron:
        new_cron = current_cron + "\n" + cron_command + "\n"
        process = subprocess.Popen(["crontab", "-"], stdin=subprocess.PIPE, text=True)
        process.communicate(input=new_cron)
        print("Background cron schedule successfully configured.")
    else:
        print("Cron job is already active.")

if __name__ == "__main__":
    configure_cron()
