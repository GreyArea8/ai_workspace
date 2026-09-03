import re

def process_user_request(prompt):
    text = prompt.lower().strip()
    
    # Check for standard OBDII codes (e.g., p0442, c0350)
    if re.match(r"^[pbcsu]\d{4}$", text):
        return f"DTC Lookup for {text.upper()}: Check related sensor circuits, wiring harness, and reference voltage. Verify freeze frame data."
    elif "evap" in text or "leak" in text:
        return "Diagnostic Rule: Check purge valve, vent solenoid, and gas cap seal for EVAP system integrity."
    elif "code" in text or "dtc" in text:
        return "Diagnostic Lookup: Please provide the specific OBDII trouble code (e.g., P0442) for targeted troubleshooting steps."
    elif "escalade" in text:
        if "suspension" in text or "air ride" in text:
            return "Escalade Air Suspension: Inspect compressor relay, airline connections, and height sensors."
        elif "transmission" in text or "shift" in text:
            return "Escalade Transmission: Check fluid level, 1-2 accumulator piston, and shift solenoids."
        elif "knock" in text or "engine" in text:
            return "Escalade Engine: Verify oil pressure, check lifters, and inspect for active knock sensor codes."
        else:
            return "Vehicle Context: Cadillac Escalade system selected. Specify symptom (e.g., suspension, transmission, engine knock) to proceed."
    else:
        return f"Processed request: {prompt} (System ready for advanced command routing.)"
