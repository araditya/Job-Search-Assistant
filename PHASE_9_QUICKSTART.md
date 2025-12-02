# Phase 9: AI Features - Quick Start Guide

## What's New?

✨ **Natural Language Search** - Ask for jobs naturally: "Senior Python dev in NYC, remote, 150k"
🤖 **AI Cover Letters** - Generate customized cover letters instantly
👤 **Hiring Manager Outreach** - Find and contact hiring managers with suggested messages

## 5-Minute Setup

### 1. Get OpenAI API Key
- Go to https://platform.openai.com/account/api-keys
- Create new secret key
- Keep it secret! Don't commit to git

### 2. Set Environment Variable
```bash
# macOS/Linux (add to ~/.zshrc or ~/.bashrc)
export OPENAI_API_KEY=sk-your-key-here

# Windows PowerShell
$env:OPENAI_API_KEY="sk-your-key-here"

# Or add to .env file in backend directory
OPENAI_API_KEY=sk-your-key-here
```

### 3. Restart Backend
```bash
# Stop current Flask process (Ctrl+C)
cd backend
pip install -r requirements.txt  # Install new dependencies
python app.py
```

### 4. Test It
1. Open http://localhost:3000
2. Check the "Natural Language" checkbox
3. Try: "Senior Python developer in San Francisco, remote, $150k"
4. Click Search
5. See parsed parameters display
6. Expand a job, click "Letter" → Cover letter generated!

## Feature Breakdown

### Natural Language Search
Instead of: "python developer"
Try: "Senior Python developer in SF, remote, 150k-200k, 5+ years"

**Extracted:**
- 📍 Location: San Francisco
- 🏢 Type: Remote
- 💰 Salary: $150k-200k
- 📊 Level: Senior
- ⏱️ Experience: 5+ years
- 🛠️ Skills: Python

### Cover Letter Generation
**Click "Letter" button on any job**
- System calls OpenAI GPT-3.5-turbo
- Generates ~250 word professional cover letter
- Customized to job description
- Saved in database
- You can copy/paste directly

**Example Cover Letter (auto-generated):**
```
Dear Hiring Manager,

I am writing to express my strong interest in the Senior Python Developer 
position at Google. With 6+ years of hands-on experience developing scalable 
Python applications and a proven track record of leading cross-functional teams, 
I am confident in my ability to contribute significantly to your engineering team.

Throughout my career, I have specialized in building robust backend systems 
using Python, AWS, and Docker. My expertise aligns perfectly with your 
requirements...

Sincerely,
[Your Name]
```

### Hiring Manager Discovery & Outreach
**Click "Manager" button on any job**
- System finds recruiters at that company
- Shows name, title, email
- Three outreach options:
  1. **LinkedIn Message** - Copy/paste to LinkedIn
  2. **Email** - Complete email template ready to send
  3. **Job Portal** - Message through application portal

**Example Workflow:**
1. Find job → Click "Manager"
2. See list: "Sarah Johnson - Senior Recruiter at Google"
3. Choose "Email" option
4. System generates personalized email
5. You copy & send from your email
6. System logs outreach attempt (pending → sent → response)

## Usage Patterns

### Pattern 1: Exploratory Search
1. Enable Natural Language
2. Enter conversational query: "What jobs match my profile? Java developer, NYC area, 100k+"
3. System extracts: Java, Location: NYC, Salary: 100k+
4. See filtered results
5. Perfect for discovery!

### Pattern 2: Generate & Apply
1. Search for relevant jobs
2. Find interesting job in results
3. Click "Letter" button → Copy cover letter
4. Click "Apply" → Apply on job site with generated letter
5. Click "Manager" → Note who you're reaching out to
6. Send personalized email/LinkedIn message

### Pattern 3: Track Outreach
1. For each application, record outreach:
   - Click "Manager" → choose method
   - System logs: Email to Sarah Johnson at Google
2. Later, check your outreach history
   - Go to API: GET /ai/outreach-history
   - See: 5 emails sent, 2 LinkedIn messages, 1 response

## Common Queries to Try

```
"Python developer"  
→ Location: None, Job type: None, Skills: [python]

"Senior React developer in San Francisco, remote, $200k"  
→ Location: SF, Job type: remote, Salary: $200k, Seniority: senior

"Entry-level data scientist, NYC, 80k-100k, Python and SQL"  
→ Seniority: entry-level, Location: NYC, Salary: $80k-100k, Skills: [python, sql]

"Full-time Java backend engineer, AWS experience, 5+ years, $150-200k"  
→ Type: full-time, Skills: [java, aws], Experience: 5+ years, Salary: $150k-200k

"Hybrid work, machine learning, NYC, senior role"  
→ Job type: hybrid, Location: NYC, Skills: [ml], Seniority: senior
```

## Troubleshooting

### "Cover letter generation failed"
- ✅ Check OPENAI_API_KEY is set correctly
- ✅ Verify key has remaining credits in OpenAI dashboard
- ✅ Try again (may be temporary API issue)
- ✅ Falls back to template if API down

### "No hiring managers found"
- ✅ Company name may be spelled differently
- ✅ Company may be very small/private
- ✅ System shows template suggestions as fallback
- ✅ Consider researching on LinkedIn manually

### "Authorization error on cover letter"
- ✅ Make sure you're logged in (check token in browser storage)
- ✅ If logged in, token may have expired
- ✅ Log out and log back in
- ✅ Create new JWT token

### "Button is grayed out / not responding"
- ✅ Wait for current operation to complete
- ✅ Refresh page if stuck
- ✅ Check browser console for errors (F12)
- ✅ Try restarting backend

## API Examples (Advanced)

### Parse Query Only
```bash
curl -X POST http://localhost:5000/ai/parse-query \
  -H "Content-Type: application/json" \
  -d '{"query": "Senior Python dev in SF, 150k-200k"}'
```

### Get Your Outreach History
```bash
curl -X GET http://localhost:5000/ai/outreach-history \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Generate Cover Letter (with auth)
```bash
curl -X POST http://localhost:5000/ai/generate-cover-letter \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "job_id": "12345",
    "title": "Senior Python Developer",
    "company": "Google",
    "resume_text": "your resume content"
  }'
```

## Next Steps

1. ✅ Set OPENAI_API_KEY
2. ✅ Restart backend with `pip install -r requirements.txt`
3. ✅ Test natural language search in UI
4. ✅ Generate a cover letter
5. ✅ Find hiring managers and send outreach
6. ✅ Track your applications

## Getting Help

- **Backend errors?** Check `backend/error.log`
- **Frontend not working?** Check browser console (F12)
- **API key issues?** Verify in OpenAI dashboard
- **Database errors?** Run `/db-init` endpoint to initialize tables

## Pro Tips

💡 **Reuse templates** - System caches cover letters, no need to regenerate for similar roles

💡 **Batch outreach** - Find all managers at a company, then reach out with slightly different angles

💡 **Track responses** - Update outreach status when you hear back (API supports response tracking)

💡 **Natural language > keywords** - More conversational queries work better

💡 **Include specifics** - Location + salary + skills get better extracted results

## Performance Notes

⚡ **NLP Parsing:** ~100ms  
⚡ **Cover Letter Generation:** ~3-5 seconds (waits for OpenAI API)  
⚡ **Hiring Manager Search:** ~500ms-2 seconds  

Consider running these operations in background or showing loading indicators.

