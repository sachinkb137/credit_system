import requests
import json

BASE_URL = 'http://localhost:8000/api'

def test_register_customer():
    """Test customer registration"""
    data = {
        'first_name': 'Alice',
        'last_name': 'Brown',
        'age': 28,
        'monthly_income': 55000,
        'phone_number': '5556667777'
    }

    response = requests.post(f'{BASE_URL}/register', json=data)
    print(f'Register Customer: {response.status_code}')
    if response.status_code == 201:
        print(json.dumps(response.json(), indent=2))
    else:
        print(response.text)
    return response

def test_check_eligibility():
    """Test loan eligibility check"""
    data = {
        'customer_id': 1,
        'loan_amount': 200000,
        'interest_rate': 10,
        'tenure': 24
    }

    response = requests.post(f'{BASE_URL}/check-eligibility', json=data)
    print(f'Check Eligibility: {response.status_code}')
    print(json.dumps(response.json(), indent=2))
    return response

def test_create_loan():
    """Test loan creation"""
    data = {
        'customer_id': 1,
        'loan_amount': 200000,
        'interest_rate': 10,
        'tenure': 24
    }

    response = requests.post(f'{BASE_URL}/create-loan', json=data)
    print(f'Create Loan: {response.status_code}')
    print(json.dumps(response.json(), indent=2))
    return response

def test_view_loan():
    """Test viewing loan details"""
    loan_id = 1
    response = requests.get(f'{BASE_URL}/view-loan/{loan_id}')
    print(f'View Loan {loan_id}: {response.status_code}')
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))
    else:
        print(response.text)
    return response

def test_view_customer_loans():
    """Test viewing customer loans"""
    customer_id = 1
    response = requests.get(f'{BASE_URL}/view-loans/{customer_id}')
    print(f'View Customer {customer_id} Loans: {response.status_code}')
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))
    else:
        print(response.text)
    return response

if __name__ == '__main__':
    print("Testing Credit Approval System API")
    print("=" * 40)

    # Test all endpoints
    test_register_customer()
    print()

    test_check_eligibility()
    print()

    test_create_loan()
    print()

    test_view_loan()
    print()

    test_view_customer_loans()
    print()

    print("API testing completed!")