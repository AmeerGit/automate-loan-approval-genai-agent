from flask import Flask, jsonify
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# This data now lives in its own "service"
CUSTOMERS = {
  # High credit score, should auto-approve
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
    }
}

@app.route('/customers/<string:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = CUSTOMERS.get(customer_id)
    if customer:
        return jsonify(customer)
    else:
        return jsonify({"error": "Customer not found"}), 404

if __name__ == '__main__':
    app.run(port=5001, debug=True)