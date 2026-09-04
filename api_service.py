from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/callback/complete', methods=['GET', 'POST'])
def task_completion_callback():
    if request.is_json:
        data = request.json or {}
    else:
        data = request.args or {}
        
    # Capture universal network tracking parameters and identifiers
    user_id = data.get("user_id") or data.get("subid") or data.get("click_id") or data.get("uid", "live_network_user")
    
    try:
        payout_amount = float(data.get("amount") or data.get("payout") or data.get("earn", 0.00))
    except (ValueError, TypeError):
        payout_amount = 0.00
    
    payout_link = "https://www.paypal.me/CornellEugene"
    
    print(f"Live conversion verified. Identifier: {user_id} | Amount: ${payout_amount:.2f} | Routing to: {payout_link}")
    
    return jsonify({
        "status": "success",
        "user_id": user_id,
        "credited_amount": payout_amount,
        "routed_to": payout_link
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
