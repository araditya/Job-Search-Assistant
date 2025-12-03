# Testing Guide - Job Search Assistant

This guide provides multiple ways to test the Job Search Assistant tool to ensure it's working correctly.

## Quick Test

The fastest way to test the tool is using the automated test script:

```bash
python3 test_tool.py
```

This script will:
- ✅ Check if all dependencies are installed
- ✅ Verify environment configuration (.env file)
- ✅ Test module imports
- ✅ Start the Flask server temporarily
- ✅ Test the /health endpoint
- ✅ Test the /search_jobs endpoint with a sample query
- ✅ Display a summary of all test results

### Expected Output

If everything is working correctly, you should see:

```
============================================================
Test Summary
============================================================
✓ Dependencies: PASSED
✓ Environment: PASSED
✓ Module Import: PASSED
✓ Server Functionality: PASSED

============================================================
✓ All tests passed! ✨
```

## Manual Testing

### 1. Setup

Before testing, ensure you have:

```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env and add your RAPIDAPI_KEY
# RAPIDAPI_KEY=your_actual_key_here
```

### 2. Start the Server

```bash
python3 app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### 3. Test Health Endpoint

In a new terminal:

```bash
curl http://127.0.0.1:5000/health
```

Expected response:
```json
{
  "status": "ok"
}
```

### 4. Test Job Search

```bash
curl -X POST http://127.0.0.1:5000/search_jobs \
  -H "Content-Type: application/json" \
  -d '{"query": "python developer", "page": 1, "num_pages": 1}'
```

Expected response structure:
```json
{
  "jobs": [
    {
      "Job Name": "Senior Python Developer",
      "Company": "TechCo",
      "Location": "Remote",
      "Link": "https://...",
      ...
    }
  ],
  "page": 1,
  "num_pages": 1,
  "total": 10
}
```

### 5. Test with Different Queries

```bash
# Search for data analyst jobs
curl -X POST http://127.0.0.1:5000/search_jobs \
  -H "Content-Type: application/json" \
  -d '{"query": "data analyst in New York"}'

# Search with pagination
curl -X POST http://127.0.0.1:5000/search_jobs \
  -H "Content-Type: application/json" \
  -d '{"query": "software engineer", "page": 1, "num_pages": 2}'
```

## Unit Tests

Run the existing unit tests:

```bash
# Run all tests
python3 -m unittest discover -s . -p "test_*.py"

# Run specific test file
python3 -m unittest test_job_search.py

# Run with verbose output
python3 -m unittest test_job_search.py -v
```

## Testing with Docker

If you prefer to test with Docker:

```bash
# Start all services
docker-compose up -d

# Initialize database
curl -X POST http://localhost:5000/db-init

# Test health
curl http://localhost:5000/health

# Test search
curl -X POST http://localhost:5000/search_jobs \
  -H "Content-Type: application/json" \
  -d '{"query": "developer"}'

# View logs
docker-compose logs backend

# Stop services
docker-compose down
```

## Testing Authentication Features

### 1. Sign Up

```bash
curl -X POST http://localhost:5000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "securepassword123"
  }'
```

### 2. Login

```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "securepassword123"
  }'
```

Save the returned token for authenticated requests.

### 3. Add Favorite (requires token)

```bash
# Replace YOUR_TOKEN with the token from login
curl -X POST http://localhost:5000/favorites \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "job_id": "12345",
    "job_title": "Python Developer",
    "company": "TechCorp",
    "location": "Remote"
  }'
```

## Troubleshooting Tests

### Issue: ImportError when running tests

**Solution:**
```bash
# Make sure you're in the project root directory
cd /path/to/Job-Search-Assistant

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: "RAPIDAPI_KEY not found"

**Solution:**
```bash
# Check if .env file exists
ls -la .env

# If not, copy from example
cp .env.example .env

# Edit .env and add your key
nano .env  # or use your preferred editor
```

### Issue: Port 5000 already in use

**Solution:**
```bash
# Find process using port 5000
lsof -ti:5000

# Kill the process (replace <PID> with actual process ID)
kill -9 <PID>

# Or use a different port by modifying app.py
```

### Issue: No jobs returned from search

**Possible causes:**
1. Invalid or expired RAPIDAPI_KEY
2. RapidAPI rate limit exceeded
3. Network connectivity issues
4. API service temporarily down

**Solution:**
```bash
# Verify API key is valid by testing directly
curl -X GET "https://jsearch.p.rapidapi.com/search?query=python&page=1" \
  -H "X-RapidAPI-Key: YOUR_KEY_HERE" \
  -H "X-RapidAPI-Host: jsearch.p.rapidapi.com"

# Check error.log for details
cat error.log | tail -50
```

## Performance Testing

Test the API performance:

```bash
# Install Apache Bench (if not already installed)
# Ubuntu/Debian: sudo apt-get install apache2-utils
# macOS: already installed

# Run 100 requests with 10 concurrent
ab -n 100 -c 10 -p search.json -T application/json http://127.0.0.1:5000/search_jobs
```

Create `search.json`:
```json
{"query": "python developer", "page": 1, "num_pages": 1}
```

## CI/CD Testing

The repository includes a basic CI configuration. To test locally:

```bash
# Run the same checks that CI would run
python3 -m unittest discover
python3 test_tool.py
```

## Best Practices

1. **Always test after changes**: Run `python3 test_tool.py` after making code changes
2. **Test edge cases**: Try empty queries, special characters, very long queries
3. **Monitor logs**: Check `error.log` for any issues
4. **Test with real data**: Use actual job search queries relevant to your use case
5. **Performance**: Monitor response times for different query types

## Additional Resources

- [QUICK_START.md](QUICK_START.md) - Complete setup guide
- [MANUAL_TEST_STEPS.txt](MANUAL_TEST_STEPS.txt) - Step-by-step manual testing
- [README.md](README.md) - Project overview
- [PRODUCTION_GUIDE.md](PRODUCTION_GUIDE.md) - Deployment guide

## Need Help?

If tests fail:
1. Check the error message carefully
2. Review the troubleshooting section above
3. Check error.log for detailed error traces
4. Ensure all dependencies are installed
5. Verify your RAPIDAPI_KEY is valid
6. Check that no other service is using port 5000

---

**Quick Test Command**: `python3 test_tool.py`
