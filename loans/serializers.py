from rest_framework import serializers
from .models import Customer, Loan


class CustomerSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    monthly_income = serializers.SerializerMethodField()
    approved_limit = serializers.SerializerMethodField()
    phone_number = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = ['customer_id', 'name', 'age', 'monthly_income', 'approved_limit', 'phone_number']

    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def get_monthly_income(self, obj):
        return int(obj.monthly_salary)

    def get_approved_limit(self, obj):
        return int(obj.approved_limit)

    def get_phone_number(self, obj):
        # Return as integer for API response
        try:
            return int(obj.phone_number)
        except (ValueError, TypeError):
            return obj.phone_number


class CustomerRegistrationSerializer(serializers.ModelSerializer):
    monthly_income = serializers.DecimalField(max_digits=15, decimal_places=2, source='monthly_salary')

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'age', 'monthly_income', 'phone_number']

    def create(self, validated_data):
        # Calculate approved limit: 36 * monthly_salary, rounded to nearest lakh
        monthly_salary = validated_data['monthly_salary']
        approved_limit = round(36 * float(monthly_salary) / 100000) * 100000
        validated_data['approved_limit'] = approved_limit
        return super().create(validated_data)


class LoanEligibilitySerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    loan_amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    interest_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    tenure = serializers.IntegerField()


class LoanEligibilityResponseSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    approval = serializers.BooleanField()
    interest_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    corrected_interest_rate = serializers.DecimalField(max_digits=5, decimal_places=2, required=False)
    tenure = serializers.IntegerField()
    monthly_installment = serializers.DecimalField(max_digits=15, decimal_places=2)


class LoanCreationSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    loan_amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    interest_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    tenure = serializers.IntegerField()


class LoanCreationResponseSerializer(serializers.Serializer):
    loan_id = serializers.IntegerField(required=False, allow_null=True)
    customer_id = serializers.IntegerField()
    loan_approved = serializers.BooleanField()
    message = serializers.CharField(required=False)
    monthly_installment = serializers.DecimalField(max_digits=15, decimal_places=2, required=False)


class LoanDetailSerializer(serializers.ModelSerializer):
    customer = serializers.SerializerMethodField()

    class Meta:
        model = Loan
        fields = ['loan_id', 'customer', 'loan_amount', 'interest_rate', 'monthly_installment', 'tenure']

    def get_customer(self, obj):
        return {
            'id': obj.customer.customer_id,
            'first_name': obj.customer.first_name,
            'last_name': obj.customer.last_name,
            'phone_number': obj.customer.phone_number,
            'age': obj.customer.age
        }


class CustomerLoansSerializer(serializers.ModelSerializer):
    loan_amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    interest_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    monthly_installment = serializers.DecimalField(max_digits=15, decimal_places=2)
    repayments_left = serializers.SerializerMethodField()

    class Meta:
        model = Loan
        fields = ['loan_id', 'loan_amount', 'interest_rate', 'monthly_installment', 'repayments_left']

    def get_repayments_left(self, obj):
        return obj.repayments_left