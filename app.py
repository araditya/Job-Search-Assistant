from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import logging
import traceback
import typing
import os
from datetime import timedelta

# Database and auth imports
from models import db
from auth import auth_bp
from favorites import favorites_bp
from ai_features import ai_features_bp
from nlp_parser import parse_natural_language_query

# Make imports robust so `app.py` can be executed from different CWDs
try:
    from backend.job_search import search_jobs
except Exception:
    from job_search import search_jobs

try:
    from backend.ai_match import match_resume_to_job
except Exception:
    from ai_match import match_resume_to_job

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'postgresql://user:password@localhost:5432/job_search_db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)

db.init_app(app)
jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(favorites_bp)
app.register_blueprint(ai_features_bp)

# Configure logging to file for unhandled exceptions
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler('error.log'),
        logging.StreamHandler()
    ]
)


@app.route('/search_jobs', methods=['POST'])
def search_jobs_endpoint():
    """Search jobs and optionally match to an uploaded resume.

    Accepts page and num_pages parameters for pagination.
    """
    # Accept JSON or form data
    query = None
    if request.is_json:
        payload = request.get_json(silent=True) or {}
        query = payload.get('query')
        page = payload.get('page', 1)
        num_pages = payload.get('num_pages', 1)
    else:
        query = request.form.get('query') or request.values.get('query')
        page = int(request.form.get('page', 1))
        num_pages = int(request.form.get('num_pages', 1))

    if not query:
        return jsonify({"error": "Missing required parameter: query"}), 400

    logging.info(f"Received search query (natural language): {query}, page: {page}, num_pages: {num_pages}")

    # Parse natural language query into structured parameters and a core search query
    try:
        parsed = parse_natural_language_query(query)
        core_query = parsed.get('search_query') or query
        logging.info(f"Parsed params: {parsed}")
    except Exception as e:
        logging.error(f"NLP parsing failed: {e}")
        parsed = None
        core_query = query

    resume_file = request.files.get('resume')
    resume_text: typing.Optional[str] = None
    if resume_file:
        try:
            raw = resume_file.read()
            resume_text = raw.decode('utf-8', errors='ignore')
        except Exception:
            resume_text = None

    # Use the core_query for the actual job search
    jobs = search_jobs(core_query, page=page, num_pages=num_pages)
    results = []
    for job in jobs:
        if resume_text:
            try:
                match_score, cover_letter = match_resume_to_job(resume_text, job)
            except Exception:
                match_score, cover_letter = "N/A", "N/A"
        else:
            match_score, cover_letter = "N/A", "N/A"

        requirements = job.get('requirements', [])
        nice_to_have = job.get('nice_to_have', [])

        results.append({
            "Job Name": job.get('title', 'N/A'),
            "Job ID": job.get('id', 'N/A'),
            "Company": job.get('company', 'N/A'),
            "Summary": job.get('summary', ''),
            "Key Requirements": ", ".join(requirements) if isinstance(requirements, list) else str(requirements),
            "Good to Have": ", ".join(nice_to_have) if isinstance(nice_to_have, list) else str(nice_to_have),
            "Location": job.get('location', ''),
            "Link": job.get('url', ''),
            "AI Job Match": match_score,
            "Cover Letter Summary": cover_letter,
        })

    response = {
        'jobs': results,
        'page': page,
        'num_pages': num_pages,
        'total': len(results)
    }

    # Attach parsed parameters to the response so frontend can display filters
    if parsed:
        response['parsed_params'] = parsed

    return jsonify(response)


@app.route('/health', methods=['GET'])
def health_check():
    """Simple health-check endpoint for automated checks."""
    return jsonify({"status": "ok"}), 200


@app.route('/db-init', methods=['POST'])
def init_db():
    """Initialize database tables (development only)."""
    try:
        with app.app_context():
            db.create_all()
        return jsonify({"message": "Database initialized"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)


@app.errorhandler(Exception)
def handle_unexpected_error(e):
    """Catch-all error handler: log exception and return JSON during debug."""
    tb = traceback.format_exc()
    logging.error('Unhandled exception: %s\n%s', e, tb)
    if app.debug:
        return jsonify({'error': str(e), 'trace': tb}), 500
    return jsonify({'error': 'Internal server error'}), 500
