"""
Advanced AI-powered job search and outreach features.
Includes natural language search, cover letter generation, and LinkedIn outreach.
"""

from flask import Blueprint, request, jsonify, current_app
import os
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging
from models import db, User, GeneratedCoverLetter, OutreachRecord
from nlp_parser import parse_natural_language_query
from cover_letter_generator import generate_cover_letter, generate_outreach_message
from linkedin_manager import LinkedInManager

ai_features_bp = Blueprint('ai_features', __name__, url_prefix='/ai')

# Initialize LinkedIn manager
linkedin_manager = LinkedInManager()


@ai_features_bp.route('/parse-query', methods=['POST'])
def parse_search_query():
    """
    Parse natural language search query and extract structured parameters.
    
    Example input: "python developer in San Francisco, remote, 120k salary"
    """
    data = request.get_json() or {}
    query = data.get('query', '')
    
    if not query:
        return jsonify({'error': 'Missing query parameter'}), 400
    
    try:
        parsed = parse_natural_language_query(query)
        return jsonify({
            'query': query,
            'parsed_params': parsed,
            'message': 'Query parsed successfully'
        }), 200
    except Exception as e:
        logging.error(f"Error parsing query: {e}")
        return jsonify({'error': f'Failed to parse query: {str(e)}'}), 500


@ai_features_bp.route('/generate-cover-letter', methods=['POST'])
@jwt_required()
def generate_cover_letter_endpoint():
    """
    Generate a customized cover letter for a job.
    
    Required: job_id, company, title
    Optional: resume_text, user_name
    """
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    
    job_id = data.get('job_id')
    job_title = data.get('title')
    company = data.get('company')
    resume_text = data.get('resume_text')
    user_name = data.get('user_name', 'Job Seeker')
    
    if not all([job_id, job_title, company]):
        return jsonify({'error': 'Missing job_id, title, or company'}), 400
    
    try:
        # Check if cover letter already exists
        existing = GeneratedCoverLetter.query.filter_by(
            user_id=user_id,
            job_id=job_id
        ).first()
        
        if existing:
            return jsonify({
                'message': 'Cover letter already generated',
                'cover_letter': existing.to_dict()
            }), 200
        
        # Generate new cover letter
        job = {
            'id': job_id,
            'title': job_title,
            'company': company,
            'summary': data.get('summary', ''),
            'requirements': data.get('requirements', [])
        }
        
        cover_letter_text = generate_cover_letter(job, resume_text, user_name)
        
        # Save to database
        cover_letter = GeneratedCoverLetter(
            user_id=user_id,
            job_id=job_id,
            job_title=job_title,
            company=company,
            cover_letter_text=cover_letter_text,
            customization_level='standard' if resume_text else 'minimal'
        )
        
        db.session.add(cover_letter)
        db.session.commit()
        
        return jsonify({
            'message': 'Cover letter generated successfully',
            'cover_letter': cover_letter.to_dict()
        }), 201
        
    except Exception as e:
        logging.error(f"Error generating cover letter: {e}")
        db.session.rollback()
        return jsonify({'error': f'Failed to generate cover letter: {str(e)}'}), 500



@ai_features_bp.route('/dev/generate-cover-letter', methods=['POST'])
def dev_generate_cover_letter():
    """Dev-only endpoint: generate a cover letter without authentication.

    Enabled when environment variable `ENABLE_DEV_COVER` is 'true' or when
    the Flask app is in debug mode. Not for production use.
    """
    enabled = os.environ.get('ENABLE_DEV_COVER', 'false').lower() == 'true' or (current_app and current_app.debug)
    if not enabled:
        return jsonify({'error': 'Dev cover-letter endpoint disabled'}), 403

    data = request.get_json() or {}
    job_id = data.get('job_id', 'dev-job')
    job_title = data.get('title', data.get('job_title', 'Developer'))
    company = data.get('company', data.get('company_name', 'ExampleCo'))
    resume_text = data.get('resume_text')
    user_name = data.get('user_name', 'Dev User')

    try:
        job = {
            'id': job_id,
            'title': job_title,
            'company': company,
            'summary': data.get('summary', ''),
            'requirements': data.get('requirements', [])
        }

        cover_letter_text = generate_cover_letter(job, resume_text, user_name)

        return jsonify({'message': 'Dev cover letter generated', 'cover_letter_text': cover_letter_text}), 200
    except Exception as e:
        logging.error(f"Dev generate cover letter error: {e}")
        return jsonify({'error': str(e)}), 500


@ai_features_bp.route('/find-hiring-managers', methods=['POST'])
def find_hiring_managers():
    """
    Find potential hiring managers at a company.
    
    Required: company_name
    Optional: job_title
    """
    data = request.get_json() or {}
    company_name = data.get('company_name', '')
    job_title = data.get('job_title', '')
    
    if not company_name:
        return jsonify({'error': 'Missing company_name'}), 400
    
    try:
        managers = linkedin_manager.find_hiring_managers(company_name, job_title)
        
        return jsonify({
            'company': company_name,
            'hiring_managers': managers,
            'count': len(managers),
            'note': 'Manual verification recommended for email addresses'
        }), 200
        
    except Exception as e:
        logging.error(f"Error finding hiring managers: {e}")
        return jsonify({'error': f'Failed to find managers: {str(e)}'}), 500


@ai_features_bp.route('/create-outreach', methods=['POST'])
@jwt_required()
def create_outreach():
    """
    Create an outreach workflow with multiple contact options.
    
    Required: job_id, company, title, hiring_manager_name
    Optional: hiring_manager_email, tone (professional, friendly, casual)
    """
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    
    job_id = data.get('job_id')
    company = data.get('company')
    job_title = data.get('title')
    hiring_manager_name = data.get('hiring_manager_name')
    tone = data.get('tone', 'professional')
    
    if not all([job_id, company, job_title, hiring_manager_name]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        user = User.query.get(user_id)
        
        job = {
            'id': job_id,
            'company': company,
            'title': job_title,
            'url': data.get('job_url', ''),
            'summary': data.get('summary', ''),
            'requirements': data.get('requirements', [])
        }
        
        hiring_manager = {
            'name': hiring_manager_name,
            'title': data.get('hiring_manager_title', 'Hiring Manager'),
            'email': data.get('hiring_manager_email'),
            'profile_url': data.get('linkedin_profile_url')
        }
        
        # Generate outreach options
        outreach_workflow = linkedin_manager.create_outreach_workflow(
            job=job,
            hiring_manager=hiring_manager,
            user_email=user.email
        )
        
        return jsonify({
            'message': 'Outreach workflow created',
            'workflow': outreach_workflow,
            'user_email': user.email,
            'recommendation': 'Choose your preferred outreach method below'
        }), 200
        
    except Exception as e:
        logging.error(f"Error creating outreach: {e}")
        return jsonify({'error': f'Failed to create outreach: {str(e)}'}), 500


@ai_features_bp.route('/send-outreach', methods=['POST'])
@jwt_required()
def send_outreach():
    """
    Record and prepare outreach message.
    
    Required: job_id, company, method (linkedin, email, portal)
    Optional: recipient_name, recipient_email, message
    """
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    
    job_id = data.get('job_id')
    company = data.get('company')
    method = data.get('method')  # linkedin, email, portal
    
    if not all([job_id, company, method]):
        return jsonify({'error': 'Missing job_id, company, or method'}), 400
    
    if method not in ['linkedin', 'email', 'portal']:
        return jsonify({'error': 'Invalid method. Use: linkedin, email, or portal'}), 400
    
    try:
        # Record outreach
        outreach = OutreachRecord(
            user_id=user_id,
            job_id=job_id,
            company=company,
            outreach_method=method,
            recipient_name=data.get('recipient_name'),
            recipient_email=data.get('recipient_email'),
            message_sent=data.get('message'),
            status='pending'
        )
        
        db.session.add(outreach)
        db.session.commit()
        
        response_data = {
            'message': f'Outreach recorded via {method}',
            'outreach_id': outreach.id,
            'status': 'pending',
            'next_steps': []
        }
        
        if method == 'email':
            response_data['next_steps'] = [
                'Copy the message from above',
                'Send from your email client',
                'Update status when you receive a response'
            ]
        elif method == 'linkedin':
            response_data['next_steps'] = [
                'Visit the hiring manager LinkedIn profile',
                'Send the message using LinkedIn messaging',
                'Record the response in the outreach tracker'
            ]
        else:  # portal
            response_data['next_steps'] = [
                'Visit the job application URL',
                'Submit your application with the cover letter',
                'Track application status'
            ]
        
        return jsonify(response_data), 201
        
    except Exception as e:
        logging.error(f"Error recording outreach: {e}")
        db.session.rollback()
        return jsonify({'error': f'Failed to record outreach: {str(e)}'}), 500


@ai_features_bp.route('/outreach-history', methods=['GET'])
@jwt_required()
def get_outreach_history():
    """Get user's outreach history."""
    user_id = get_jwt_identity()
    
    try:
        outreach_records = OutreachRecord.query.filter_by(user_id=user_id).order_by(
            OutreachRecord.created_at.desc()
        ).all()
        
        records = [record.to_dict() for record in outreach_records]
        
        # Summary stats
        stats = {
            'total_outreach': len(records),
            'by_method': {},
            'by_status': {}
        }
        
        for record in records:
            method = record['outreach_method']
            status = record['status']
            stats['by_method'][method] = stats['by_method'].get(method, 0) + 1
            stats['by_status'][status] = stats['by_status'].get(status, 0) + 1
        
        return jsonify({
            'outreach_records': records,
            'stats': stats,
            'count': len(records)
        }), 200
        
    except Exception as e:
        logging.error(f"Error fetching outreach history: {e}")
        return jsonify({'error': f'Failed to fetch history: {str(e)}'}), 500


@ai_features_bp.route('/cover-letters', methods=['GET'])
@jwt_required()
def get_cover_letters():
    """Get all generated cover letters for the user."""
    user_id = get_jwt_identity()
    
    try:
        cover_letters = GeneratedCoverLetter.query.filter_by(user_id=user_id).order_by(
            GeneratedCoverLetter.created_at.desc()
        ).all()
        
        letters = [letter.to_dict() for letter in cover_letters]
        
        return jsonify({
            'cover_letters': letters,
            'count': len(letters)
        }), 200
        
    except Exception as e:
        logging.error(f"Error fetching cover letters: {e}")
        return jsonify({'error': f'Failed to fetch cover letters: {str(e)}'}), 500


@ai_features_bp.route('/cover-letters/<int:letter_id>', methods=['DELETE'])
@jwt_required()
def delete_cover_letter(letter_id):
    """Delete a generated cover letter."""
    user_id = get_jwt_identity()
    
    try:
        letter = GeneratedCoverLetter.query.filter_by(
            id=letter_id,
            user_id=user_id
        ).first()
        
        if not letter:
            return jsonify({'error': 'Cover letter not found'}), 404
        
        db.session.delete(letter)
        db.session.commit()
        
        return jsonify({'message': 'Cover letter deleted'}), 200
        
    except Exception as e:
        logging.error(f"Error deleting cover letter: {e}")
        db.session.rollback()
        return jsonify({'error': f'Failed to delete cover letter: {str(e)}'}), 500
