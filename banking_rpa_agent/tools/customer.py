import logging
import requests
from banking_rpa_agent.config import API_BASE_URL

def fetch_customer_data(customer_id: str) -> dict:
    try:
        response = requests.get(f"{API_BASE_URL}/customers/{customer_id}")
        if response.status_code == 200:
            customer = response.json()
            # Escalation rules
            if customer.get("kyc_status") != "verified":
                customer["escalate"] = True
                customer["escalation_reason"] = "KYC not verified"
            elif not customer.get("credit_score"):
                customer["escalate"] = True
                customer["escalation_reason"] = "Missing credit score"
            elif customer.get("account_status") != "active":
                customer["escalate"] = True
                customer["escalation_reason"] = "Account not active"
            logging.info(f"Fetched customer data: {customer}")
            return customer
        elif response.status_code == 404:
            logging.error(f"Customer not found: {customer_id}")
            return {"customer_id": customer_id, "error": "Customer not found", "escalate": True, "escalation_reason": "Customer not found"}
        else:
            logging.error(f"API error for customer {customer_id}: {response.status_code}")
            return {"customer_id": customer_id, "error": "API error", "escalate": True, "escalation_reason": "API error"}
    except requests.exceptions.RequestException as e:
        logging.error(f"Could not connect to customer API: {e}")
        return {"customer_id": customer_id, "error": "Could not connect to API", "escalate": True, "escalation_reason": "API connection error"}