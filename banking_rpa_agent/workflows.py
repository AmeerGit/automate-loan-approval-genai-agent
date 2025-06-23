import logging
import time
from typing import Optional, List, Dict, Any

from banking_rpa_agent.tools.customer import fetch_customer_data
from banking_rpa_agent.tools.compliance import check_compliance
from banking_rpa_agent.tools.loan import process_loan
from banking_rpa_agent.tools.rpa import simulate_rpa_action
from banking_rpa_agent.utils import escalate

def orchestrate_loan_workflow(customer_id: str, amount: float, rules: Optional[List[str]] = None, human_decision: Optional[dict] = None) -> dict:
    start_time = time.time()
    application = {"customer_id": customer_id, "amount": amount}
    if human_decision is not None:
        application["human_decision"] = human_decision
    customer = fetch_customer_data(customer_id)
    compliance = check_compliance(application, customer, rules)
    result = process_loan(application, customer, compliance)
    end_time = time.time()

    # Add metrics for the demo
    automation_status = "fully_automated"
    if result.get("status") in ["pending", "rejected"]:
        automation_status = "human_intervention_required"

    metrics = {
        "processing_time_ms": (end_time - start_time) * 1000,
        "automation_status": automation_status
    }

    logging.info(f"Workflow result: {result}")
    return {
        "customer": customer,
        "compliance": compliance,
        "loan_result": result,
        "metrics": metrics
    }

def orchestrate_onboarding_workflow(customer_id: str, onboarding_data: dict) -> dict:
    customer = fetch_customer_data(customer_id)
    rpa_steps = [simulate_rpa_action("Mainframe", "create_account", {"customer_id": customer_id, **onboarding_data})]
    compliance = check_compliance({"customer_id": customer_id, **onboarding_data}, customer)
    if not compliance.get("compliant", False):
        escalation = escalate("Onboarding compliance failed", {"customer": customer, "onboarding_data": onboarding_data})
        return {"status": "escalated", "escalation": escalation, "rpa_steps": rpa_steps}
    return {"status": "onboarded", "rpa_steps": rpa_steps, "compliance": compliance}