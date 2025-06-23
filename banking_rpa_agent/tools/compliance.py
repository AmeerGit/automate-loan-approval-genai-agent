import logging
from typing import Optional, List

# This is a risky function. In a real-world scenario, a more secure rule engine should be used.
def safe_eval_rule(rule: str, context: dict) -> bool:
    # Only allow access to context keys, no builtins
    try:
        return eval(rule, {"__builtins__": None}, context)
    except Exception as e:
        logging.error(f"Rule eval error: {rule} | {e}")
        return False

def check_compliance(application: dict, customer: dict, rules: Optional[List[str]] = None) -> dict:
    # If human decision is present and approved, treat as compliant
    human_decision = application.get("human_decision")
    if human_decision and human_decision.get("status") == "approved_by_human":
        return {"compliant": True, "reason": "Approved by human override."}
    # --- Salary-based rules (Caixabank best practice) ---
    salary = customer.get("annual_income", 0)
    if salary < 18000:
        return {"compliant": False, "reason": "Salary below minimum threshold (auto-reject).", "escalate": False}
    if 18000 <= salary < 25000:
        return {"compliant": False, "reason": "Salary in borderline range, requires risk/compliance review.", "escalate": True}
    # Static rules
    if application.get("amount", 0) > 50000:
        return {"compliant": False, "reason": "Amount exceeds auto-approval limit.", "escalate": True}
    if customer.get("kyc_status") != "verified":
        return {"compliant": False, "reason": "KYC not verified.", "escalate": True}
    if customer.get("credit_score", 0) < 600:
        return {"compliant": False, "reason": "Credit score below minimum threshold."}
    if customer.get("employment_status") != "employed":
        return {"compliant": False, "reason": "Employment status not valid."}
    # Dynamic rules (LLM simulation)
    if rules:
        context = {**application, **customer}
        for rule in rules:
            if not safe_eval_rule(rule, context):
                return {"compliant": False, "reason": f"Failed dynamic rule: {rule}"}
    return {"compliant": True}