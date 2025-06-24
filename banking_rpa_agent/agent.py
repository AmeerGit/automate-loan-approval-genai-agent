import requests
from banking_rpa_agent.tools.compliance import check_compliance
from banking_rpa_agent.tools.customer import fetch_customer_data
from banking_rpa_agent.tools.loan import process_loan
from banking_rpa_agent.tools.rpa import simulate_rpa_action
from banking_rpa_agent.utils import escalate
from google.adk.agents import Agent
import logging
import time
from typing import Optional, List, Dict, Any

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# customer fetch sub agent
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


# compliance check sub agent
compliance_agent = Agent(
    name="compliance_agent",
    model="gemini-2.0-flash",
    description="Handles compliance checks for banking workflows, including dynamic LLM-powered rules.",
    instruction="Check compliance for loan and account operations. Use LLM for dynamic rule interpretation if needed.",
    tools=[check_compliance],
)

# RPA Sub-Agent (UI Simulation & Logging)
rpa_agent = Agent(
    name="rpa_agent",
    model="gemini-2.0-flash",
    description="Simulates/automates UI actions and logs them for compliance.",
    instruction="Automate UI actions for legacy and web platforms. Log all actions.",
    tools=[simulate_rpa_action],
)

# Loan Processing Sub-Agent
loan_agent = Agent(
    name="loan_agent",
    model="gemini-2.0-flash",
    description="Handles loan processing decisions.",
    instruction="Process loan applications based on customer and compliance data.",
    tools=[process_loan],
)

# --- Main Banking RPA Root Agent ---
def orchestrate_loan_workflow(customer_id: str, amount: float, rules: Optional[List[str]] = None, human_decision: Optional[dict] = None) -> dict:
    application = {"customer_id": customer_id, "amount": amount}
    if human_decision:
        application["human_decision"] = human_decision
    customer = fetch_customer_data(customer_id)
    compliance = check_compliance(application, customer, rules)
    result = process_loan(application, customer, compliance)
    logging.info(f"Workflow result: {result}")
    return {
        "customer": customer,
        "compliance": compliance,
        "loan_result": result
    }

# Workflow  Onboarding ---
def orchestrate_onboarding_workflow(customer_id: str, onboarding_data: dict) -> dict:
    customer = fetch_customer_data(customer_id)
    rpa_steps = [simulate_rpa_action(step, {"customer_id": customer_id, **onboarding_data})
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