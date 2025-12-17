from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, Text, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from typing import Optional

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, index=True)
    password_hash = Column(String(255))
    full_name = Column(String(255))
    profile_bio = Column(Text, nullable=True)
    location = Column(String(255), nullable=True)
    target_countries = Column(JSON, default=[])
    min_salary = Column(Float, nullable=True)
    max_salary = Column(Float, nullable=True)
    currency = Column(String(3), default="USD")
    preferred_job_types = Column(JSON, default=[])
    preferred_industries = Column(JSON, default=[])
    experience_years = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Resume(Base):
    __tablename__ = "resumes"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    filename = Column(String(255))
    file_path = Column(String(512))
    extracted_text = Column(Text)
    skills = Column(JSON, default=[])
    experience_summary = Column(Text, nullable=True)
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Job(Base):
    __tablename__ = "jobs"
    id = Column(String(255), primary_key=True)
    title = Column(String(255), index=True)
    company = Column(String(255), index=True)
    location = Column(String(255))
    country = Column(String(100))
    region = Column(String(100), nullable=True)
    job_type = Column(String(50))
    employment_status = Column(String(100), nullable=True)
    min_salary = Column(Float, nullable=True)
    max_salary = Column(Float, nullable=True)
    currency = Column(String(3), nullable=True)
    experience_level = Column(String(50), nullable=True)
    industry = Column(String(100), nullable=True)
    company_size = Column(String(50), nullable=True)
    description = Column(Text)
    required_skills = Column(JSON, default=[])
    remote_option = Column(Boolean, default=False)
    posted_date = Column(DateTime, nullable=True)
    application_url = Column(String(512))
    is_active = Column(Boolean, default=True)
    cached_at = Column(DateTime, default=datetime.utcnow)
    source = Column(String(50), default="foorilla")

class Application(Base):
    __tablename__ = "applications"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    job_id = Column(String(255), ForeignKey("jobs.id"))
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=True)
    status = Column(String(50), default="submitted")  # submitted, viewed, rejected, interview, accepted
    match_score = Column(Float, nullable=True)
    cover_letter = Column(Text, nullable=True)
    submitted_at = Column(DateTime, default=datetime.utcnow)
    response_at = Column(DateTime, nullable=True)
    rejection_reason = Column(Text, nullable=True)
    auto_applied = Column(Boolean, default=False)
    form_data_used = Column(JSON, nullable=True)
    notes = Column(Text, nullable=True)

class JobCache(Base):
    __tablename__ = "job_cache"
    id = Column(Integer, primary_key=True)
    filters_hash = Column(String(255), unique=True, index=True)
    filters = Column(JSON)
    job_ids = Column(JSON)  # List of cached job IDs
    total_count = Column(Integer)
    cached_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)

class ApplicationLog(Base):
    __tablename__ = "application_logs"
    id = Column(Integer, primary_key=True)
    application_id = Column(Integer, ForeignKey("applications.id"))
    action = Column(String(50))  # auto_apply_started, form_filled, submit_attempted, submit_success, error
    details = Column(JSON)
    error_message = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
