from banking_rpa_agent.utils import escalate
from banking_rpa_agent.tools.rpa import simulate_rpa_action

def process_loan(application: dict, customer: dict, compliance: dict) -> dict:
    human_decision = application.get("human_decision")
    # If human decision is present, honor it
    if human_decision:
        status = human_decision.get("status")
        notes = human_decision.get("notes", "Human reviewed.")
        if status == "approved_by_human":
            rpa_log = [
                simulate_rpa_action("Core Banking System (Legacy)", "override_compliance_flag", {"customer_id": customer["customer_id"]}),
                simulate_rpa_action("Web Loan Portal", "approve_loan_application", {"application_id": application["customer_id"]})
            ]
            return {"status": "approved", "message": "Loan approved by human.", "rpa_log": rpa_log, "escalation_result": {"escalation": "notified_human", "status": status, "notes": notes}}
        else:
            return {"status": "rejected", "reason": notes, "escalation_result": {"escalation": "notified_human", "status": status, "notes": notes}}
    # Otherwise, normal compliance/escalation logic
    if not compliance.get("compliant", False):
        if compliance.get("escalate"):
            escalation_result = escalate(compliance.get("reason", "Compliance failed"), {"application": application, "customer": customer, "human_decision": human_decision})
            return {"status": escalation_result["status"], "reason": escalation_result.get("reason"), "next_best_action": escalation_result.get("next_best_action"), "escalation_result": escalation_result}
        return {"status": "rejected", "reason": compliance.get("reason", "Compliance failed")}
    if application.get("amount", 0) > 50000 or customer.get("escalate"):
        escalation_result = escalate("High-value loan or flagged customer requires human approval.", {"application": application, "customer": customer, "human_decision": human_decision})
        return {"status": escalation_result["status"], "reason": escalation_result.get("reason"), "next_best_action": escalation_result.get("next_best_action"), "escalation_result": escalation_result}

    # Simulate a more realistic, multi-system RPA workflow for a fully automated approval
    rpa_log = [
        simulate_rpa_action("Credit Bureau API", "final_credit_check", {"customer_id": customer["customer_id"]}),
        simulate_rpa_action("Core Banking System (Legacy)", "disburse_funds", {"amount": application["amount"], "account": customer["customer_id"]}),
        simulate_rpa_action("Salesforce (Web)", "update_loan_status", {"status": "Approved", "customer_id": customer["customer_id"]}),
        simulate_rpa_action("Email Gateway API", "send_approval_notification", {"customer_email": f"{customer.get('name', '').replace(' ', '.').lower()}@example.com"})
    ]

    return {"status": "approved", "message": "Loan approved and processed.", "rpa_log": rpa_log}