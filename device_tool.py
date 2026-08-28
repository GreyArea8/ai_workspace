import platform
import subprocess
def get_system_info():
    # Gathers basic container specs
    info = {
        "system": platform.system(),
        "release": platform.release(),
        "node": platform.node()
    }

    return info
if __name__ == "__main__":
    print("Running diagnostic tool...")
    specs = get_system_info()
    for key, value in specs.items():
        print(f"   - {key.capitalize()}: {value}")
