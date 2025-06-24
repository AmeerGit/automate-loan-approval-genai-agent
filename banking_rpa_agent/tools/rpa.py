import logging
import time
from typing import Dict, Any

def simulate_rpa_action(action: str, details: Dict[str, Any] = None) -> Dict[str, Any]:
  logging.info(f"Simulating RPA action: {action} with details: {details}")
  # Simulate actions and return results as per actual RPA would
  if action == "approve_loan":
    return {"status": "success", "message": "Loan approved in system.", "timestamp": time.time()}
  return {"status": "simulated", "action": action, "details": details}