"""
Cover letter generation module using OpenAI GPT.
Generates customized cover letters based on job and resume.
"""

import os
from typing import Optional, Dict, Any
import openai

# Set OpenAI API key
openai.api_key = os.environ.get("OPENAI_API_KEY")


def generate_cover_letter(
    job: Dict[str, Any],
    resume_text: Optional[str] = None,
    user_name: str = "Job Seeker"
) -> str:
    """
    Generate a customized cover letter for a job posting.
    
    Args:
        job: Job posting details
        resume_text: User's resume text (optional)
        user_name: User's name for personalization
        
    Returns:
        Generated cover letter as string
    """
    
    # Use OpenAI if available; otherwise fall back to template
    if not openai.api_key:
        return generate_fallback_cover_letter(job, user_name)
    
    try:
        job_title = job.get('title', 'the position')
        company = job.get('company', 'the company')
        summary = job.get('summary', '')
        requirements = job.get('requirements', [])
        
        # Format requirements
        req_text = ""
        if isinstance(requirements, list):
            req_text = "\n".join([f"- {req}" for req in requirements[:5]])
        else:
            req_text = str(requirements)
        
        resume_context = ""
        if resume_text:
            # Use first 1000 chars of resume for context
            resume_context = f"\n\nUser's Resume Summary:\n{resume_text[:1000]}"
        
        prompt = f"""Write a professional, compelling cover letter for the following job posting. 
        
Job Title: {job_title}
Company: {company}
Job Description: {summary}

Key Requirements:
{req_text}
{resume_context}

Please write a concise (200-300 words) cover letter that:
1. Shows genuine interest in the role and company
2. Highlights relevant skills from the requirements
3. If resume provided, align experience with job needs
4. Uses professional but personable tone
5. Ends with strong call to action

Format: Start with "Dear Hiring Manager," and sign off appropriately."""

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert cover letter writer creating compelling, personalized cover letters for job seekers."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        cover_letter = response['choices'][0]['message']['content'].strip()
        return cover_letter
        
    except Exception as e:
        print(f"Error generating cover letter with OpenAI: {e}")
        return generate_fallback_cover_letter(job, user_name)


def generate_fallback_cover_letter(job: Dict[str, Any], user_name: str) -> str:
    """Generate a basic cover letter template when API unavailable."""
    
    job_title = job.get('title', 'the position')
    company = job.get('company', 'the company')
    
    return f"""Dear Hiring Manager,

I am writing to express my strong interest in the {job_title} position at {company}. 
With my relevant experience and skills, I am confident I can make a meaningful contribution to your team.

Throughout my career, I have developed a strong foundation in the key areas this role requires. 
Your job posting aligns perfectly with my professional goals and areas of expertise. I am particularly 
drawn to {company}'s commitment to innovation and excellence in the industry.

I am eager to bring my skills, work ethic, and collaborative spirit to your organization. 
I would welcome the opportunity to discuss how my background and enthusiasm can contribute to your team's success.

Thank you for considering my application. I look forward to the possibility of speaking with you soon.

Sincerely,
{user_name}"""


def generate_outreach_message(
    job: Dict[str, Any],
    hiring_manager: str = "Hiring Manager",
    company: str = "",
    tone: str = "professional"
) -> str:
    """
    Generate a LinkedIn outreach message for a hiring manager.
    
    Args:
        job: Job posting details
        hiring_manager: Name of the hiring manager
        company: Company name
        tone: Message tone (professional, friendly, casual)
        
    Returns:
        Generated outreach message
    """
    
    job_title = job.get('title', 'this opportunity')
    
    if tone == "friendly":
        message = f"""Hi {hiring_manager},

I came across the {job_title} role at {company} and it caught my attention! Your company's approach to innovation really resonates with me, and I think I could be a great fit for this position.

I'd love to learn more about the opportunity and discuss how I could contribute to your team. Would you be open to a quick conversation?

Looking forward to connecting!"""
    
    elif tone == "casual":
        message = f"""Hey {hiring_manager},

Excited about the {job_title} opening at {company}. This looks like an amazing opportunity that aligns perfectly with my background and interests.

Would love to chat about how I can add value to your team!"""
    
    else:  # professional (default)
        message = f"""Dear {hiring_manager},

I hope this message finds you well. I recently came across the {job_title} position at {company} and was impressed by the opportunity and your company's vision.

I believe my background and expertise align well with the requirements for this role. I would appreciate the opportunity to discuss how I can contribute to your team's success.

Thank you for considering my outreach. I look forward to hearing from you.

Best regards"""
    
    return message


def generate_email_outreach(
    job: Dict[str, Any],
    hiring_manager_email: str,
    hiring_manager_name: str = "Hiring Manager"
) -> Dict[str, str]:
    """
    Generate an email outreach with subject line and body.
    
    Args:
        job: Job posting details
        hiring_manager_email: Email address
        hiring_manager_name: Name of hiring manager
        
    Returns:
        Dictionary with subject and body
    """
    
    job_title = job.get('title', 'this opportunity')
    company = job.get('company', 'your company')
    
    subject = f"Interested in {job_title} Position at {company}"
    
    body = f"""Dear {hiring_manager_name},

I am writing to express my interest in the {job_title} position at {company}.

With my relevant skills and experience, I am confident I can make a valuable contribution to your team. 
I am particularly interested in your company's vision and would welcome the opportunity to discuss how I can help achieve your goals.

I have attached my resume for your reference and would be grateful for the opportunity to discuss this role further.

Thank you for your time and consideration. I look forward to hearing from you.

Best regards,
[Your Name]
[Your Email]
[Your Phone Number]"""
    
    return {
        'to': hiring_manager_email,
        'subject': subject,
        'body': body
    }
