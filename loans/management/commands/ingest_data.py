from django.core.management.base import BaseCommand
from loans.tasks import ingest_customer_data, ingest_loan_data
import os


class Command(BaseCommand):
    help = 'Ingest customer and loan data from Excel files'

    def add_arguments(self, parser):
        # Calculate absolute paths to data files
        # Command is at: loans/management/commands/ingest_data.py
        # Files are at: credit_approval_system/customer_data.xlsx and loan_data.xlsx
        command_dir = os.path.dirname(__file__)
        commands_dir = os.path.dirname(command_dir)
        management_dir = os.path.dirname(commands_dir)
        loans_dir = os.path.dirname(management_dir)
        project_dir = os.path.dirname(loans_dir)
        
        default_customer = os.path.join(project_dir, 'customer_data.xlsx')
        default_loan = os.path.join(project_dir, 'loan_data.xlsx')

        parser.add_argument(
            '--customer-file',
            type=str,
            help='Path to customer data Excel file',
            default=default_customer
        )
        parser.add_argument(
            '--loan-file',
            type=str,
            help='Path to loan data Excel file',
            default=default_loan
        )

    def handle(self, *args, **options):
        customer_file = options['customer_file']
        loan_file = options['loan_file']

        self.stdout.write('Starting data ingestion...')

        # Check if files exist
        if not os.path.exists(customer_file):
            self.stderr.write(f'Customer data file not found: {customer_file}')
            return

        if not os.path.exists(loan_file):
            self.stderr.write(f'Loan data file not found: {loan_file}')
            return

        # Try to use Celery if available, otherwise run synchronously
        try:
            # Trigger background tasks
            customer_task = ingest_customer_data.delay(customer_file)
            loan_task = ingest_loan_data.delay(loan_file)
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Data ingestion tasks started. Customer task ID: {customer_task.id}, '
                    f'Loan task ID: {loan_task.id}'
                )
            )
        except Exception as e:
            # Fallback to synchronous execution if Celery not available
            self.stdout.write(self.style.WARNING(f'Celery not available, running synchronously: {str(e)}'))
            self.stdout.write('Ingesting customer data...')
            ingest_customer_data(customer_file)
            self.stdout.write('Ingesting loan data...')
            ingest_loan_data(loan_file)
            self.stdout.write(self.style.SUCCESS('Data ingestion completed synchronously!'))