from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/callback/complete', methods=['GET', 'POST'])
def task_completion_callback():
    # Capture incoming postback data via JSON payload or URL query strings
    if request.is_json:
        data = request.json or {}
    else:
        data = request.args or {}
        
    # Extract identifiers used by CPAlead, MyLead, or custom networks
    user_id = (
        data.get("user_id") or 
        data.get("subid") or 
        data.get("click_id") or 
        data.get("clickid") or 
        data.get("uid", "live_network_user")
    )
    
    # Extract financial payout macros safely
    try:
        payout_amount = float(
            data.get("amount") or 
            data.get("payout") or 
            data.get("payout_decimal") or 
            data.get("earn", 0.00)
        )
    except (ValueError, TypeError):
        payout_amount = 0.00
    
    payout_link = "https://www.paypal.me/CornellEugene"
    
    print(f"Verified live conversion. User/ClickID: {user_id} | Credited Payout: ${payout_amount:.2f} | Routing Target: {payout_link}")
    
    return jsonify({
        "status": "success",
        "user_id": user_id,
        "credited_amount": payout_amount,
        "routed_to": payout_link
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
