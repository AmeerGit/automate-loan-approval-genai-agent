import logging
import time

def simulate_rpa_action(system: str, action: str, details: dict) -> dict:
    log_message = f"Simulating RPA Action on '{system}': {action} | Details: {details}"
    logging.info(log_message)
    time.sleep(0.5)
    return {"system": system, "action": action, "details": details, "status": "success", "timestamp": time.time()}