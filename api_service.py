import os
import re
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

def process_user_request(prompt):
    text = prompt.lower().strip()
    
    # 1. Standard OBD-II Trouble Code Regex Match (e.g., P0442, C0350, B0010, U0100)
    if re.match(r"^[pbcsu]\d{4}$", text):
        return f"DTC Lookup for {text.upper()}: Check related sensor circuits, wiring harness, connector pins, and reference voltage. Verify live freeze frame data."
    
    # 2. Keyword Subsystem Routines
    elif "evap" in text or "leak" in text:
        return "Diagnostic Rule: Check purge valve, vent solenoid, gas cap seal, and pressure sensor for EVAP system integrity."
    elif "code" in text or "dtc" in text:
        return "Diagnostic Lookup: Please provide the specific OBDII trouble code (e.g., P0442) for targeted troubleshooting steps."
    
    # 3. Cadillac Escalade Multi-Level Subsystem Branching
    elif "escalade" in text:
        if "suspension" in text or "air ride" in text or "strut" in text:
            return "Escalade Air Suspension: Inspect compressor relay, airline connections, height sensors, and electronic damping control fuses."
        elif "transmission" in text or "shift" in text or "slip" in text:
            return "Escalade Transmission: Check fluid level/condition, 1-2 accumulator piston, 3-5-R wave plate, and shift solenoids."
        elif "knock" in text or "engine" in text or "lifter" in text:
            return "Escalade Engine: Verify oil pressure, inspect Active Fuel Management (AFM) lifters, check pushrods, and scan for active knock sensor codes."
        elif "brakes" in text or "abs" in text:
            return "Escalade Brakes: Inspect wheel speed sensor wiring harness, ABS module ground, and brake booster vacuum line."
        else:
            return "Vehicle Context: Cadillac Escalade system selected. Specify target symptom (e.g., suspension, transmission, engine knock, brakes) to proceed."
            
    # 4. General Catch-All
    else:
        return f"Processed request: {prompt} (System ready for advanced command routing.)"

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json() or {}
    
    if "message" in data:
        message = data["message"]
        chat_id = message["chat"]["id"]
        user_text = message.get("text", "")
        
        reply = process_user_request(user_text)
        
        try:
            requests.post(TELEGRAM_API_URL, json={
                "chat_id": chat_id,
                "text": reply
            }, timeout=5)
        except Exception as e:
            print(f"Telegram API dispatch error: {e}")
            
        return jsonify({"status": "success"})
        
    return jsonify({"status": "ignored"})

@app.route("/", methods=["GET"])
def health_check():
    return "Cadillac Escalade Diagnostic Bot service is live.", 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
