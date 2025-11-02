# Deployment Guide for Render

This guide will help you deploy the Credit Approval System to Render.

## Prerequisites

1. A GitHub repository containing this project
2. A Render account (free tier works)

## Deployment Steps

### 1. Prepare Your Repository

Ensure your repository has:
- `Dockerfile` in the `credit_approval_system` directory
- `render.yaml` in the `credit_approval_system` directory
- `customer_data.xlsx` and `loan_data.xlsx` in the `credit_approval_system` directory
- All necessary Python files

### 2. Deploy to Render

There are two ways to deploy:

#### Option A: Using render.yaml (Recommended)

1. Go to your Render Dashboard
2. Click "New" → "Blueprint"
3. Connect your GitHub repository
4. Select your repository
5. Render will automatically detect `render.yaml`
6. Click "Apply" and deploy

#### Option B: Manual Setup

1. **Create PostgreSQL Database:**
   - Go to Dashboard → New → PostgreSQL
   - Name it: `credit-approval-db`
   - Plan: Free
   - Region: Choose closest to you
   - Click "Create Database"

2. **Create Web Service:**
   - Go to Dashboard → New → Web Service
   - Connect your GitHub repository
   - Settings:
     - **Name:** credit-approval-system
     - **Region:** Same as database
     - **Branch:** main (or your default branch)
     - **Root Directory:** credit_approval_system
     - **Environment:** Docker
     - **Dockerfile Path:** Dockerfile
     - **Docker Context:** .
     - **Instance Type:** Free

3. **Configure Environment Variables:**
   - Click on your web service → Environment
   - Add these variables:
     ```
     DEBUG=False
     SECRET_KEY=<generate-a-secure-random-key>
     DB_NAME=<from-postgres-database>
     DB_USER=<from-postgres-database>
     DB_PASSWORD=<from-postgres-database>
     DB_HOST=<from-postgres-database>
     DB_PORT=<from-postgres-database>
     ALLOWED_HOSTS=your-app-name.onrender.com
     ```

### 3. Deploy Your Service

1. Click "Deploy" or "Save Changes"
2. Wait for the build to complete (can take 5-10 minutes)
3. Your app will be live at: `https://your-app-name.onrender.com`

## Post-Deployment

### Verify Deployment

1. Visit your app URL
2. You should see the API root endpoint with available endpoints
3. Test the API using curl or Postman

### Example API Calls

```bash
# Register a customer
curl -X POST https://your-app-name.onrender.com/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "age": 30,
    "monthly_income": 50000,
    "phone_number": "1234567890"
  }'

# Check eligibility
curl -X POST https://your-app-name.onrender.com/api/check-eligibility \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 1,
    "loan_amount": 200000,
    "interest_rate": 10,
    "tenure": 24
  }'

# View loans
curl https://your-app-name.onrender.com/api/view-loans/1
```

## Troubleshooting

### Build Fails

- Check that all Excel files are in the correct location
- Ensure Dockerfile is properly formatted
- Check build logs for specific errors

### Database Connection Issues

- Verify environment variables are set correctly
- Check that database internal hostname is used
- Ensure database is in the same region as web service

### Data Not Loading

- Check that customer_data.xlsx and loan_data.xlsx are included in your repository
- Verify file paths in the ingestion script
- Check application logs for data ingestion errors

### App Not Starting

- Check that PORT environment variable is being used
- Verify all required Python packages are in requirements.txt
- Review application logs for startup errors

## Environment Variables Reference

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| DEBUG | Django debug mode | Yes | False |
| SECRET_KEY | Django secret key | Yes | Generated |
| DB_NAME | PostgreSQL database name | Yes | credit_db |
| DB_USER | PostgreSQL username | Yes | postgres |
| DB_PASSWORD | PostgreSQL password | Yes | password |
| DB_HOST | PostgreSQL host | Yes | db |
| DB_PORT | PostgreSQL port | Yes | 5432 |
| ALLOWED_HOSTS | Comma-separated allowed hosts | Yes | * |
| REDIS_URL | Redis connection URL (optional) | No | redis://redis:6379/0 |
| PORT | Server port | Yes | 8000 |

## Support

For issues or questions:
1. Check the build/deploy logs in Render dashboard
2. Review application logs
3. Verify all files are committed to repository
4. Check that database is running and accessible

## Notes

- Free tier services may spin down after 15 minutes of inactivity
- First request after spin-down may take 30-60 seconds
- Consider upgrading to paid tier for production use
- Redis/Celery are optional - the app will run synchronously without them

