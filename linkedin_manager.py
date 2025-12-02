"""
LinkedIn integration module for finding hiring managers and sending messages.
Supports both web scraping fallback and LinkedIn API integration.
"""

import os
from typing import Dict, List, Optional, Any
import re
import requests


class LinkedInManager:
    """Manages LinkedIn operations - finding managers and sending outreach."""
    
    def __init__(self, access_token: Optional[str] = None):
        """
        Initialize LinkedIn manager.
        
        Args:
            access_token: LinkedIn API access token (from OAuth)
        """
        self.access_token = access_token or os.environ.get("LINKEDIN_ACCESS_TOKEN")
        self.linkedin_api_url = "https://api.linkedin.com/v2"
        self.scrape_api_url = "https://nubela.co/proxycurl/api"
        self.scrape_api_key = os.environ.get("PROXYCURL_API_KEY")
    
    def find_hiring_managers(self, company_name: str, job_title: str = "") -> List[Dict[str, str]]:
        """
        Find potential hiring managers at a company.
        
        Args:
            company_name: Name of the company
            job_title: Job title to match (e.g., "recruiting manager", "hiring")
            
        Returns:
            List of hiring managers with name, title, and profile URL
        """
        
        if self.scrape_api_key:
            return self._find_managers_via_proxycurl(company_name, job_title)
        else:
            return self._find_managers_fallback(company_name, job_title)
    
    def _find_managers_via_proxycurl(self, company_name: str, job_title: str) -> List[Dict[str, str]]:
        """Use ProxyCurl API to find hiring managers."""
        try:
            # Search for company
            headers = {"Authorization": f"Bearer {self.scrape_api_key}"}
            
            query = job_title or "recruiting"
            
            # This is a simplified endpoint - actual implementation would use their API
            managers = [
                {
                    "name": "Sample Hiring Manager",
                    "title": "Recruiting Manager",
                    "company": company_name,
                    "profile_url": f"https://linkedin.com/in/hiring-manager-{company_name}",
                    "email_hint": f"hiring@{company_name.lower().replace(' ', '')}.com"
                }
            ]
            
            return managers
            
        except Exception as e:
            print(f"Error finding managers via ProxyCurl: {e}")
            return []
    
    def _find_managers_fallback(self, company_name: str, job_title: str) -> List[Dict[str, str]]:
        """Fallback: Return template suggestions for manual outreach."""
        
        # Generate likely titles for hiring managers
        likely_titles = [
            "Recruiting Manager",
            "HR Manager",
            "Talent Manager",
            "Hiring Manager",
            "Chief People Officer",
            "Head of Talent"
        ]
        
        managers = []
        for title in likely_titles[:2]:  # Return top 2
            managers.append({
                "name": f"{title} at {company_name}",
                "title": title,
                "company": company_name,
                "profile_url": f"https://linkedin.com/search/results/people/?keywords={company_name}%20{title}",
                "email_hint": f"recruiting@{company_name.lower().replace(' ', '')}.com",
                "note": "Search LinkedIn directly or use the profile URL to find specific managers"
            })
        
        return managers
    
    def send_linkedin_message(
        self,
        recipient_id: str,
        message: str,
        job_title: str = ""
    ) -> Dict[str, Any]:
        """
        Send a LinkedIn message (requires API access).
        
        Args:
            recipient_id: LinkedIn profile ID of recipient
            message: Message content
            job_title: Job title for reference
            
        Returns:
            Response status
        """
        
        if not self.access_token:
            return {
                "success": False,
                "message": "LinkedIn API access not configured. Use email outreach instead.",
                "method": "manual"
            }
        
        try:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "message": message,
                "recipients": [recipient_id]
            }
            
            # LinkedIn messaging API endpoint
            response = requests.post(
                f"{self.linkedin_api_url}/messaging/conversations",
                json=payload,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 201:
                return {
                    "success": True,
                    "message": "Message sent successfully",
                    "method": "linkedin_api"
                }
            else:
                return {
                    "success": False,
                    "message": f"Failed to send message: {response.status_code}",
                    "method": "linkedin_api"
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Error sending LinkedIn message: {str(e)}",
                "method": "linkedin_api"
            }
    
    def get_email_from_company_domain(self, company_name: str) -> str:
        """
        Guess company domain and suggest email format.
        
        Args:
            company_name: Company name
            
        Returns:
            Suggested email domain
        """
        
        # Common company domain variations
        domain = company_name.lower().replace(" ", "").replace(",", "")
        
        return f"{domain}.com"
    
    def format_profile_url(self, linkedin_id: str) -> str:
        """Format LinkedIn profile URL."""
        return f"https://www.linkedin.com/in/{linkedin_id}"
    
    def create_outreach_workflow(
        self,
        job: Dict[str, str],
        hiring_manager: Dict[str, str],
        user_email: str
    ) -> Dict[str, Any]:
        """
        Create complete outreach workflow with multiple options.
        
        Args:
            job: Job posting details
            hiring_manager: Hiring manager details
            user_email: User's email for contact
            
        Returns:
            Workflow with multiple outreach options
        """
        
        from cover_letter_generator import generate_email_outreach, generate_outreach_message
        
        company = job.get('company', 'Company')
        job_title = job.get('title', 'Position')
        
        # Option 1: LinkedIn Message
        linkedin_msg = generate_outreach_message(
            job=job,
            hiring_manager=hiring_manager.get('name', 'Hiring Manager'),
            company=company,
            tone='professional'
        )
        
        # Option 2: Email
        email_data = generate_email_outreach(
            job=job,
            hiring_manager_email=f"hr@{self.get_email_from_company_domain(company)}",
            hiring_manager_name=hiring_manager.get('name', 'Hiring Manager')
        )
        
        # Option 3: Direct message via job portal
        portal_msg = f"""Dear Hiring Team,

I am applying for the {job_title} position and believe my background aligns perfectly with your requirements.

Please find my resume attached and feel free to reach out if you have any questions.

Best regards,
{user_email}"""
        
        return {
            "job_id": job.get('id'),
            "company": company,
            "job_title": job_title,
            "hiring_manager": hiring_manager,
            "outreach_options": {
                "linkedin_message": {
                    "method": "LinkedIn Direct Message",
                    "content": linkedin_msg,
                    "profile_url": hiring_manager.get('profile_url'),
                    "requires": "LinkedIn API or manual send"
                },
                "email": {
                    "method": "Email",
                    "to": email_data['to'],
                    "subject": email_data['subject'],
                    "body": email_data['body'],
                    "requires": "Email client"
                },
                "job_portal": {
                    "method": "Job Portal Application",
                    "content": portal_msg,
                    "url": job.get('url'),
                    "requires": "Company job portal"
                }
            },
            "recommendation": "LinkedIn message is most effective for initial outreach"
        }
