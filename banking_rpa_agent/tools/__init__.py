from .compliance import check_compliance
from .customer import fetch_customer_data
from .loan import process_loan
from .rpa import simulate_rpa_action

__all__ = [
    "check_compliance",
    "fetch_customer_data",
    "process_loan",
    "simulate_rpa_action",
]