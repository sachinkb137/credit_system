import pandas as pd
from datetime import datetime
from django.conf import settings
from celery import shared_task
from .models import Customer, Loan


@shared_task
def ingest_customer_data(file_path):
    """Background task to ingest customer data from Excel file"""
    try:
        df = pd.read_excel(file_path)

        for _, row in df.iterrows():
            # Handle different possible column name formats
            customer_id = row.get('customer_id') or row.get('Customer ID')
            first_name = row.get('first_name') or row.get('First Name')
            last_name = row.get('last_name') or row.get('Last Name')
            phone_number = row.get('phone_number') or row.get('Phone Number')
            monthly_salary = row.get('monthly_salary') or row.get('Monthly Salary')
            approved_limit = row.get('approved_limit') or row.get('Approved Limit')
            age = row.get('age') or row.get('Age', 25)
            current_debt = row.get('current_debt', 0)
            
            Customer.objects.update_or_create(
                customer_id=customer_id,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'phone_number': str(phone_number),
                    'monthly_salary': monthly_salary,
                    'approved_limit': approved_limit,
                    'current_debt': current_debt,
                    'age': age
                }
            )
        return f"Successfully ingested {len(df)} customer records"
    except Exception as e:
        return f"Error ingesting customer data: {str(e)}"


@shared_task
def ingest_loan_data(file_path):
    """Background task to ingest loan data from Excel file"""
    try:
        df = pd.read_excel(file_path)

        for _, row in df.iterrows():
            # Handle different possible column name formats
            customer_id = row.get('customer id') or row.get('Customer ID')
            loan_id = row.get('loan id') or row.get('Loan ID')
            loan_amount = row.get('loan amount') or row.get('Loan Amount')
            tenure = row.get('tenure') or row.get('Tenure')
            interest_rate = row.get('interest rate') or row.get('Interest Rate')
            monthly_payment = row.get('monthly repayment (emi)') or row.get('Monthly payment')
            emis_paid = row.get('EMIs paid on time') or row.get('EMIs paid on Time')
            start_date_col = row.get('start date') or row.get('Date of Approval')
            end_date_col = row.get('end date') or row.get('End Date')
            
            customer = Customer.objects.get(customer_id=customer_id)
            start_date = pd.to_datetime(start_date_col).date()
            end_date = pd.to_datetime(end_date_col).date()

            Loan.objects.update_or_create(
                loan_id=loan_id,
                defaults={
                    'customer': customer,
                    'loan_amount': loan_amount,
                    'tenure': tenure,
                    'interest_rate': interest_rate,
                    'monthly_installment': monthly_payment,
                    'emis_paid_on_time': emis_paid,
                    'start_date': start_date,
                    'end_date': end_date,
                }
            )
        return f"Successfully ingested {len(df)} loan records"
    except Exception as e:
        return f"Error ingesting loan data: {str(e)}"