# Job-Search-Assistant
# Job Search App (monorepo)

This repository contains a Flask backend and a React frontend for a simple job search assistant.

Project layout
- `backend/` — Flask API, job search logic, tests
- `job-search-app/frontend/` — React frontend (CRA-style scaffold)

Prerequisites
- Python 3.11+ and pip
- Node.js (16+) and npm

Backend (run)
1. Open a PowerShell terminal and go to the backend folder:

```powershell
cd 'c:\Users\aauradker\Desktop\Job Search Assistant\backend'
```

2. (Optional) Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\activate
```

3. Install Python dependencies:

```powershell
pip install -r requirements.txt
```

4. Provide your RapidAPI key. For a one-off session run in PowerShell:

```powershell
$env:RAPIDAPI_KEY = 'your_real_rapidapi_key_here'
```

Alternatively, create a `.env` file inside `backend/` with:

```
RAPIDAPI_KEY=your_real_rapidapi_key_here
```

5. Start the backend server:

```powershell
python app.py
```

The backend listens on http://127.0.0.1:5000

Frontend (run)
1. Open a second terminal and change to the frontend folder:

```powershell
cd 'c:\Users\aauradker\Desktop\Job Search Assistant\job-search-app\frontend'
```

2. Install npm dependencies and start the dev server:

```powershell
npm install
npm start
```

The frontend dev server runs on http://localhost:3000 and is configured to proxy API requests to the backend (`proxy` is set to `http://localhost:5000` in `package.json`).

Quick test
- Open http://localhost:3000 in your browser.
- Enter a search query and optionally upload a resume (.txt or .pdf), then click Search.

Running backend tests
1. From the `backend` folder run:

```powershell
# If using venv, activate it first
python -m unittest test_job_search.py -v
```

Notes & troubleshooting
- If the frontend fails to proxy, ensure the backend is running and `proxy` is correctly set in `job-search-app/frontend/package.json`.
- If you get API errors, verify `RAPIDAPI_KEY` is set and valid. You can also inspect logs printed by the backend for request/response details.
- To re-initialize a full CRA project instead of using the scaffold here, run `npx create-react-app .` inside `job-search-app/frontend` and replace `src/App.js` and add `src/JobTable.js` from this repo.

Next steps you might want me to do
- Add CSS styling for the frontend table
- Add more endpoint tests using Flask's test client
- Add a GitHub Actions workflow to run the unit tests automatically
