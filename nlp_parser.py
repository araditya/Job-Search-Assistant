"""
Natural Language Processing module for parsing job search queries.
Extracts location, job type, salary, skills, and other requirements from user input.
"""

import re
from typing import Dict, Any, List

# Common job types
JOB_TYPES = {
    'full-time', 'fulltime', 'ft', 'full time',
    'part-time', 'parttime', 'pt', 'part time',
    'contract', 'temporary', 'temp', 'freelance', 'remote', 'on-site', 'onsite', 'hybrid'
}

# Common US locations
US_LOCATIONS = {
    'new york', 'ny', 'los angeles', 'la', 'california', 'ca', 'texas', 'tx', 'chicago', 'il',
    'florida', 'fl', 'washington', 'wa', 'denver', 'co', 'boston', 'ma', 'seattle', 'wa',
    'san francisco', 'sf', 'bay area', 'austin', 'atlanta', 'ga', 'miami', 'dallas', 'tx',
    'atlanta', 'phoenix', 'az', 'philadelphia', 'pa', 'houston', 'tx', 'portland', 'or',
    'remote', 'anywhere', 'us', 'united states'
}

# Common salary indicators
SALARY_INDICATORS = ['salary', 'pay', 'compensation', 'pays', 'wage', 'hourly', '$']

# Common skill keywords
COMMON_SKILLS = {
    'python', 'javascript', 'java', 'c#', 'c++', 'react', 'node', 'angular', 'vue',
    'sql', 'mongodb', 'postgresql', 'aws', 'azure', 'gcp', 'docker', 'kubernetes',
    'machine learning', 'ai', 'data science', 'analytics', 'blockchain', 'web3',
    'django', 'fastapi', 'flask', 'spring', 'golang', 'rust', 'typescript'
}


def extract_location(query: str) -> str:
    """Extract location from query."""
    query_lower = query.lower()
    
    # Look for "in" or "at" followed by location
    location_patterns = [
        r'in\s+(\w+(?:\s+\w+)?)',  # "in New York"
        r'at\s+(\w+(?:\s+\w+)?)',  # "at Austin"
        r'based in\s+(\w+(?:\s+\w+)?)',  # "based in San Francisco"
        r'location:\s*(\w+(?:\s+\w+)?)',  # "location: New York"
    ]
    
    for pattern in location_patterns:
        match = re.search(pattern, query_lower)
        if match:
            location = match.group(1).strip()
            if location in US_LOCATIONS or len(location.split()) <= 2:
                return location
    
    # Check if query contains any known location
    for loc in US_LOCATIONS:
        if loc in query_lower:
            return loc
    
    return 'Remote'  # Default to remote


def extract_job_type(query: str) -> str:
    """Extract job type (full-time, part-time, contract, etc) from query."""
    query_lower = query.lower()
    
    for job_type in JOB_TYPES:
        if job_type in query_lower:
            return job_type
    
    return 'full-time'  # Default


def extract_salary_range(query: str) -> Dict[str, int]:
    """Extract salary range from query."""
    query_lower = query.lower()
    
    # Look for patterns like "$100k-$150k" or "100k to 150k"
    salary_patterns = [
        r'\$(\d+k?)\s*-\s*\$?(\d+k?)',  # "$100k-150k"
        r'(\d+)\s*(?:to|-)?\s*(\d+)\s*(?:k|thousand)',  # "100 to 150k"
        r'(?:salary|pay|compensation).*?(\d+k?)\s*-\s*(\d+k?)',  # "salary 100k-150k"
    ]
    
    for pattern in salary_patterns:
        match = re.search(pattern, query_lower)
        if match:
            min_sal = match.group(1).replace('k', '000')
            max_sal = match.group(2).replace('k', '000')
            try:
                return {
                    'min': int(min_sal),
                    'max': int(max_sal)
                }
            except:
                pass
    
    return {}


def extract_skills(query: str) -> List[str]:
    """Extract required skills from query."""
    query_lower = query.lower()
    found_skills = []
    
    for skill in COMMON_SKILLS:
        if skill in query_lower:
            found_skills.append(skill)
    
    return found_skills


def extract_seniority(query: str) -> str:
    """Extract job seniority level."""
    query_lower = query.lower()
    
    seniority_levels = {
        'entry': ['entry', 'junior', 'entry-level', 'fresh'],
        'mid': ['mid', 'mid-level', 'intermediate', 'mid-senior'],
        'senior': ['senior', 'lead', 'staff', 'principal', 'architect'],
        'executive': ['executive', 'director', 'vp', 'vice president', 'cto', 'ceo', 'head']
    }
    
    for level, keywords in seniority_levels.items():
        for keyword in keywords:
            if keyword in query_lower:
                return level
    
    return 'mid'  # Default


def extract_experience_years(query: str) -> Dict[str, int]:
    """Extract years of experience requirement."""
    query_lower = query.lower()
    
    # Look for patterns like "5 years", "3-5 years", "10+ years"
    patterns = [
        r'(\d+)\+?\s*years?',  # "5 years" or "5+ years"
        r'(\d+)-(\d+)\s*years?',  # "3-5 years"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, query_lower)
        if match:
            if len(match.groups()) == 1:
                years = int(match.group(1))
                return {'min': years, 'max': years + 10}
            else:
                return {
                    'min': int(match.group(1)),
                    'max': int(match.group(2))
                }
    
    return {}


def parse_natural_language_query(query: str) -> Dict[str, Any]:
    """
    Parse natural language job search query and extract structured parameters.
    
    Args:
        query: Natural language search query
        
    Returns:
        Dictionary with extracted parameters
    """
    return {
        'search_query': extract_core_query(query),
        'location': extract_location(query),
        'job_type': extract_job_type(query),
        'salary_range': extract_salary_range(query),
        'required_skills': extract_skills(query),
        'seniority': extract_seniority(query),
        'experience_years': extract_experience_years(query),
        'original_query': query
    }


def extract_core_query(query: str) -> str:
    """Remove filter keywords and extract core job title query."""
    # Remove common filter keywords
    filter_keywords = [
        r'in\s+\w+(?:\s+\w+)?',  # location
        r'at\s+\w+(?:\s+\w+)?',  # location
        r'for\s+\$?\d+k?.*',  # salary
        r'with\s+\d+\+?\s*years',  # experience
        r'remote|onsite|hybrid|full-time|part-time|contract',  # job type
        r'requiring?\s+.*',  # skills
    ]
    
    core_query = query
    for keyword_pattern in filter_keywords:
        core_query = re.sub(keyword_pattern, '', core_query, flags=re.IGNORECASE)
    
    return core_query.strip()
