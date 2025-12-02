from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    favorites = db.relationship('FavoriteJob', backref='user', lazy=True, cascade='all, delete-orphan')
    saved_searches = db.relationship('SavedSearch', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'created_at': self.created_at.isoformat()
        }


class FavoriteJob(db.Model):
    __tablename__ = 'favorite_jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    job_id = db.Column(db.String(255), nullable=False)
    job_title = db.Column(db.String(255), nullable=False)
    company = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255))
    job_data = db.Column(db.JSON, nullable=False)  # Store full job details as JSON
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'job_id', name='uq_user_job'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'job_id': self.job_id,
            'job_title': self.job_title,
            'company': self.company,
            'location': self.location,
            'created_at': self.created_at.isoformat(),
            **self.job_data
        }


class SavedSearch(db.Model):
    __tablename__ = 'saved_searches'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    search_query = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(500))
    filters = db.Column(db.JSON)  # Store filter criteria as JSON
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_searched = db.Column(db.DateTime)
    
    def to_dict(self):
        return {
            'id': self.id,
            'search_query': self.search_query,
            'description': self.description,
            'filters': self.filters,
            'created_at': self.created_at.isoformat(),
            'last_searched': self.last_searched.isoformat() if self.last_searched else None
        }


class GeneratedCoverLetter(db.Model):
    __tablename__ = 'cover_letters'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    job_id = db.Column(db.String(255), nullable=False)
    job_title = db.Column(db.String(255), nullable=False)
    company = db.Column(db.String(255), nullable=False)
    cover_letter_text = db.Column(db.Text, nullable=False)
    customization_level = db.Column(db.String(50), default='standard')  # minimal, standard, tailored
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'job_id', name='uq_user_cover_letter'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'job_id': self.job_id,
            'job_title': self.job_title,
            'company': self.company,
            'cover_letter': self.cover_letter_text,
            'customization_level': self.customization_level,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class OutreachRecord(db.Model):
    __tablename__ = 'outreach_records'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    job_id = db.Column(db.String(255), nullable=False)
    company = db.Column(db.String(255), nullable=False)
    outreach_method = db.Column(db.String(50), nullable=False)  # linkedin, email, portal
    recipient_name = db.Column(db.String(255))
    recipient_email = db.Column(db.String(255))
    message_sent = db.Column(db.Text)
    status = db.Column(db.String(50), default='pending')  # pending, sent, interested, rejected
    response = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'job_id': self.job_id,
            'company': self.company,
            'outreach_method': self.outreach_method,
            'recipient_name': self.recipient_name,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

