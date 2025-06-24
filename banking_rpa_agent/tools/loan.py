from banking_rpa_agent.utils import escalate
from banking_rpa_agent.tools.rpa import simulate_rpa_action

def process_loan(application: dict, customer: dict, compliance: dict) -> dict:
    human_decision = application.get("human_decision")
    # If human decision is present, honor it
    if human_decision:
        status = human_decision.get("status")
        notes = human_decision.get("notes", "Human reviewed.")
        if status == "approved_by_human":
            rpa_result = simulate_rpa_action("approve_loan", {"application": application, "customer": customer})
            return {"status": "approved", "message": "Loan approved by human.", "rpa_log": rpa_result, "escalation_result": {"escalation": "notified_human", "status": status, "notes": notes}}
        else:
            return {"status": "rejected", "reason": notes, "escalation_result": {"escalation": "notified_human", "status": status, "notes": notes}}
    # Otherwise, normal compliance/escalation logic
    if not compliance.get("compliant", False):
        if compliance.get("escalate"):
            escalation_result = escalate(compliance.get("reason", "Compliance failed"), {"application": application, "customer": customer, "human_decision": human_decision})
            return {"status": escalation_result["status"], "reason": escalation_result.get("notes", escalation_result.get("reason")), "escalation_result": escalation_result}
        return {"status": "rejected", "reason": compliance.get("reason", "Compliance failed")}
    if application.get("amount", 0) > 50000 or customer.get("escalate"):
        escalation_result = escalate("High-value loan or flagged customer requires human approval.", {"application": application, "customer": customer, "human_decision": human_decision})
        return {"status": escalation_result["status"], "reason": escalation_result.get("notes", escalation_result.get("reason")), "escalation_result": escalation_result}
    rpa_result = simulate_rpa_action("approve_loan", {"application": application, "customer": customer})
    return {"status": "approved", "message": "Loan approved and processed.", "rpa_log": rpa_result}