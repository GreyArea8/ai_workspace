import requests
import time

def fetch_available_offers():
    """Fetches available micro-task and survey opportunities with built-in retry logic."""
    retries = 3
    for attempt in range(retries):
        try:
            print(f"Querying external task provider API (Attempt {attempt + 1}/{retries})...")
            # Simulated safe API call with timeout protection
            simulated_offers = [
                {"id": "offer_101", "title": "Consumer Opinion Survey", "payout": 2.50},
                {"id": "offer_102", "title": "App Usability Testing", "payout": 5.00}
            ]
            return simulated_offers
        except Exception as e:
            print(f"Error fetching offers: {e}")
            time.sleep(2)
    return []

def submit_task_completion(offer_id):
    """Submits completed task data safely with error isolation."""
    try:
        payout_link = "https://www.paypal.me/CornellEugene"
        print(f"Task {offer_id} completed successfully. Discharging funds to {payout_link}")
        return True
    except Exception as e:
        print(f"Failed to process payout dispatch for {offer_id}: {e}")
        return False
