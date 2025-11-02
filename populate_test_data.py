import os
import django
from datetime import date, timedelta
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'credit_approval_system.settings')
django.setup()

from loans.models import Customer, Loan

def populate_test_data():
    """Populate test data for the credit approval system"""

    # Create test customers
    customers_data = [
        {
            'customer_id': 1,
            'first_name': 'John',
            'last_name': 'Doe',
            'age': 30,
            'phone_number': '1234567890',
            'monthly_salary': Decimal('50000.00'),
            'approved_limit': Decimal('1800000.00'),
            'current_debt': Decimal('0.00')
        },
        {
            'customer_id': 2,
            'first_name': 'Jane',
            'last_name': 'Smith',
            'age': 25,
            'phone_number': '0987654321',
            'monthly_salary': Decimal('60000.00'),
            'approved_limit': Decimal('2160000.00'),
            'current_debt': Decimal('0.00')
        },
        {
            'customer_id': 3,
            'first_name': 'Bob',
            'last_name': 'Johnson',
            'age': 35,
            'phone_number': '1122334455',
            'monthly_salary': Decimal('45000.00'),
            'approved_limit': Decimal('1620000.00'),
            'current_debt': Decimal('0.00')
        }
    ]

    for customer_data in customers_data:
        Customer.objects.get_or_create(
            customer_id=customer_data['customer_id'],
            defaults=customer_data
        )

    # Create test loans
    loans_data = [
        {
            'loan_id': 1,
            'customer_id': 1,
            'loan_amount': Decimal('500000.00'),
            'tenure': 24,
            'interest_rate': Decimal('12.00'),
            'monthly_installment': Decimal('23000.00'),
            'emis_paid_on_time': 24,
            'start_date': date.today() - timedelta(days=730),  # 2 years ago
            'end_date': date.today() - timedelta(days=365)  # 1 year ago
        },
        {
            'loan_id': 2,
            'customer_id': 1,
            'loan_amount': Decimal('300000.00'),
            'tenure': 12,
            'interest_rate': Decimal('10.00'),
            'monthly_installment': Decimal('27000.00'),
            'emis_paid_on_time': 10,
            'start_date': date.today() - timedelta(days=365),  # 1 year ago
            'end_date': date.today() - timedelta(days=30)  # 1 month ago
        },
        {
            'loan_id': 3,
            'customer_id': 2,
            'loan_amount': Decimal('800000.00'),
            'tenure': 36,
            'interest_rate': Decimal('14.00'),
            'monthly_installment': Decimal('28000.00'),
            'emis_paid_on_time': 36,
            'start_date': date.today() - timedelta(days=1095),  # 3 years ago
            'end_date': date.today() - timedelta(days=365)  # 1 year ago
        }
    ]

    for loan_data in loans_data:
        customer = Customer.objects.get(customer_id=loan_data['customer_id'])
        Loan.objects.get_or_create(
            loan_id=loan_data['loan_id'],
            defaults={
                'customer': customer,
                **{k: v for k, v in loan_data.items() if k != 'customer_id'}
            }
        )

    print("Test data populated successfully!")

if __name__ == '__main__':
    populate_test_data()