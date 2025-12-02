# Phase 9: AI Features - Deployment Checklist

## Pre-Deployment Setup (Do These First)

### ✅ Step 1: Environment Configuration
```bash
# Option A: Set environment variable (Linux/macOS)
export OPENAI_API_KEY=sk-your-actual-key-here

# Option B: Set in PowerShell (Windows)
$env:OPENAI_API_KEY="sk-your-actual-key-here"

# Option C: Add to backend/.env file
echo "OPENAI_API_KEY=sk-your-actual-key-here" >> backend/.env

# Verify it's set
echo $env:OPENAI_API_KEY  # Windows
echo $OPENAI_API_KEY      # Mac/Linux
```

### ✅ Step 2: Install New Dependencies
```bash
cd backend
pip install -r requirements.txt

# Verify installations
python -c "import openai; print('✓ OpenAI')"
python -c "import spacy; print('✓ Spacy')"
python -c "import nltk; print('✓ NLTK')"
python -c "import linkedin_api; print('✓ LinkedIn API')"
```

### ✅ Step 3: Initialize Database (if not already done)
```bash
# While backend is running
curl -X POST http://localhost:5000/db-init

# Expected response: {"message": "Database initialized"}
```

### ✅ Step 4: Restart Backend
```bash
# Kill existing Flask process (Ctrl+C)
# Then restart:
python backend/app.py

# You should see in output:
# * Running on http://127.0.0.1:5000
# * Flask is running in development mode
```

### ✅ Step 5: Verify Backend is Running
```bash
# Test health check
curl http://localhost:5000/health

# Expected: {"status": "ok"}
```

---

## Feature Testing (Do These Next)

### Test 1: NLP Query Parser
```bash
# Test basic query parsing
curl -X POST http://localhost:5000/ai/parse-query \
  -H "Content-Type: application/json" \
  -d '{"query": "Senior Python developer in San Francisco, remote, 150k salary"}'

# Expected response includes:
# - search_query: "Senior Python developer"
# - location: "San Francisco"
# - job_type: "remote"
# - salary_range: {min: 150000, max: 150000}
```

### Test 2: Hiring Manager Discovery
```bash
# Find managers at a company
curl -X POST http://localhost:5000/ai/find-hiring-managers \
  -H "Content-Type: application/json" \
  -d '{"company_name": "Google", "job_title": "Recruiter"}'

# Should return list of managers (or fallback templates)
```

### Test 3: Frontend Integration

**Step 1: Start Frontend**
```bash
cd job-search-app/frontend
npm start  # Should open http://localhost:3000
```

**Step 2: Test Natural Language Checkbox**
- [ ] See "Natural Language" checkbox appears
- [ ] Unchecked by default
- [ ] Clicking toggles the state

**Step 3: Test NLP Search**
- [ ] Check the "Natural Language" checkbox
- [ ] Enter: "Senior Python developer in San Francisco, remote, $150k"
- [ ] Click "Search"
- [ ] See parsed parameters displayed below search bar
- [ ] See results appear in table

**Step 4: Test Cover Letter Generation**
- [ ] Click "Letter" button on a job
- [ ] Wait 3-5 seconds for generation
- [ ] Button shows "..." while loading
- [ ] Cover letter appears in expandable section
- [ ] Click expand button (▶) to collapse/expand

**Step 5: Test Hiring Manager Search**
- [ ] Click "Manager" button on a job
- [ ] Wait 1-2 seconds
- [ ] Button shows "..." while loading
- [ ] Managers appear in expandable section
- [ ] Expand to see names, titles, emails

**Step 6: Test Expand/Collapse**
- [ ] Click expand button (▶/▼)
- [ ] Should toggle letter and manager sections
- [ ] Both sections visible when expanded
- [ ] Arrow indicator changes direction

---

## API Endpoint Validation

### Endpoint 1: /ai/parse-query (Public)
```bash
curl -X POST http://localhost:5000/ai/parse-query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Python developer with 5+ years, New York, 100k-150k"
  }'

✅ Should return: parsed_params with extracted fields
```

### Endpoint 2: /ai/find-hiring-managers (Public)
```bash
curl -X POST http://localhost:5000/ai/find-hiring-managers \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Google",
    "job_title": "Recruiter"
  }'

✅ Should return: list of managers
```

### Endpoint 3: /ai/generate-cover-letter (Protected)
```bash
# First get a token by logging in
TOKEN=$(curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password"}' \
  | jq -r '.access_token')

# Then generate cover letter
curl -X POST http://localhost:5000/ai/generate-cover-letter \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "job_id": "12345",
    "title": "Senior Developer",
    "company": "Google",
    "resume_text": "Your resume here"
  }'

✅ Should return: generated cover letter
✅ Should be saved in database
```

### Endpoint 4: /ai/create-outreach (Protected)
```bash
curl -X POST http://localhost:5000/ai/create-outreach \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "job_id": "12345",
    "company": "Google",
    "title": "Senior Developer",
    "hiring_manager_name": "John Smith",
    "tone": "professional"
  }'

✅ Should return: outreach workflow with 3 options
```

### Endpoint 5: /ai/send-outreach (Protected)
```bash
curl -X POST http://localhost:5000/ai/send-outreach \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "job_id": "12345",
    "company": "Google",
    "method": "email",
    "recipient_name": "John Smith",
    "recipient_email": "john@example.com"
  }'

✅ Should return: outreach recorded message
✅ Should be in OutreachRecord table
```

### Endpoint 6: /ai/outreach-history (Protected)
```bash
curl -X GET http://localhost:5000/ai/outreach-history \
  -H "Authorization: Bearer $TOKEN"

✅ Should return: list of outreach records for user
✅ Should include stats (by method, by status)
```

### Endpoint 7: /ai/cover-letters (Protected)
```bash
curl -X GET http://localhost:5000/ai/cover-letters \
  -H "Authorization: Bearer $TOKEN"

✅ Should return: all cover letters for user
✅ Should include count
```

---

## Frontend UI Checklist

### Header & Search Bar
- [ ] Title "Job Search Assistant" displays
- [ ] Search input visible with placeholder
- [ ] "Natural Language" checkbox visible
- [ ] Resume file input visible
- [ ] Search button visible and functional

### Natural Language Feature
- [ ] Checkbox toggles naturally
- [ ] Placeholder changes when enabled
- [ ] Parsed parameters display below search form
- [ ] Shows: Location, Job Type, Salary, Skills, Level
- [ ] Colored badges for each parameter

### Job Table
- [ ] Header row displays: Job Name, Company, Location, Summary, Key Requirements, Actions
- [ ] Jobs display in alternating row colors
- [ ] Each job has 4 action buttons: Apply, Letter, Manager, Expand

### Interactive Features
- [ ] Letter button (orange) generates cover letters
- [ ] Manager button (blue) finds hiring managers
- [ ] Apply button (blue) opens job link in new tab
- [ ] Expand button (green) toggles expandable section

### Expandable Section
- [ ] Shows when expand button clicked
- [ ] Two-column layout (Letter | Managers)
- [ ] Cover letter displays with scrollbar if long
- [ ] Manager list shows with names, titles, emails
- [ ] Collapses when expand button clicked again

### Loading States
- [ ] Search button shows "Searching..." when active
- [ ] Letter button shows "..." while generating
- [ ] Manager button shows "..." while loading
- [ ] Load More button works after results
- [ ] No UI freezing during operations

### Error Handling
- [ ] Error messages display in red banner
- [ ] Error disappears on next search
- [ ] User can retry operation
- [ ] Fallback templates work if API fails

---

## Database Verification

### Check New Tables Created
```bash
# Login to PostgreSQL
psql postgresql://user:password@localhost:5432/job_search_db

# List all tables
\dt

# Should show:
# - public | generated_cover_letter
# - public | outreach_record
# (+ existing tables: user, favorite_job, saved_search)
```

### Verify Table Structure
```sql
-- Check GeneratedCoverLetter table
SELECT * FROM generated_cover_letter LIMIT 5;

-- Check OutreachRecord table
SELECT * FROM outreach_record LIMIT 5;

-- Check if any cover letters stored
SELECT COUNT(*) FROM generated_cover_letter;

-- Check outreach records
SELECT COUNT(*) FROM outreach_record;
```

---

## Performance Verification

### Measure NLP Parser Speed
```bash
# Time the parse request
time curl -X POST http://localhost:5000/ai/parse-query \
  -H "Content-Type: application/json" \
  -d '{"query": "Senior Python dev in SF, 150k"}'

# Expected: < 200ms
```

### Measure Cover Letter Generation Speed
```bash
# Should take 3-5 seconds (API bound)
# Time it with:
time curl -X POST http://localhost:5000/ai/generate-cover-letter \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"job_id": "1", "title": "Dev", "company": "Google"}'

# Expected: 3-5 seconds (openai API latency)
```

### Measure Hiring Manager Search Speed
```bash
time curl -X POST http://localhost:5000/ai/find-hiring-managers \
  -H "Content-Type: application/json" \
  -d '{"company_name": "Google"}'

# Expected: < 2 seconds
```

---

## Security Checklist

### API Key Security
- [ ] OPENAI_API_KEY not in git history
- [ ] .env file in .gitignore
- [ ] API key never logged in debug output
- [ ] Rate limiting on sensitive endpoints
- [ ] JWT tokens valid (30-day expiration)

### Authentication
- [ ] Cover letter generation requires JWT token
- [ ] Outreach endpoints require JWT token
- [ ] Unauthorized requests return 401
- [ ] User can only see their own data

### Data Protection
- [ ] Cover letters stored encrypted (consider adding)
- [ ] Outreach records private per user
- [ ] No sensitive data in logs
- [ ] HTTPS enforced in production

---

## Final Verification (Go-Live Checklist)

### Before Deploying to Production
- [ ] All environment variables set
- [ ] Database initialized with new tables
- [ ] All dependencies installed
- [ ] Backend running without errors
- [ ] Frontend connects to backend successfully
- [ ] Natural language search works
- [ ] Cover letter generation works (with OPENAI_API_KEY)
- [ ] Hiring manager search works
- [ ] Outreach recording works
- [ ] All 8 API endpoints respond correctly
- [ ] Authentication working properly
- [ ] Error messages are user-friendly
- [ ] Performance metrics acceptable (< 5s per operation)
- [ ] No console errors in browser
- [ ] No backend errors in Flask logs
- [ ] Database persisting data correctly

---

## Troubleshooting Guide

### Issue: "OpenAI API key invalid"
```bash
# Check if key is set
echo $OPENAI_API_KEY

# If empty, set it again:
export OPENAI_API_KEY=sk-your-key

# Restart Flask
# Try again
```

### Issue: "Module 'openai' not found"
```bash
# Reinstall packages
pip install --upgrade openai

# Or reinstall all
pip install -r requirements.txt
```

### Issue: "Database tables don't exist"
```bash
# Initialize database
curl -X POST http://localhost:5000/db-init

# Verify
psql postgresql://... -c "\dt generated_cover_letter"
```

### Issue: "Frontend can't reach backend"
```bash
# Check backend running
curl http://localhost:5000/health

# Check CORS enabled
# Check proxy setting in package.json

# If still failing, restart both:
# 1. Backend: python app.py
# 2. Frontend: npm start
```

### Issue: "Cover letter generation slow"
```bash
# This is expected (3-5 seconds due to OpenAI API)
# Consider showing loading animation
# Add timeout for long requests
# Recommend in docs to wait patiently
```

### Issue: "Button remains loading forever"
```bash
# Check browser console for errors (F12)
# Check backend logs for 500 errors
# Try refreshing page
# Check API response time: curl with -v flag
```

---

## Production Deployment Notes

### Using Docker
```bash
# Build images
docker-compose build

# Run with env variable
OPENAI_API_KEY=sk-xxx docker-compose up

# Or add to .env file and run
docker-compose up
```

### Using systemd (Linux Server)
```bash
# Create service file
sudo nano /etc/systemd/system/job-search-api.service

[Unit]
Description=Job Search Assistant API
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/job-search
Environment="OPENAI_API_KEY=sk-xxx"
Environment="DATABASE_URL=postgresql://..."
ExecStart=/usr/bin/python3 app.py
Restart=always

[Install]
WantedBy=multi-user.target

# Enable and start
sudo systemctl enable job-search-api
sudo systemctl start job-search-api
```

### Monitoring
```bash
# Monitor logs
tail -f backend/error.log

# Monitor API calls
curl http://localhost:5000/health

# Set up alerts for:
# - 500 errors
# - Slow responses (> 10s)
# - OpenAI API failures
# - Database connection issues
```

---

## Rollback Plan

If issues occur after deployment:

1. **Immediate**: Disable NLP checkbox in frontend (comment out)
2. **Short-term**: Remove OPENAI_API_KEY to fall back to templates
3. **Medium-term**: Revert app.py to previous version
4. **Full rollback**: Restore database backup, redeploy Phase 8 code

---

## Sign-Off Checklist

- [ ] All tests passing
- [ ] No console errors
- [ ] No backend errors
- [ ] Performance acceptable
- [ ] Documentation complete
- [ ] Team trained on new features
- [ ] Backup taken before deployment
- [ ] Monitoring set up
- [ ] Go/No-go decision: **APPROVED FOR DEPLOYMENT**

---

**Status: Phase 9 AI Features Ready for Deployment** ✅

**Next Step: Follow checklist above, then deploy with confidence!**

