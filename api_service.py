from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/callback/complete', methods=['GET', 'POST'])
def task_completion_callback():
    # Capture payloads sent via URL query string (GET/POST) or JSON body (POST)
    if request.is_json:
        data = request.json or {}
    else:
        data = request.args or {}
        
    # Extract identifiers and dynamic financial macros from network postbacks
    user_id = data.get("user_id") or data.get("subid") or data.get("click_id", "external_network_user")
    
    try:
        payout_amount = float(data.get("amount") or data.get("payout", 0.00))
    except (ValueError, TypeError):
        payout_amount = 0.00
    
    payout_link = "https://www.paypal.me/CornellEugene"
    
    print(f"External conversion registered. User/ClickID: {user_id} | Credited Payout: ${payout_amount:.2f} | Payout Target: {payout_link}")
    
    return jsonify({
        "status": "success",
        "network_identifier": user_id,
        "credited_amount": payout_amount,
        "routed_to": payout_link
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
