# Credit Approval System

A Django REST API system for credit approval and loan management.

## Features

- Customer registration with automatic credit limit calculation
- Credit scoring based on historical loan data
- Loan eligibility checking with interest rate adjustments
- Loan creation and management
- Background data ingestion from Excel files
- Docker containerization

## Setup

### Prerequisites

- Docker and Docker Compose
- Python 3.11+ (if running locally)

### 🚀 Deploy to Render (Production)

**Quickest way to get started!**

1. Push your code to GitHub
2. Go to [Render Dashboard](https://dashboard.render.com)
3. Click "New" → "Blueprint"
4. Connect your repository
5. Deploy! (Auto-detects `render.yaml`)

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions or [README_RENDER.md](README_RENDER.md) for quick start.

## Quick Start with Docker (Local)

1. Clone the repository and navigate to the project directory
2. Place your Excel data files (`customer_data.xlsx` and `loan_data.xlsx`) in the project root
3. Run the application:

```bash
docker-compose up --build
```

This will start:
- Django web application on port 8000
- PostgreSQL database on port 5432
- Redis for Celery on port 6379
- Celery worker for background tasks

### Manual Setup (without Docker)

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up PostgreSQL database and update settings.py with your database credentials

3. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. Populate test data:
```bash
python populate_test_data.py
```

5. Start Redis server (for Celery)

6. Start Celery worker:
```bash
celery -A credit_approval_system worker --loglevel=info
```

7. Start Django server:
```bash
python manage.py runserver
```

## API Endpoints

### Register Customer
**POST** `/api/register`

Request body:
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "age": 30,
  "monthly_income": 50000,
  "phone_number": "1234567890"
}
```

### Check Loan Eligibility
**POST** `/api/check-eligibility`

Request body:
```json
{
  "customer_id": 1,
  "loan_amount": 200000,
  "interest_rate": 10,
  "tenure": 24
}
```

### Create Loan
**POST** `/api/create-loan`

Request body:
```json
{
  "customer_id": 1,
  "loan_amount": 200000,
  "interest_rate": 10,
  "tenure": 24
}
```

### View Loan Details
**GET** `/api/view-loan/<loan_id>`

### View Customer Loans
**GET** `/api/view-loans/<customer_id>`

## Data Ingestion

To ingest data from Excel files:

```bash
python manage.py ingest_data --customer-file customer_data.xlsx --loan-file loan_data.xlsx
```

## Testing

Run the test script:

```bash
python test_api.py
```

## Credit Scoring Logic

The system calculates credit scores based on:

1. **Past Loans Paid on Time** (0-20 points): Percentage of EMIs paid on time
2. **Number of Loans Taken** (0-20 points): 2 points per loan (max 20)
3. **Loan Activity in Current Year** (0-30 points): 1 point per ₹10,000 loaned
4. **Loan Approved Volume** (0-30 points): 1 point per ₹10,000 total loan volume

### Approval Rules

- **Credit Score > 50**: Approve loan
- **30 < Credit Score ≤ 50**: Approve with minimum 12% interest rate
- **10 < Credit Score ≤ 30**: Approve with minimum 16% interest rate
- **Credit Score ≤ 10**: Reject loan

### Additional Checks

- Reject if sum of current loans > approved limit
- Reject if sum of current EMIs > 50% of monthly salary

## Architecture

- **Django 4+** with Django REST Framework
- **PostgreSQL** for data storage
- **Redis** for Celery message broker
- **Celery** for background task processing
- **Docker** for containerization

## Deployment

This application is ready for deployment to:

- ✅ **Render** - One-click deployment with `render.yaml`
- ✅ **Heroku** - With minor configuration changes
- ✅ **AWS/GCP/Azure** - Via Docker container
- ✅ **Any Docker-compatible platform**

See [DEPLOYMENT.md](DEPLOYMENT.md) for comprehensive deployment guides.

## Documentation

- [DEPLOYMENT.md](DEPLOYMENT.md) - Complete deployment guide
- [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) - Pre-deployment checklist
- [RENDER_SUMMARY.md](RENDER_SUMMARY.md) - Render deployment readiness
- [README_RENDER.md](README_RENDER.md) - Quick start for Render
- [DEPLOYMENT_CHANGES.md](DEPLOYMENT_CHANGES.md) - Summary of all changes