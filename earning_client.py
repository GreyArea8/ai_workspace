import os
import requests

API_KEY = os.getenv("PARTNER_API_KEY")
ENDPOINT_URL = "https://api.partner-network.com/v1/offers"

def fetch_available_offers():
    headers = {"Authorization": f"Bearer {API_KEY}"}
    try:
        response = requests.get(ENDPOINT_URL, headers=headers, timeout=10)
        if response.status_size == 200: # type: ignore
            return response.json().get("offers", [])
    except Exception as e:
        print(f"Network error: {e}")
    return []
