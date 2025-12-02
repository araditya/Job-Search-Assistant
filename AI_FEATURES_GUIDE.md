# Job Search Assistant - Phase 9: AI Features Implementation Guide

## Overview

Phase 9 adds intelligent AI-powered features to the Job Search Assistant:

1. **Natural Language Query Parsing** - Converts conversational search queries into structured job search parameters
2. **AI-Generated Cover Letters** - Creates customized cover letters using OpenAI GPT-3.5-turbo
3. **LinkedIn Hiring Manager Discovery & Outreach** - Finds hiring managers and provides outreach workflow options

## Architecture

### Backend Components

#### 1. NLP Parser (`backend/nlp_parser.py`)
Extracts structured job search parameters from natural language queries.

**Key Functions:**
- `parse_natural_language_query(query)` - Main function
  - Input: "Senior Python developer in San Francisco, remote, 150k-200k salary, 5+ years experience"
  - Output: Dict with location, job_type, salary_range, required_skills, seniority, experience_years, core search query

**Supported Extractions:**
- **Location**: "New York", "San Francisco", "Remote", "NYC", etc.
- **Job Type**: Full-time, part-time, contract, remote, hybrid
- **Salary Range**: "$100k-150k", "120k", etc.
- **Skills**: Python, Java, AWS, SQL, React, etc.
- **Seniority**: Entry-level, mid-level, senior, executive
- **Experience**: "5+ years", "3-5 years", etc.

#### 2. Cover Letter Generator (`backend/cover_letter_generator.py`)
Generates customized cover letters using OpenAI GPT-3.5-turbo with fallback templates.

**Key Functions:**
- `generate_cover_letter(job, resume_text, user_name)` - Creates customized letter
  - Uses OpenAI API if OPENAI_API_KEY is set
  - Falls back to template if API unavailable
  - Returns 200-300 word professional cover letter
  
- `generate_outreach_message(job, hiring_manager, company, tone)` - Creates outreach message
  - Tones: 'professional', 'friendly', 'casual'
  - Perfect for LinkedIn DMs or emails

- `generate_email_outreach(subject, hiring_manager, company, user_email, message)` - Full email template

#### 3. LinkedIn Manager (`backend/linkedin_manager.py`)
Manages hiring manager discovery and outreach workflows.

**Key Class: LinkedInManager**
- `find_hiring_managers(company_name, job_title)` - Finds potential hiring managers
  - Uses ProxyCurl API (optional) for accuracy
  - Falls back to templated suggestions
  - Returns list with name, title, email, LinkedIn profile

- `create_outreach_workflow(job, hiring_manager, user_email)` - Generates outreach options
  - LinkedIn message option
  - Email outreach option
  - Job portal message option

- `send_linkedin_message()` - Sends LinkedIn DM (requires LINKEDIN_ACCESS_TOKEN)

#### 4. Database Models Update (`backend/models.py`)
Added two new tables for persistence:

**GeneratedCoverLetter Table:**
```python
{
  'id': int,
  'user_id': int,
  'job_id': str,
  'job_title': str,
  'company': str,
  'cover_letter_text': str,
  'customization_level': str,  # 'minimal', 'standard', 'tailored'
  'created_at': datetime,
  'updated_at': datetime
}
```

**OutreachRecord Table:**
```python
{
  'id': int,
  'user_id': int,
  'job_id': str,
  'company': str,
  'outreach_method': str,  # 'linkedin', 'email', 'portal'
  'recipient_name': str,
  'recipient_email': str,
  'message_sent': str,
  'status': str,  # 'pending', 'sent', 'interested', 'rejected'
  'response': str,
  'created_at': datetime,
  'updated_at': datetime
}
```

### API Endpoints (New)

All AI endpoints are under `/ai` prefix and require Flask backend running.

#### POST `/ai/parse-query`
Parse natural language search query.

**Request:**
```json
{
  "query": "Senior Python developer in San Francisco, remote, 150k-200k, 5+ years"
}
```

**Response:**
```json
{
  "query": "Senior Python developer in San Francisco...",
  "parsed_params": {
    "search_query": "Senior Python developer",
    "location": "San Francisco",
    "job_type": "remote",
    "salary_range": {"min": 150000, "max": 200000},
    "required_skills": ["python"],
    "seniority": "senior",
    "experience_years": {"min": 5, "max": 15}
  }
}
```

#### POST `/ai/generate-cover-letter` (Requires Auth)
Generate customized cover letter for a job.

**Request:**
```json
{
  "job_id": "12345",
  "title": "Senior Python Developer",
  "company": "Google",
  "summary": "We are looking for...",
  "requirements": ["Python", "AWS", "Docker"],
  "resume_text": "Optional resume content",
  "user_name": "John Doe"
}
```

**Response:**
```json
{
  "message": "Cover letter generated successfully",
  "cover_letter": {
    "id": 1,
    "user_id": 1,
    "job_id": "12345",
    "company": "Google",
    "cover_letter_text": "Dear Hiring Manager...",
    "customization_level": "standard",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00"
  }
}
```

#### POST `/ai/find-hiring-managers`
Find potential hiring managers at a company.

**Request:**
```json
{
  "company_name": "Google",
  "job_title": "Recruiter"
}
```

**Response:**
```json
{
  "company": "Google",
  "hiring_managers": [
    {
      "name": "Sarah Johnson",
      "title": "Senior Recruiter",
      "email": "sarah.j@google.com",
      "profile_url": "https://linkedin.com/in/sarah-johnson"
    }
  ],
  "count": 1,
  "note": "Manual verification recommended for email addresses"
}
```

#### POST `/ai/create-outreach` (Requires Auth)
Create outreach workflow with multiple contact options.

**Request:**
```json
{
  "job_id": "12345",
  "company": "Google",
  "title": "Senior Python Developer",
  "hiring_manager_name": "Sarah Johnson",
  "hiring_manager_title": "Senior Recruiter",
  "hiring_manager_email": "sarah.j@google.com",
  "tone": "professional"
}
```

**Response:**
```json
{
  "message": "Outreach workflow created",
  "workflow": {
    "linkedin_message": "Hi Sarah, I'm interested in the Senior Python Developer role at Google...",
    "email": {
      "subject": "Interested in Senior Python Developer Role at Google",
      "body": "Dear Sarah..."
    },
    "job_portal_message": "Applying through the job portal for Senior Python Developer..."
  },
  "user_email": "user@example.com"
}
```

#### POST `/ai/send-outreach` (Requires Auth)
Record outreach message in the system.

**Request:**
```json
{
  "job_id": "12345",
  "company": "Google",
  "method": "email",
  "recipient_name": "Sarah Johnson",
  "recipient_email": "sarah.j@google.com",
  "message": "Email message sent"
}
```

**Response:**
```json
{
  "message": "Outreach recorded via email",
  "outreach_id": 1,
  "status": "pending",
  "next_steps": [
    "Copy the message from above",
    "Send from your email client",
    "Update status when you receive a response"
  ]
}
```

#### GET `/ai/outreach-history` (Requires Auth)
Get user's complete outreach history.

**Response:**
```json
{
  "outreach_records": [...],
  "stats": {
    "total_outreach": 5,
    "by_method": {"email": 3, "linkedin": 2},
    "by_status": {"pending": 2, "sent": 3}
  },
  "count": 5
}
```

#### GET `/ai/cover-letters` (Requires Auth)
Get all generated cover letters for the user.

**Response:**
```json
{
  "cover_letters": [...],
  "count": 5
}
```

#### DELETE `/ai/cover-letters/<letter_id>` (Requires Auth)
Delete a specific cover letter.

### Frontend Components

#### Updated `App.js`
- Natural Language Checkbox - Toggle between regular and NLP search
- Natural Language Placeholder - Shows example queries
- Parsed Parameters Display - Shows extracted location, salary, skills, etc.
- Extended Job submission with NLP parsing

**Example Usage:**
```javascript
const [useNLP, setUseNLP] = useState(false);
const [parsedParams, setParsedParams] = useState(null);

// When useNLP is true:
const parseRes = await axios.post('/ai/parse-query', { query });
setParsedParams(parseRes.data.parsed_params);
```

#### Updated `JobTable.js`
New interactive features per job:

1. **Letter Button** - Generates customized cover letter
   - Displays in expandable row
   - Automatically saves to database
   - Shows customization level (minimal/standard/tailored)

2. **Manager Button** - Finds hiring managers
   - Displays names, titles, emails in expandable row
   - Shows LinkedIn profile links

3. **Apply Link** - Original job application link (unchanged)

4. **Expand/Collapse Button** - Shows/hides cover letter and manager sections

**Key Features:**
- Button states during loading
- Error handling and user feedback
- Caching of generated data locally
- Requires authentication for sensitive operations

## Setup & Configuration

### Environment Variables Required

```bash
# OpenAI API Key (required for cover letter generation)
OPENAI_API_KEY=sk-...

# Optional: LinkedIn Access Token
LINKEDIN_ACCESS_TOKEN=...

# Optional: ProxyCurl API Key for hiring manager discovery
PROXYCURL_API_KEY=...

# Existing variables
DATABASE_URL=postgresql://user:password@localhost:5432/job_search_db
JWT_SECRET_KEY=your-secret-key
```

### Installation

1. **Install dependencies:**
```bash
pip install -r backend/requirements.txt
```

New packages added:
- `openai` - OpenAI API client
- `spacy` - NLP library (optional, regex-based parsing used by default)
- `nltk` - Natural language toolkit (optional)
- `linkedin-api` - LinkedIn API client

2. **Update database with new tables:**
```bash
curl -X POST http://localhost:5000/db-init
```

3. **Set environment variables:**
```bash
# Linux/Mac
export OPENAI_API_KEY=sk-...
export DATABASE_URL=postgresql://...

# Windows PowerShell
$env:OPENAI_API_KEY="sk-..."
$env:DATABASE_URL="postgresql://..."
```

4. **Restart backend:**
```bash
python backend/app.py
# Or use Docker
docker-compose up
```

## Usage Examples

### 1. Natural Language Search

**User Input:**
"I'm looking for a senior Python developer role in San Francisco with remote work option, expecting around 150k-200k salary"

**System Flow:**
1. Frontend sends query to `/ai/parse-query`
2. Backend extracts: location=SF, job_type=remote, salary=$150k-200k, seniority=senior, skills=[python]
3. Display parsed params to user for review
4. Use core query "senior Python developer" in job search
5. Filter results by location, salary, etc.

### 2. Generate Cover Letter

**User Clicks "Letter" Button on a Job**
1. Frontend sends POST to `/ai/generate-cover-letter` with job details
2. Backend calls OpenAI GPT-3.5-turbo to generate customized letter
3. Cover letter saved in database with customization_level='standard'
4. Displayed in expandable job row with word count ~250 words

### 3. Find Hiring Managers & Send Outreach

**User Clicks "Manager" Button on a Job**
1. Frontend sends POST to `/ai/find-hiring-managers` with company name
2. Backend searches for recruiters/HR managers at that company
3. Returns list with name, title, email, LinkedIn profile

**User Chooses Outreach Method:**
1. System generates customized message (LinkedIn/email)
2. Displays message preview for user review
3. User clicks "Send" (for email) or copies message (for LinkedIn)
4. Outreach recorded in `OutreachRecord` table with status='pending'

## Testing

### Manual Testing Steps

1. **Test NLP Parser:**
```bash
curl -X POST http://localhost:5000/ai/parse-query \
  -H "Content-Type: application/json" \
  -d '{"query": "Python developer in NYC, remote, 150k"}'
```

2. **Test Cover Letter Generation (requires auth):**
```bash
# First, get JWT token from /auth/login
curl -X POST http://localhost:5000/ai/generate-cover-letter \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "job_id": "12345",
    "title": "Senior Developer",
    "company": "Google",
    "resume_text": "Your resume content"
  }'
```

3. **Test Hiring Manager Discovery:**
```bash
curl -X POST http://localhost:5000/ai/find-hiring-managers \
  -H "Content-Type: application/json" \
  -d '{"company_name": "Google", "job_title": "Recruiter"}'
```

### Frontend Testing

1. Click "Natural Language" checkbox
2. Enter: "Senior Python developer in San Francisco, remote, 150k salary"
3. Verify parsed parameters display correctly
4. Click "Search"
5. Verify jobs appear in table
6. Click "Letter" button on a job → cover letter generates
7. Click "Manager" button on a job → hiring managers display
8. Click expand button to see both letter and managers

## Troubleshooting

### Cover Letter Generation Fails

**Error:** "Request failed 401" or "OpenAI API key invalid"

**Solution:**
1. Check `OPENAI_API_KEY` environment variable is set correctly
2. Verify key is valid in OpenAI dashboard
3. Check quota/billing in OpenAI account
4. System falls back to template if API unavailable

### Hiring Managers Not Found

**Issue:** Getting generic template suggestions instead of real managers

**Solution:**
1. Enable ProxyCurl API for accurate discovery (optional)
2. Set `PROXYCURL_API_KEY` environment variable
3. Verify company name is accurate and publicly listed
4. Try searching for the company on LinkedIn directly

### Authentication Errors

**Error:** "401 Unauthorized" on cover letter or outreach endpoints

**Solution:**
1. Ensure user is logged in (JWT token in localStorage)
2. Token may have expired (30-day expiration)
3. Login again to get new token
4. Check JWT_SECRET_KEY in backend matches frontend

## Performance & Limitations

### Rate Limiting
- OpenAI API: Rate limited per your account tier (typically 3-5 requests/min for free tier)
- LinkedIn API: Limited by API key quotas
- ProxyCurl API: Limited by subscription level

### Optimization Tips
1. **Cache cover letters** - Same job doesn't need regeneration
2. **Batch hiring manager searches** - Search once per company
3. **Store parsed queries** - Reuse NLP results within session

## Future Enhancements

1. **LinkedIn OAuth** - Enable actual LinkedIn API integration with user accounts
2. **Advanced NLP** - Use spaCy/NLTK for more sophisticated parsing
3. **Multi-language Support** - Support queries in different languages
4. **Interview Prep** - Generate interview questions based on job
5. **Salary Negotiation** - Research salary benchmarks
6. **Application Tracking** - Track status across all applications
7. **Cover Letter Templates** - Save and reuse user's own templates
8. **LinkedIn DM Automation** - Send messages directly to hiring managers

## Support & Debugging

### Enable Debug Mode
```bash
# Frontend console
localStorage.setItem('debug', 'true');

# Backend logging
export FLASK_ENV=development
python -m flask --app app run
```

### Common Queries for NLP Testing
- "Python developer in New York"
- "Senior Java developer, remote, $200k"
- "Data scientist role, 3-5 years experience"
- "Entry level React developer, San Francisco, hybrid"
- "Machine learning engineer, AWS, Kubernetes, $150-200k"

### API Response Times
- NLP parsing: ~100ms
- Cover letter generation: ~3-5 seconds (OpenAI API)
- Hiring manager search: ~500ms-2s (ProxyCurl API)
- Database queries: ~50ms

