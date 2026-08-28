import subprocess
def ping_host(ip_address):
   # Sends a single ping packet to chech if a device is online
   command=["ping", "-c", "1", "-W", "1", ip_address]
   result=subprocess.run(command,stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
   return result.returncode == 0

print("Checking local container interface...")
if ping_host("127.0.0.1"):
    print("Local interface loopback is active and responding.")
else:
    print("loopback failed.")
