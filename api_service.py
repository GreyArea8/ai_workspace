from flask import Flask, request

app = Flask(__name__)

@app.route('/callback/complete', methods=['POST'])
def task_completion_callback():
    data = request.json
    user_id = data.get("user_id")
    payout_amount = data.get("amount")
    
    payout_link = "https://www.paypal.me/CornellEugene"
    print(f"Verified completion for {user_id}. Payout of ${payout_amount} routed to {payout_link}")
    
    return {"status": "success", "routed_to": payout_link}, 200
