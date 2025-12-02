
import os
import re
import logging
import requests
from typing import List, Dict, Any

# Optional dotenv support for local development. If python-dotenv is not
# installed the import will be ignored and environment variables are used
# as usual.
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    # dotenv not installed or .env not present — continue using os.environ
    pass


RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY") or os.environ.get("YOUR_RAPIDAPI_KEY") or ""


# Lightweight skill keyword set to extract common requirements.
COMMON_SKILLS = {
    'python', 'sql', 'aws', 'excel', 'powerbi', 'power bi', 'postgres', 'postgresql',
    'pandas', 'numpy', 'tableau', 'spark', 'hadoop', 'gcp', 'azure', 'docker',
    'kubernetes', 'react', 'node', 'java', 'c#', 'c++', 'git', 'linux', 'html', 'css',
    'javascript', 'r', 'sas', 'mongodb', 'redis', 'jira', 'salesforce', 'pytest'
}


def extract_requirement_keywords(qualifications, description):
    """Return a short list of keywords extracted from qualifications or description."""
    keywords = []
    # Start with explicit qualifications list
    for q in qualifications or []:
        for token in re.split(r"[\,;\n\r\/()]+", str(q)):
            t = token.strip()
            if not t:
                continue
            # simple normalization
            lk = t.lower()
            if any(skill in lk for skill in COMMON_SKILLS):
                keywords.append(t.strip())

    # Fallback: scan description for common skills
    if not keywords and description:
        for skill in COMMON_SKILLS:
            if skill in description.lower():
                keywords.append(skill)

    # Deduplicate and return top 8
    seen = []
    for k in keywords:
        if k not in seen:
            seen.append(k)
    return seen[:8]


def normalize_query(q: str) -> str:
    """Clean up a natural-language query to improve API results.

    - collapse repeated punctuation (commas),
    - strip obvious salary tokens (e.g. 150k, $150k, 150,000),
    - normalize whitespace.
    """
    if not q:
        return q
    s = q
    # remove common salary patterns like 150k-200k or $150,000
    s = re.sub(r"\$?\d{2,3}[,\d]*k?(-\$?\d{2,3}[,\d]*k?)?", "", s, flags=re.IGNORECASE)
    # collapse multiple commas/spaces
    s = re.sub(r",+", ",", s)
    s = re.sub(r"\s+", " ", s).strip()
    # remove leading/trailing commas and extra separators
    s = re.sub(r"^[,\s]+|[,\s]+$", "", s)
    # remove repeated punctuation like ', ,'
    s = s.replace(', ,', ',')
    return s


def search_jobs(query: str, page: int = 1, num_pages: int = 1) -> List[Dict[str, Any]]:
    """Search jobs using the jsearch RapidAPI endpoint.

    Supports requesting multiple pages by setting `num_pages` and will return
    combined results. If `num_pages == 1` and `page` is provided, it will return
    that single page which the frontend can use for "load more" behavior.
    """
    logger = logging.getLogger(__name__)
    if not RAPIDAPI_KEY:
        logger.warning("RAPIDAPI_KEY environment variable not set. Returning empty results.")
        return []

    url = "https://jsearch.p.rapidapi.com/search"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com",
    }

    results: List[Dict[str, Any]] = []

    # Normalize the incoming query to avoid noisy tokens (salary ranges, extra commas)
    query_clean = normalize_query(query)
    logger.info("Searching jobs with query=%s (cleaned: %s), page=%s, num_pages=%s", query, query_clean, page, num_pages)

    for p in range(page, page + int(num_pages)):
        params = {
            "query": query_clean,
            "page": str(p),
            "num_pages": "1",
        }

        try:
            logger.info("Outgoing API request to %s params=%s headers_keys=%s", url, params, list(headers.keys()))
            resp = requests.get(url, headers=headers, params=params, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            logger.info("API response status=%s data_items=%s", resp.status_code, len(data.get("data", [])))
        except Exception as exc:
            logger.exception("Error fetching jobs from API (page %s): %s", p, exc)
            # On API error, stop fetching more pages but return what we have
            break

        for job in data.get("data", []):
            highlights = job.get("job_highlights") or {}
            qualifications = highlights.get("Qualifications") if isinstance(highlights, dict) else highlights.get("Qualifications") or []
            responsibilities = highlights.get("Responsibilities") if isinstance(highlights, dict) else highlights.get("Responsibilities") or []

            # Map additional fields (best effort)
            salary = job.get('job_salary') or job.get('salary') or job.get('job_min_salary') or job.get('job_max_salary')
            posted = job.get('job_posted_at') or job.get('job_posted_at_datetime_utc') or job.get('date')
            employment_type = job.get('job_employment_type') or job.get('employment_type')

            description = job.get("job_description") or job.get("description") or ""

            reqs = qualifications if isinstance(qualifications, list) else ([qualifications] if qualifications else [])
            nice = responsibilities if isinstance(responsibilities, list) else ([responsibilities] if responsibilities else [])

            keywords = extract_requirement_keywords(reqs, description)

            results.append({
                "title": job.get("job_title") or job.get("title") or "N/A",
                "id": job.get("job_id") or job.get("job_publisher") or "N/A",
                "company": job.get("employer_name") or job.get("company_name") or "N/A",
                "summary": (description or "")[:500],
                "location": job.get("job_city") or ("Remote" if job.get("remote", False) else ""),
                "url": job.get("job_apply_link") or job.get("url") or "",
                "requirements": reqs,
                "nice_to_have": nice,
                "requirements_keywords": keywords,
                "salary": salary,
                "posted": posted,
                "employment_type": employment_type,
            })

    return results
