from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY, JSON
from datetime import datetime

db = SQLAlchemy()

class PropertyAnalytics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, unique=True, nullable=False)
    views_count = db.Column(db.Integer, default=0)
    favorites_count = db.Column(db.Integer, default=0)
    search_appearances = db.Column(db.Integer, default=0)
    last_price_change = db.Column(db.DateTime)
    days_on_market = db.Column(db.Integer)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

class MarketTrend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    area = db.Column(db.String(255), nullable=False)
    property_type = db.Column(db.String(50), nullable=False)
    average_price = db.Column(db.Numeric(12, 2))
    median_price = db.Column(db.Numeric(12, 2))
    price_change_percentage = db.Column(db.Numeric(5, 2))
    total_listings = db.Column(db.Integer)
    inventory_level = db.Column(db.Integer)
    days_on_market_avg = db.Column(db.Float)
    date = db.Column(db.Date, nullable=False)

class PerformanceMetric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, nullable=False)
    metric_name = db.Column(db.String(100), nullable=False)
    metric_value = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class AnalyticsReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    report_type = db.Column(db.String(50), nullable=False)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)
    data = db.Column(JSON)
    filters = db.Column(JSON)

class PropertyRecommendation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    property_id = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserAnalytics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=True, nullable=False)
    total_properties_viewed = db.Column(db.Integer, default=0)
    total_inquiries_made = db.Column(db.Integer, default=0)
    total_favorites = db.Column(db.Integer, default=0)
    last_login = db.Column(db.DateTime)
    account_creation_date = db.Column(db.DateTime, nullable=False)

class SearchAnalytics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    search_query = db.Column(db.Text)
    filters_used = db.Column(JSON)
    results_count = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)