# Quick Start Guide - Production Setup

## 🚀 Fastest Way to Test the Tool

### Option 1: Automated Testing (Recommended)

```bash
# One command to test everything
python3 test_tool.py
```

This will:
- ✅ Check all dependencies
- ✅ Verify configuration
- ✅ Test the API endpoints
- ✅ Provide a detailed report

### Option 2: Quick Setup & Test Script

```bash
# Setup and test in one go
./quick_test.sh
```

This script will install dependencies, check configuration, and run all tests.

For detailed test examples, see [TEST_EXAMPLES.md](TEST_EXAMPLES.md) and [TESTING.md](TESTING.md).

---

## 🚀 Fastest Way to Deploy Locally

### Prerequisites
- Docker & Docker Compose installed
- Your RapidAPI key

### Step 1: Create .env file
```bash
cp .env.example .env
```

Edit `.env`:
```
RAPIDAPI_KEY=your_key_here
JWT_SECRET_KEY=your-secret-key
DB_PASSWORD=your_secure_password
```

### Step 2: Start Everything
```bash
docker-compose up -d
```

### Step 3: Initialize Database
```bash
curl -X POST http://localhost:5000/db-init
```

### Step 4: Visit the App
- Frontend: http://localhost:3000
- Backend: http://localhost:5000
- Health: http://localhost:5000/health

## 📋 What Was Added

### 1. **Database Support**
- PostgreSQL with User, FavoriteJobs, SavedSearches tables
- Automatic schema creation

### 2. **User Authentication**
- Sign up / Login with JWT tokens
- Protected API endpoints
- 30-day token expiration

### 3. **User Features**
- Save favorite jobs
- Save search queries
- Access history

### 4. **Pagination**
- Load more button
- 10 jobs per page
- Accumulate results

### 5. **Docker Setup**
- Complete containerization
- Easy deployment to cloud
- Automatic service orchestration

## 🔧 API Examples

### Sign Up
```bash
curl -X POST http://localhost:5000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "john_doe",
    "password": "secure_password"
  }'
```

### Login
```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "secure_password"
  }'
```

### Search Jobs (with pagination)
```bash
curl -X POST http://localhost:5000/search_jobs \
  -H "Content-Type: application/json" \
  -d '{
    "query": "python developer",
    "page": 1,
    "num_pages": 1
  }'
```

### Add to Favorites (requires token)
```bash
curl -X POST http://localhost:5000/favorites \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "job_id": "12345",
    "job_title": "Senior Python Developer",
    "company": "Google",
    "location": "Remote"
  }'
```

## 🐳 Docker Compose Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs backend
docker-compose logs frontend
docker-compose logs postgres

# Restart a service
docker-compose restart backend

# Remove everything (including volumes)
docker-compose down -v
```

## 📦 Deployment Options

### AWS
1. RDS for database
2. ECR for images
3. ECS for container orchestration
4. ALB for load balancing

### Heroku
```bash
heroku create job-search-app
heroku addons:create heroku-postgresql:standard-0
heroku config:set RAPIDAPI_KEY=your_key
git push heroku main
```

### DigitalOcean
1. Connect GitHub
2. Auto-deploy from docker-compose.yml
3. Add PostgreSQL database service

## 🔒 Important Security Notes

Before deploying to production:
1. Change `JWT_SECRET_KEY` in `.env`
2. Use strong database password
3. Set `FLASK_ENV=production`
4. Enable HTTPS
5. Use secrets manager for API keys
6. Add rate limiting
7. Enable database backups

## 📚 Documentation Files

- `PRODUCTION_GUIDE.md` - Full deployment guide
- `IMPLEMENTATION_SUMMARY.md` - What was added
- `backend/README.md` - Backend setup
- `job-search-app/frontend/README.md` - Frontend setup

## ✅ Checklist

- [ ] Copy `.env.example` to `.env`
- [ ] Add your RAPIDAPI_KEY
- [ ] Run `docker-compose up -d`
- [ ] Initialize database: `curl -X POST http://localhost:5000/db-init`
- [ ] Test: http://localhost:3000
- [ ] Create user account
- [ ] Search for jobs
- [ ] Click Load More

## 🐛 Troubleshooting

### Port already in use
```bash
# Kill process on port 5000/3000/5432
lsof -ti:5000 | xargs kill -9
```

### Database connection error
```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# Check logs
docker logs job_search_db
```

### Frontend can't reach backend
- Verify backend health: `curl http://localhost:5000/health`
- Check if proxy is set correctly in frontend

### Changes not showing
```bash
# Rebuild images
docker-compose down
docker-compose up -d --build
```

## 📞 Support

For issues:
1. Check logs: `docker-compose logs -f backend`
2. Read PRODUCTION_GUIDE.md
3. Verify .env file
4. Check internet connection (API calls)

## 🎯 Next Steps

1. **Test locally** with Docker Compose
2. **Add more features**:
   - Email notifications
   - Advanced filters
   - Analytics
3. **Deploy to cloud**:
   - AWS, Heroku, or DigitalOcean
4. **Monitor** with Sentry + DataDog
5. **Scale** as traffic grows

---

**Ready to go!** Start with: `docker-compose up -d`
