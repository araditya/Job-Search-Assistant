# Job Search Assistant - Production Deployment Guide

## Overview

This is a full-stack job search application with:
- **Backend**: Flask API with PostgreSQL database
- **Frontend**: React web application
- **Features**: User authentication, favorite jobs, saved searches, pagination

## Prerequisites

- Docker & Docker Compose (for containerized deployment)
- PostgreSQL 15+ (if not using Docker)
- Node.js 18+ (for local frontend development)
- Python 3.13+ (for local backend development)
- RapidAPI key for job search (jsearch endpoint)

## Quick Start with Docker Compose

### 1. Setup Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and add your configuration:
```env
DB_USER=job_user
DB_PASSWORD=your_secure_password
RAPIDAPI_KEY=your_rapidapi_key
JWT_SECRET_KEY=your_jwt_secret_key
FLASK_ENV=production
```

### 2. Start Services

```bash
docker-compose up -d
```

This will start:
- PostgreSQL database on port 5432
- Flask backend on port 5000
- React frontend on port 3000

### 3. Initialize Database

```bash
curl -X POST http://localhost:5000/db-init
```

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **Health Check**: http://localhost:5000/health

## API Endpoints

### Authentication

```
POST   /auth/signup         - Register new user
POST   /auth/login          - Login user (returns JWT token)
GET    /auth/me             - Get current user (requires auth)
```

### Search

```
POST   /search_jobs         - Search for jobs
  Query params: query (required), page (default: 1), num_pages (default: 1)
```

### Favorites

```
GET    /favorites           - Get all favorite jobs (requires auth)
POST   /favorites           - Add job to favorites (requires auth)
DELETE /favorites/<id>      - Remove favorite by ID (requires auth)
DELETE /favorites/job/<job_id> - Remove favorite by job ID (requires auth)
```

### Saved Searches

```
GET    /favorites/searches       - Get all saved searches (requires auth)
POST   /favorites/searches       - Save a search (requires auth)
DELETE /favorites/searches/<id>  - Delete saved search (requires auth)
```

## Database Schema

### Users Table
- `id`: Primary key
- `email`: User email (unique)
- `username`: Username (unique)
- `password_hash`: Hashed password
- `created_at`, `updated_at`: Timestamps

### FavoriteJobs Table
- `id`: Primary key
- `user_id`: Foreign key to users
- `job_id`: Job ID from API
- `job_title`, `company`, `location`: Job details
- `job_data`: Full job object (JSON)
- `created_at`: Timestamp

### SavedSearches Table
- `id`: Primary key
- `user_id`: Foreign key to users
- `search_query`: Search query string
- `description`: Optional description
- `filters`: Filter criteria (JSON)
- `created_at`, `last_searched`: Timestamps

## Local Development

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL=postgresql://localhost/job_search_db
export RAPIDAPI_KEY=your_key

python app.py
```

### Frontend Setup

```bash
cd job-search-app/frontend
npm install
npm start
```

## Deployment Options

### AWS (Recommended)

1. **Use RDS for PostgreSQL**
   ```
   - Create RDS instance
   - Update DATABASE_URL in environment
   ```

2. **Use ECR for Docker Images**
   ```bash
   # Build and push images
   docker tag job_search_backend:latest <aws_account>.dkr.ecr.us-east-1.amazonaws.com/job_search_backend:latest
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <aws_account>.dkr.ecr.us-east-1.amazonaws.com
   docker push <aws_account>.dkr.ecr.us-east-1.amazonaws.com/job_search_backend:latest
   ```

3. **Use ECS for Container Orchestration**
   - Create ECS cluster
   - Define task definitions
   - Create services for backend and frontend

### Heroku

```bash
# Install Heroku CLI
heroku login

# Create app
heroku create job-search-app

# Add PostgreSQL add-on
heroku addons:create heroku-postgresql:standard-0 -a job-search-app

# Set environment variables
heroku config:set RAPIDAPI_KEY=your_key -a job-search-app
heroku config:set JWT_SECRET_KEY=your_secret -a job-search-app

# Deploy
git push heroku main
```

### DigitalOcean App Platform

1. Connect GitHub repository
2. Create app from Dockerfile
3. Add PostgreSQL database service
4. Set environment variables
5. Deploy

## Security Considerations

1. **Change JWT_SECRET_KEY** in production
2. **Use HTTPS** with SSL certificates
3. **Set CORS properly** for your domain
4. **Use environment-based secrets** (never commit .env)
5. **Enable database backups**
6. **Use strong database passwords**
7. **Implement rate limiting** on API endpoints
8. **Validate and sanitize** all user inputs
9. **Use connection pooling** for database
10. **Monitor logs** for suspicious activity

## Monitoring & Logging

- Backend logs: Check `error.log` file
- Database logs: Check PostgreSQL logs
- Frontend errors: Check browser console

For production, integrate with:
- Sentry (error tracking)
- DataDog (monitoring)
- CloudWatch (AWS logging)

## Scaling Considerations

1. **Database**: Increase RDS instance size, enable read replicas
2. **Backend**: Use load balancer (ALB/NLB), auto-scaling groups
3. **Frontend**: Use CDN (CloudFront), cache static assets
4. **Cache**: Add Redis for API caching
5. **Queue**: Use Celery + Redis for background jobs

## Troubleshooting

### Database Connection Error
```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# Check database logs
docker logs job_search_db
```

### Backend Not Starting
```bash
# Check backend logs
docker logs job_search_backend

# Verify database initialization
curl -X POST http://localhost:5000/db-init
```

### Frontend Can't Connect to Backend
- Verify backend is running: `curl http://localhost:5000/health`
- Check CORS settings in backend
- Verify proxy setting in frontend package.json

## Support & Documentation

- API Documentation: `http://localhost:5000/docs` (add Swagger integration)
- Backend README: `backend/README.md`
- Frontend README: `job-search-app/frontend/README.md`

## License

MIT License - See LICENSE file for details
