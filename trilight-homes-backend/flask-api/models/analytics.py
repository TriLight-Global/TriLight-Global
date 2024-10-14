#analytics models
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY, JSON

db = SQLAlchemy()

class PropertyAnalytics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'))
    views = db.Column(db.Integer, default=0)
    favorites = db.Column(db.Integer, default=0)
    last_price_change = db.Column(db.DateTime)
    days_on_market = db.Column(db.Integer)

class MarketTrend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(255))
    property_type = db.Column(db.String(50))
    date = db.Column(db.Date)
    average_price = db.Column(db.Numeric(12, 2))
    median_price = db.Column(db.Numeric(12, 2))
    total_listings = db.Column(db.Integer)
    days_on_market_avg = db.Column(db.Float)

class PropertyValuation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'))
    estimated_value = db.Column(db.Numeric(12, 2))
    confidence_score = db.Column(db.Float)
    last_updated = db.Column(db.DateTime)
    comparable_properties = db.Column(ARRAY(db.Integer))

class SearchLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    search_params = db.Column(JSON)
    results_count = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)

class PerformanceMetric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    metric_name = db.Column(db.String(100))
    metric_value = db.Column(db.Float)
    timestamp = db.Column(db.DateTime)

# This model would be used to cache complex query results
class QueryCache(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    query_hash = db.Column(db.String(64), unique=True)
    result = db.Column(JSON)
    created_at = db.Column(db.DateTime)
    expires_at = db.Column(db.DateTime)