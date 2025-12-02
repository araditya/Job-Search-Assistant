from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, FavoriteJob, SavedSearch, User

favorites_bp = Blueprint('favorites', __name__, url_prefix='/favorites')


@favorites_bp.route('', methods=['GET'])
@jwt_required()
def get_favorites():
    """Get all favorite jobs for the current user."""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    favorites = [fav.to_dict() for fav in user.favorites]
    return jsonify({'favorites': favorites, 'count': len(favorites)}), 200


@favorites_bp.route('', methods=['POST'])
@jwt_required()
def add_favorite():
    """Add a job to favorites."""
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    
    if not data.get('job_id') or not data.get('job_title') or not data.get('company'):
        return jsonify({'error': 'Missing job_id, job_title, or company'}), 400
    
    # Check if already favorited
    existing = FavoriteJob.query.filter_by(user_id=user_id, job_id=data['job_id']).first()
    if existing:
        return jsonify({'message': 'Already in favorites'}), 200
    
    favorite = FavoriteJob(
        user_id=user_id,
        job_id=data['job_id'],
        job_title=data['job_title'],
        company=data['company'],
        location=data.get('location', ''),
        job_data=data  # Store full job object
    )
    
    db.session.add(favorite)
    db.session.commit()
    
    return jsonify({'message': 'Job added to favorites', 'favorite': favorite.to_dict()}), 201


@favorites_bp.route('/<int:fav_id>', methods=['DELETE'])
@jwt_required()
def remove_favorite(fav_id):
    """Remove a job from favorites."""
    user_id = get_jwt_identity()
    favorite = FavoriteJob.query.filter_by(id=fav_id, user_id=user_id).first()
    
    if not favorite:
        return jsonify({'error': 'Favorite not found'}), 404
    
    db.session.delete(favorite)
    db.session.commit()
    
    return jsonify({'message': 'Job removed from favorites'}), 200


@favorites_bp.route('/job/<job_id>', methods=['DELETE'])
@jwt_required()
def remove_favorite_by_job_id(job_id):
    """Remove a job from favorites by job_id."""
    user_id = get_jwt_identity()
    favorite = FavoriteJob.query.filter_by(job_id=job_id, user_id=user_id).first()
    
    if not favorite:
        return jsonify({'error': 'Favorite not found'}), 404
    
    db.session.delete(favorite)
    db.session.commit()
    
    return jsonify({'message': 'Job removed from favorites'}), 200


# Saved Searches

@favorites_bp.route('/searches', methods=['GET'])
@jwt_required()
def get_saved_searches():
    """Get all saved searches for the current user."""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    searches = [search.to_dict() for search in user.saved_searches]
    return jsonify({'searches': searches, 'count': len(searches)}), 200


@favorites_bp.route('/searches', methods=['POST'])
@jwt_required()
def save_search():
    """Save a search query."""
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    
    if not data.get('search_query'):
        return jsonify({'error': 'Missing search_query'}), 400
    
    saved_search = SavedSearch(
        user_id=user_id,
        search_query=data['search_query'],
        description=data.get('description', ''),
        filters=data.get('filters')
    )
    
    db.session.add(saved_search)
    db.session.commit()
    
    return jsonify({'message': 'Search saved', 'search': saved_search.to_dict()}), 201


@favorites_bp.route('/searches/<int:search_id>', methods=['DELETE'])
@jwt_required()
def delete_saved_search(search_id):
    """Delete a saved search."""
    user_id = get_jwt_identity()
    saved_search = SavedSearch.query.filter_by(id=search_id, user_id=user_id).first()
    
    if not saved_search:
        return jsonify({'error': 'Search not found'}), 404
    
    db.session.delete(saved_search)
    db.session.commit()
    
    return jsonify({'message': 'Search deleted'}), 200
