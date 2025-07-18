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
    # Low salary, should auto-reject
    "C789": {
        "customer_id": "C789",
        "name": "Carlos Ruiz",
        "kyc_status": "verified",
        "account_status": "active",
        "address": "789 Oak St, Barcelona",
        "dob": "1995-07-15",
        "credit_score": 700,
        "employment_status": "employed",
        "annual_income": 15000,
        "existing_loans": 0,
        "loan_defaults": 0
    },
    # Borderline salary, should escalate
    "C321": {
        "customer_id": "C321",
        "name": "Maria Lopez",
        "kyc_status": "verified",
        "account_status": "active",
        "address": "321 Pine St, Madrid",
        "dob": "1988-11-30",
        "credit_score": 680,
        "employment_status": "employed",
        "annual_income": 20000,
        "existing_loans": 1,
        "loan_defaults": 0
    },
    # Bad credit score
    "C654": {
        "customer_id": "C654",
        "name": "Luis Garcia",
        "kyc_status": "verified",
        "account_status": "active",
        "address": "654 Maple St, Valencia",
        "dob": "1978-03-22",
        "credit_score": 550,
        "employment_status": "employed",
        "annual_income": 40000,
        "existing_loans": 3,
        "loan_defaults": 2
    },
    # Inactive account
    "C111": {
        "customer_id": "C111",
        "name": "Pablo Martinez",
        "kyc_status": "verified",
        "account_status": "inactive",
        "address": "111 Birch St, Bilbao",
        "dob": "1980-01-01",
        "credit_score": 690,
        "employment_status": "employed",
        "annual_income": 35000,
        "existing_loans": 1,
        "loan_defaults": 0
    },
    # Self-employed, good salary
    "C222": {
        "customer_id": "C222",
        "name": "Lucia Fernandez",
        "kyc_status": "verified",
        "account_status": "active",
        "address": "222 Palm St, Zaragoza",
        "dob": "1983-09-09",
        "credit_score": 710,
        "employment_status": "self-employed",
        "annual_income": 65000,
        "existing_loans": 0,
        "loan_defaults": 0
    },
    # Missing credit score
    "C333": {
        "customer_id": "C333",
        "name": "Miguel Sanchez",
        "kyc_status": "verified",
        "account_status": "active",
        "address": "333 Spruce St, Malaga",
        "dob": "1999-12-12",
        "employment_status": "employed",
        "annual_income": 30000,
        "existing_loans": 0,
        "loan_defaults": 0
    },
    # Many loan defaults
    "C444": {
        "customer_id": "C444",
        "name": "Isabel Romero",
        "kyc_status": "verified",
        "account_status": "active",
        "address": "444 Willow St, Murcia",
        "dob": "1975-06-06",
        "credit_score": 610,
        "employment_status": "employed",
        "annual_income": 42000,
        "existing_loans": 4,
        "loan_defaults": 4
    }
}

@app.get("/customers/{customer_id}")
def get_customer(customer_id: str):
    customer = CUSTOMERS.get(customer_id)
    if customer:
        return JSONResponse(content=customer)
    return JSONResponse(content={"error": "Customer not found"}, status_code=404)
