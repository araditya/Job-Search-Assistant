# Test Examples - Job Search Assistant

This file contains example test scenarios to verify different aspects of the Job Search Assistant.

## Example 1: Basic Job Search

### Test: Search for Python Developer Jobs

```bash
curl -X POST http://127.0.0.1:5000/search_jobs \
  -H "Content-Type: application/json" \
  -d '{
    "query": "python developer",
    "page": 1,
    "num_pages": 1
  }'
```

**Expected Result:**
- Status: 200 OK
- Response contains `jobs` array
- Each job has: Job Name, Company, Location, Link
- Total count is returned

---

## Example 2: Location-Specific Search

### Test: Search for Remote Data Analyst Jobs

```bash
curl -X POST http://127.0.0.1:5000/search_jobs \
  -H "Content-Type: application/json" \
  -d '{
    "query": "data analyst remote",
    "page": 1,
    "num_pages": 1
  }'
```

**Expected Result:**
- Jobs should be filtered for remote or data analyst positions
- Location field should indicate "Remote" where applicable

---

## Example 3: Multiple Pages

### Test: Fetch Multiple Pages of Results

```bash
curl -X POST http://127.0.0.1:5000/search_jobs \
  -H "Content-Type: application/json" \
  -d '{
    "query": "software engineer",
    "page": 1,
    "num_pages": 2
  }'
```

**Expected Result:**
- More results returned (approximately 20 jobs)
- Results span multiple pages

---

## Example 4: Natural Language Query

### Test: Use Natural Language to Search

```bash
curl -X POST http://127.0.0.1:5000/search_jobs \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Find me frontend developer jobs in San Francisco with React experience"
  }'
```

**Expected Result:**
- NLP parser extracts relevant parameters
- Jobs match the specified criteria
- Response includes `parsed_params` showing extracted filters

---

## Example 5: Health Check

### Test: Verify Service is Running

```bash
curl http://127.0.0.1:5000/health
```

**Expected Result:**
```json
{
  "status": "ok"
}
```

---

## Example 6: Error Handling - Missing Query

### Test: Missing Required Parameter

```bash
curl -X POST http://127.0.0.1:5000/search_jobs \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Expected Result:**
- Status: 400 Bad Request
- Error message: "Missing required parameter: query"

---

## Example 7: Authentication - Sign Up

### Test: Create New User Account

```bash
curl -X POST http://127.0.0.1:5000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "testuser@example.com",
    "username": "testuser",
    "password": "SecurePassword123!"
  }'
```

**Expected Result:**
- Status: 201 Created
- Returns access token
- User is created in database

---

## Example 8: Authentication - Login

### Test: Login with Existing User

```bash
curl -X POST http://127.0.0.1:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "testuser@example.com",
    "password": "SecurePassword123!"
  }'
```

**Expected Result:**
- Status: 200 OK
- Returns access token
- Token can be used for authenticated requests

**Save the token:**
```bash
# Extract token (Linux/Mac)
TOKEN=$(curl -s -X POST http://127.0.0.1:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"testuser@example.com","password":"SecurePassword123!"}' \
  | jq -r '.access_token')

echo $TOKEN
```

---

## Example 9: Add Favorite Job (Authenticated)

### Test: Save a Job to Favorites

**Prerequisites:** Must have a valid token from login

```bash
# Replace YOUR_TOKEN with actual token
curl -X POST http://127.0.0.1:5000/favorites \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "job_id": "abc123",
    "job_title": "Senior Python Developer",
    "company": "Tech Corp",
    "location": "San Francisco, CA",
    "url": "https://example.com/job/abc123"
  }'
```

**Expected Result:**
- Status: 201 Created
- Favorite is saved to database
- Returns confirmation with job details

---

## Example 10: Get Favorite Jobs (Authenticated)

### Test: Retrieve User's Saved Jobs

```bash
# Replace YOUR_TOKEN with actual token
curl -X GET http://127.0.0.1:5000/favorites \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Expected Result:**
- Status: 200 OK
- Returns array of saved jobs
- Each job includes all saved details

---

## Example 11: Form Data Request

### Test: Submit Query as Form Data

```bash
curl -X POST http://127.0.0.1:5000/search_jobs \
  -F "query=javascript developer" \
  -F "page=1" \
  -F "num_pages=1"
```

**Expected Result:**
- Same as JSON request
- Returns job results

---

## Example 12: Database Initialization

### Test: Initialize Database Tables

```bash
curl -X POST http://127.0.0.1:5000/db-init
```

**Expected Result:**
- Status: 200 OK
- Message: "Database initialized"
- All tables created

---

## Running All Examples

You can run all these examples automatically using the test script:

```bash
python3 test_tool.py
```

Or create a bash script to run them sequentially:

```bash
#!/bin/bash
# save as run_examples.sh

echo "Testing Health Endpoint..."
curl -s http://127.0.0.1:5000/health | jq

echo -e "\nTesting Job Search..."
curl -s -X POST http://127.0.0.1:5000/search_jobs \
  -H "Content-Type: application/json" \
  -d '{"query":"python developer","page":1,"num_pages":1}' | jq '.jobs[0]'

echo -e "\nTesting Error Handling..."
curl -s -X POST http://127.0.0.1:5000/search_jobs \
  -H "Content-Type: application/json" \
  -d '{}' | jq

echo -e "\nAll examples completed!"
```

---

## Performance Testing

### Load Test with Apache Bench

```bash
# Create a JSON file
echo '{"query":"developer","page":1,"num_pages":1}' > search_payload.json

# Run 100 requests, 10 concurrent
ab -n 100 -c 10 -p search_payload.json -T application/json \
  http://127.0.0.1:5000/search_jobs

# Check results for:
# - Requests per second
# - Average response time
# - Failed requests (should be 0)
```

---

## Automated Testing with Python

Save this as `run_examples.py`:

```python
#!/usr/bin/env python3
import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_search():
    """Test job search"""
    print("Testing job search...")
    payload = {
        "query": "python developer",
        "page": 1,
        "num_pages": 1
    }
    response = requests.post(f"{BASE_URL}/search_jobs", json=payload)
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Found {data.get('total', 0)} jobs")
    if data.get('jobs'):
        print(f"First job: {data['jobs'][0]['Job Name']}")
    print()

def test_error():
    """Test error handling"""
    print("Testing error handling...")
    response = requests.post(f"{BASE_URL}/search_jobs", json={})
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

if __name__ == "__main__":
    test_health()
    test_search()
    test_error()
    print("All tests completed!")
```

Run with:
```bash
python3 run_examples.py
```

---

## Notes

- Make sure the Flask server is running before executing these examples
- Replace placeholder tokens with actual tokens from login
- Some examples require database setup (run `/db-init` first)
- API rate limits may apply depending on your RapidAPI plan
- For production testing, use environment-specific URLs

For more detailed testing documentation, see [TESTING.md](TESTING.md).
