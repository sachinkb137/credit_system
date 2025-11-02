from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import date, timedelta
from decimal import Decimal
from .models import Customer, Loan
from .serializers import (
    CustomerRegistrationSerializer, CustomerSerializer,
    LoanEligibilitySerializer, LoanEligibilityResponseSerializer,
    LoanCreationSerializer, LoanCreationResponseSerializer,
    LoanDetailSerializer, CustomerLoansSerializer
)


def calculate_credit_score(customer):
    """Calculate credit score based on historical loan data"""
    loans = Loan.objects.filter(customer=customer)
    if not loans.exists():
        return 0

    score = 0

    # Component 1: Past Loans paid on time (0-20 points)
    total_emis = sum(loan.tenure for loan in loans)
    paid_on_time = sum(loan.emis_paid_on_time for loan in loans)
    if total_emis > 0:
        on_time_percentage = (paid_on_time / total_emis) * 100
        score += min(20, on_time_percentage * 0.2)

    # Component 2: Number of loans taken (0-20 points)
    num_loans = loans.count()
    score += min(20, num_loans * 2)

    # Component 3: Loan activity in current year (0-30 points)
    current_year = date.today().year
    current_year_loans = loans.filter(start_date__year=current_year)
    current_year_volume = sum(float(loan.loan_amount) for loan in current_year_loans)
    score += min(30, current_year_volume / 10000)  # 1 point per 10k

    # Component 4: Loan approved volume (0-30 points)
    total_volume = sum(float(loan.loan_amount) for loan in loans)
    score += min(30, total_volume / 10000)  # 1 point per 10k

    return min(100, score)


def calculate_monthly_installment(loan_amount, interest_rate, tenure):
    """Calculate monthly installment using compound interest"""
    monthly_rate = float(interest_rate) / 100 / 12
    num_payments = tenure

    if monthly_rate == 0:
        return loan_amount / num_payments

    monthly_installment = loan_amount * (monthly_rate * (1 + monthly_rate) ** num_payments) / ((1 + monthly_rate) ** num_payments - 1)
    return Decimal(str(round(monthly_installment, 2)))


@api_view(['POST'])
def register_customer(request):
    """Register a new customer"""
    serializer = CustomerRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        customer = serializer.save()
        response_serializer = CustomerSerializer(customer)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def check_eligibility(request):
    """Check loan eligibility based on credit score"""
    serializer = LoanEligibilitySerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    data = serializer.validated_data
    customer_id = data['customer_id']
    loan_amount = data['loan_amount']
    interest_rate = data['interest_rate']
    tenure = data['tenure']

    try:
        customer = Customer.objects.get(customer_id=customer_id)
    except Customer.DoesNotExist:
        return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

    # Check if sum of current loans > approved limit
    current_loans = Loan.objects.filter(customer=customer)
    current_debt = sum(float(loan.loan_amount) for loan in current_loans)
    if current_debt + float(loan_amount) > float(customer.approved_limit):
        response_data = {
            'customer_id': customer_id,
            'approval': False,
            'interest_rate': interest_rate,
            'tenure': tenure,
            'monthly_installment': 0
        }
        response_serializer = LoanEligibilityResponseSerializer(response_data)
        return Response(response_serializer.data)

    # Check if sum of current EMIs > 50% of monthly salary
    current_emis = sum(float(loan.monthly_installment) for loan in current_loans)
    if current_emis > float(customer.monthly_salary) * 0.5:
        response_data = {
            'customer_id': customer_id,
            'approval': False,
            'interest_rate': interest_rate,
            'tenure': tenure,
            'monthly_installment': 0
        }
        response_serializer = LoanEligibilityResponseSerializer(response_data)
        return Response(response_serializer.data)

    # Calculate credit score
    credit_score = calculate_credit_score(customer)

    # Determine approval and interest rate correction
    approval = False
    corrected_interest_rate = interest_rate

    if credit_score > 50:
        approval = True
    elif 30 < credit_score <= 50:
        approval = True
        if interest_rate < 12:
            corrected_interest_rate = Decimal('12.00')
    elif 10 < credit_score <= 30:
        approval = True
        if interest_rate < 16:
            corrected_interest_rate = Decimal('16.00')
    else:
        approval = False

    # Calculate monthly installment
    monthly_installment = calculate_monthly_installment(loan_amount, corrected_interest_rate, tenure)

    response_data = {
        'customer_id': customer_id,
        'approval': approval,
        'interest_rate': interest_rate,
        'corrected_interest_rate': corrected_interest_rate,
        'tenure': tenure,
        'monthly_installment': monthly_installment
    }

    response_serializer = LoanEligibilityResponseSerializer(response_data)
    return Response(response_serializer.data)


@api_view(['POST'])
def create_loan(request):
    """Create a new loan after eligibility check"""
    serializer = LoanCreationSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    data = serializer.validated_data
    customer_id = data['customer_id']
    loan_amount = data['loan_amount']
    interest_rate = data['interest_rate']
    tenure = data['tenure']

    try:
        customer = Customer.objects.get(customer_id=customer_id)
    except Customer.DoesNotExist:
        return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

    # First check eligibility
    eligibility_data = {
        'customer_id': customer_id,
        'loan_amount': loan_amount,
        'interest_rate': interest_rate,
        'tenure': tenure
    }

    eligibility_request = type('Request', (), {'data': eligibility_data})()
    eligibility_response = check_eligibility(eligibility_request)

    if eligibility_response.status_code != 200:
        return eligibility_response

    eligibility_result = eligibility_response.data

    if not eligibility_result['approval']:
        response_data = {
            'loan_id': None,
            'customer_id': customer_id,
            'loan_approved': False,
            'message': 'Loan not approved based on eligibility criteria',
            'monthly_installment': 0
        }
        response_serializer = LoanCreationResponseSerializer(response_data)
        return Response(response_serializer.data)

    # Create the loan
    corrected_interest_rate = eligibility_result.get('corrected_interest_rate', interest_rate)
    monthly_installment = eligibility_result['monthly_installment']

    start_date = date.today()
    end_date = start_date + timedelta(days=30 * tenure)

    loan = Loan.objects.create(
        customer=customer,
        loan_amount=loan_amount,
        tenure=tenure,
        interest_rate=corrected_interest_rate,
        monthly_installment=monthly_installment,
        start_date=start_date,
        end_date=end_date
    )

    # Update customer's current debt
    customer.current_debt += loan_amount
    customer.save()

    response_data = {
        'loan_id': loan.loan_id,
        'customer_id': customer_id,
        'loan_approved': True,
        'message': 'Loan approved and created successfully',
        'monthly_installment': monthly_installment
    }

    response_serializer = LoanCreationResponseSerializer(response_data)
    return Response(response_serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def view_loan(request, loan_id):
    """View loan details"""
    loan = get_object_or_404(Loan, loan_id=loan_id)
    serializer = LoanDetailSerializer(loan)
    return Response(serializer.data)


@api_view(['GET'])
def view_customer_loans(request, customer_id):
    """View all loans for a customer"""
    customer = get_object_or_404(Customer, customer_id=customer_id)
    loans = Loan.objects.filter(customer=customer)
    serializer = CustomerLoansSerializer(loans, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def api_root(request):
    """API root endpoint"""
    return Response({
        "message": "Welcome to Credit Approval System API",
        "endpoints": {
            "register": "POST /api/register - Register a new customer",
            "check-eligibility": "POST /api/check-eligibility - Check loan eligibility",
            "create-loan": "POST /api/create-loan - Create a new loan",
            "view-loan": "GET /api/view-loan/<loan_id> - View loan details",
            "view-loans": "GET /api/view-loans/<customer_id> - View customer loans"
        }
    })
