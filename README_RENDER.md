# Credit Approval System - Render Deployment

## 🚀 Quick Start

Your Credit Approval System is **100% ready** for deployment to Render!

### Deploy in 3 Steps:

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Ready for Render deployment"
   git push origin main
   ```

2. **Deploy on Render**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New" → "Blueprint"
   - Connect your GitHub repository
   - Render will auto-detect `render.yaml`

3. **Done!**
   - Wait 5-10 minutes for build
   - Your API will be live!

## 📋 What's Included

### ✅ All Assignment Requirements
- Django 4+ with Django REST Framework
- PostgreSQL database
- Docker configuration
- All 5 API endpoints
- Background workers (Celery with fallback)
- Credit scoring algorithm
- Interest rate correction
- EMI calculation (compound interest)
- Comprehensive error handling

### ✅ Production Features
- Environment variable configuration
- Automatic migrations
- Data ingestion on deployment
- Static files handling
- Graceful fallbacks
- Health checks
- Logging

### ✅ Documentation
- `DEPLOYMENT.md` - Complete deployment guide
- `DEPLOYMENT_CHECKLIST.md` - Pre-deployment checklist
- `RENDER_SUMMARY.md` - Deployment readiness summary
- `README.md` - Original project documentation

## 🔗 API Endpoints

Once deployed, your API will be available at:
```
https://your-app-name.onrender.com
```

### Available Endpoints:

#### 1. Register Customer
```bash
POST /api/register
```
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "age": 30,
  "monthly_income": 50000,
  "phone_number": "1234567890"
}
```

#### 2. Check Eligibility
```bash
POST /api/check-eligibility
```
```json
{
  "customer_id": 1,
  "loan_amount": 200000,
  "interest_rate": 10,
  "tenure": 24
}
```

#### 3. Create Loan
```bash
POST /api/create-loan
```
```json
{
  "customer_id": 1,
  "loan_amount": 200000,
  "interest_rate": 10,
  "tenure": 24
}
```

#### 4. View Loan
```bash
GET /api/view-loan/<loan_id>
```

#### 5. View Customer Loans
```bash
GET /api/view-loans/<customer_id>
```

## 🧪 Test Your Deployment

After deployment, test with:

```bash
# Test API root
curl https://your-app.onrender.com/

# Register a customer
curl -X POST https://your-app.onrender.com/api/register \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Test","last_name":"User","age":30,"monthly_income":50000,"phone_number":"1234567890"}'

# Check eligibility
curl -X POST https://your-app.onrender.com/api/check-eligibility \
  -H "Content-Type: application/json" \
  -d '{"customer_id":1,"loan_amount":200000,"interest_rate":10,"tenure":24}'
```

## 📊 Credit Scoring Logic

The system calculates credit scores based on:

1. **Past Loans Paid on Time** (0-20 points)
   - Percentage of EMIs paid on time

2. **Number of Loans Taken** (0-20 points)
   - 2 points per loan (max 20)

3. **Loan Activity in Current Year** (0-30 points)
   - 1 point per ₹10,000 loaned

4. **Loan Approved Volume** (0-30 points)
   - 1 point per ₹10,000 total loan volume

### Approval Rules:
- **Score > 50**: Approve loan ✅
- **30 < Score ≤ 50**: Approve with min 12% interest ✅
- **10 < Score ≤ 30**: Approve with min 16% interest ✅
- **Score ≤ 10**: Reject loan ❌

### Additional Checks:
- ❌ Reject if current loans > approved limit
- ❌ Reject if current EMIs > 50% of monthly salary

## 🛠️ Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Setup database
python manage.py migrate

# Run server
python manage.py runserver

# Run with Docker
docker-compose up
```

## 📁 Project Structure

```
credit_approval_system/
├── Dockerfile              # Production Docker configuration
├── render.yaml             # Render deployment blueprint
├── build.sh                # Startup script
├── requirements.txt        # Python dependencies
├── customer_data.xlsx      # Sample customer data
├── loan_data.xlsx          # Sample loan data
├── credit_approval_system/ # Django project
│   ├── settings.py         # Production-ready settings
│   ├── urls.py             # URL routing
│   └── celery.py           # Celery configuration
├── loans/                  # Django app
│   ├── models.py           # Data models
│   ├── views.py            # API views
│   ├── serializers.py      # API serializers
│   ├── tasks.py            # Background tasks
│   └── urls.py             # App URLs
└── DEPLOYMENT.md           # Detailed deployment guide
```

## 🔍 Verifying Deployment

1. Check build logs in Render dashboard
2. Verify database migrations completed
3. Confirm data ingestion finished
4. Test all API endpoints
5. Review application logs

## ⚠️ Important Notes

### Free Tier
- Services spin down after 15 minutes of inactivity
- First request may take 30-60 seconds
- Consider upgrading for production

### Data
- Customer and loan data auto-load on first deployment
- Excel files must be in the repository
- Data ingestion only runs if database is empty

### Environment
- All settings use environment variables
- SECRET_KEY auto-generates on Render
- Database credentials from PostgreSQL service

## 🆘 Troubleshooting

See `DEPLOYMENT.md` for detailed troubleshooting guide.

Common issues:
- **Build fails**: Check Dockerfile and requirements.txt
- **Database errors**: Verify environment variables
- **Data not loaded**: Check file paths and logs
- **502 errors**: Review application logs

## 📝 Next Steps

1. ✅ Deploy to Render
2. ✅ Test all endpoints
3. ✅ Monitor logs
4. ✅ Add monitoring (optional)
5. ✅ Upgrade plan for production (optional)

## 🎉 Success!

Once deployed, share your API URL:
```
https://your-app-name.onrender.com
```

All endpoints are ready to use!

---

**Need help?** Check:
- `DEPLOYMENT.md` - Detailed instructions
- `DEPLOYMENT_CHECKLIST.md` - Verification steps
- `RENDER_SUMMARY.md` - Deployment readiness

**Ready to deploy?** Start now at [dashboard.render.com](https://dashboard.render.com)

