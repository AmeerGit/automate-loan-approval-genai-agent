from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

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

@app.get("/customers/{customer_id}")
def get_customer(customer_id: str):
    customer = CUSTOMERS.get(customer_id)
    if customer:
        return JSONResponse(content=customer)
    return JSONResponse(content={"error": "Customer not found"}, status_code=404)
