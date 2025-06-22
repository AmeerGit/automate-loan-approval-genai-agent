import requests
from google.adk.agents import Agent
import logging
import time
from typing import Optional, List, Dict, Any

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# --- Utility: Escalation ---
def escalate(reason: str, context: dict) -> dict:
    logging.warning(f"Escalation triggered: {reason} | Context: {context}")
    time.sleep(1)  # Simulate human-in-the-loop
    return {"escalation": "notified_human", "status": "approved_by_human", "reason": reason, "context": context}

# --- Customer Data Sub-Agent ---
# In-memory mock customer data
CUSTOMERS = {
    "C123": {
        "customer_id": "C123",
        "name": "John Doe",
        "kyc_status": "verified",
        "account_status": "active",
        "address": "123 Main St, Springfield",
        "dob": "1985-04-12",
        "credit_score": 650,
        "employment_status": "employed",
        "annual_income": 95000,
        "existing_loans": 1,
        "loan_defaults": 0
    },
    "C456": {
        "customer_id": "C456",
        "name": "Jane Smith",
        "kyc_status": "pending",
        "account_status": "inactive",
        "address": "456 Elm St, Metropolis",
        "dob": "1990-09-23",
        "credit_score": 650,
        "employment_status": "self-employed",
        "annual_income": 60000,
        "existing_loans": 2,
        "loan_defaults": 1
    },
    # Add more mock customers as needed
}

def fetch_customer_data(customer_id: str) -> dict:
    customer = CUSTOMERS.get(customer_id)
    if customer:
        # Escalation rules
        customer = customer.copy()  # Avoid mutating the global dict
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
    else:
        logging.error(f"Customer not found: {customer_id}")
        return {"customer_id": customer_id, "error": "Customer not found", "escalate": True, "escalation_reason": "Customer not found"}

customer_agent = Agent(
    name="customer_agent",
    model="gemini-2.0-flash",
    description="Handles customer data retrieval, validation, and escalation for banking workflows.",
    instruction="""
    - Retrieve customer profile and financial data from the core system or API.
    - Validate that all required fields are present: KYC status, credit score, account status, employment, income, etc.
    - If KYC is not verified, credit score is missing, or account is not active, flag the customer for escalation and provide a clear escalation reason.
    - If customer is not found or there is an API error, escalate to a human with the error details.
    - Log all data retrievals, errors, and escalations for compliance.
    - Respond with all available customer data and any escalation flags or reasons.
    """,
    tools=[fetch_customer_data],
)

# --- Compliance Sub-Agent (LLM-powered, safe rule eval) ---
def safe_eval_rule(rule: str, context: dict) -> bool:
    # Only allow access to context keys, no builtins
    try:
        return eval(rule, {"__builtins__": None}, context)
    except Exception as e:
        logging.error(f"Rule eval error: {rule} | {e}")
        return False

def check_compliance(application: dict, customer: dict, rules: Optional[List[str]] = None) -> dict:
    # Static rules
    if application.get("amount", 0) > 50000:
        return {"compliant": False, "reason": "Amount exceeds auto-approval limit."}
    if customer.get("kyc_status") != "verified":
        return {"compliant": False, "reason": "KYC not verified."}
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

compliance_agent = Agent(
    name="compliance_agent",
    model="gemini-2.0-flash",
    description="Handles compliance checks for banking workflows, including dynamic LLM-powered rules.",
    instruction="Check compliance for loan and account operations. Use LLM for dynamic rule interpretation if needed.",
    tools=[check_compliance],
)

# --- RPA Sub-Agent (UI Simulation & Logging) ---
def simulate_ui_action(action: str, details: dict) -> dict:
    logging.info(f"Simulating UI action: {action} | Details: {details}")
    time.sleep(0.5)
    return {"action": action, "details": details, "status": "success", "timestamp": time.time()}

rpa_agent = Agent(
    name="rpa_agent",
    model="gemini-2.0-flash",
    description="Simulates/automates UI actions and logs them for compliance.",
    instruction="Automate UI actions for legacy and web platforms. Log all actions.",
    tools=[simulate_ui_action],
)

# --- Loan Processing Sub-Agent ---
def process_loan(application: dict, customer: dict, compliance: dict) -> dict:
    if not compliance.get("compliant", False):
        return {"status": "rejected", "reason": compliance.get("reason", "Compliance failed")}
    if application.get("amount", 0) > 50000:
        escalation_result = escalate("High-value loan requires human approval.", {"application": application, "customer": customer})
        return {"status": "escalated", "reason": "High-value loan requires human approval.", "escalation_result": escalation_result}
    rpa_result = simulate_ui_action("approve_loan", {"application": application, "customer": customer})
    return {"status": "approved", "message": "Loan approved and processed.", "rpa_log": rpa_result}

loan_agent = Agent(
    name="loan_agent",
    model="gemini-2.0-flash",
    description="Handles loan processing decisions.",
    instruction="Process loan applications based on customer and compliance data.",
    tools=[process_loan],
)

# --- Main Banking RPA Root Agent ---
def orchestrate_loan_workflow(customer_id: str, amount: float, rules: Optional[List[str]] = None) -> dict:
    application = {"customer_id": customer_id, "amount": amount}
    customer = fetch_customer_data(customer_id)
    compliance = check_compliance(application, customer, rules)
    result = process_loan(application, customer, compliance)
    logging.info(f"Workflow result: {result}")
    return {
        "customer": customer,
        "compliance": compliance,
        "loan_result": result
    }

# --- Additional Workflow Example: Onboarding ---
def orchestrate_onboarding_workflow(customer_id: str, onboarding_data: dict) -> dict:
    customer = fetch_customer_data(customer_id)
    rpa_steps = [simulate_ui_action(step, {"customer_id": customer_id, **onboarding_data})
                 for step in ["create_account", "verify_documents", "setup_online_banking"]]
    compliance = check_compliance({"customer_id": customer_id, **onboarding_data}, customer)
    if not compliance.get("compliant", False):
        escalation = escalate("Onboarding compliance failed", {"customer": customer, "onboarding_data": onboarding_data})
        return {"status": "escalated", "escalation": escalation, "rpa_steps": rpa_steps}
    return {"status": "onboarded", "rpa_steps": rpa_steps, "compliance": compliance}

root_agent = Agent(
    name="banking_rpa_root_agent",
    model="gemini-2.0-flash",
    global_instruction="You are a helpful virtual assistant for a bank. Always respond politely.",
    instruction="You are the main banking assistant. You can help with customer data, compliance, and loan processing. Delegate to sub-agents as needed.",
    sub_agents=[customer_agent, compliance_agent, loan_agent, rpa_agent],
    tools=[orchestrate_loan_workflow, orchestrate_onboarding_workflow],
)