import os
from cover_letter_generator import generate_cover_letter

job = {
    'title': 'Senior Python Developer',
    'company': 'ExampleCorp',
    'summary': 'Build backend services and data pipelines for a fast-moving fintech startup.',
    'requirements': ['Python', 'Django', 'AWS', 'SQL']
}

resume = "Experienced backend developer with 8+ years building REST APIs, ETL pipelines, and production ML infra."

print('Using generate_cover_letter() (OpenAI primary, then fallback)')
try:
    text = generate_cover_letter(job, resume, user_name='Alice')
    print('\n--- Generated Cover Letter ---\n')
    print(text[:2000])
except Exception as e:
    print('generate_cover_letter failed:', e)
