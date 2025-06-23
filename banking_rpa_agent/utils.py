import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

def escalate(reason: str, context: dict) -> dict:
    logging.warning(f"Escalation triggered: {reason} | Context: {context}")
    human_decision = context.get("human_decision")
    if human_decision:
        status = human_decision.get("status", "approved_by_human")
        notes = human_decision.get("notes", "Human reviewed and approved.")
        return {"escalation": "notified_human", "status": status, "notes": notes, "reason": reason, "context": context}
    else:
        # Default: pending human action
        # Provide a "Next Best Action" suggestion based on the reason
        next_best_action = "Forward to compliance officer for manual review."
        if "KYC" in reason:
            next_best_action = "Contact customer to provide updated KYC documentation."
        elif "salary" in reason.lower():
            next_best_action = "Forward to senior underwriter for risk assessment."
        elif "amount" in reason.lower():
            next_best_action = "Forward to high-value loan review team."
        return {"escalation": "pending_human", "status": "pending", "reason": reason, "next_best_action": next_best_action, "context": context}