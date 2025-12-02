# Backend - Job Search Assistant

Run and test the backend service locally.

Prerequisites
- Python 3.11+ (this project was tested with Python 3.13)
- Install dependencies:

```powershell
cd 'c:\Users\aauradker\Desktop\Job Search Assistant\backend'
C:/Python313/python.exe -m pip install -r requirements.txt
```

Set your RapidAPI key (session only):

```powershell
$env:RAPIDAPI_KEY = 'your_rapidapi_key_here'
```

Run the Flask app:

```powershell
C:/Python313/python.exe app.py
```

Endpoint
- POST `/search_jobs` — accepts JSON `{ "query": "..." }` or form data `query`.

Testing
- Unit tests are in `backend/test_job_search.py`. Run using the provided test runner or:

```powershell
# from project root
C:/Python313/python.exe -m pytest backend/test_job_search.py
```
