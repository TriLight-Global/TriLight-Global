#analytics models
# from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY, JSON
from pymongo import MongoClient

client = MongoClient()

class PropertyAnalytics(client.Model):
    id = client.Column(client.Integer, primary_key=True)
    property_id = client.Column(client.Integer, client.ForeignKey('property.id'))
    views = client.Column(client.Integer, default=0)
    favorites = client.Column(client.Integer, default=0)
    last_price_change = client.Column(client.DateTime)
    days_on_market = client.Column(client.Integer)

class MarketTrend(client.Model):
    id = client.Column(client.Integer, primary_key=True)
    location = client.Column(client.String(255))
    property_type = client.Column(client.String(50))
    date = client.Column(client.Date)
    average_price = client.Column(client.Numeric(12, 2))
    median_price = client.Column(client.Numeric(12, 2))
    total_listings = client.Column(client.Integer)
    days_on_market_avg = client.Column(client.Float)

class PropertyValuation(client.Model):
    id = client.Column(client.Integer, primary_key=True)
    property_id = client.Column(client.Integer, client.ForeignKey('property.id'))
    estimated_value = client.Column(client.Numeric(12, 2))
    confidence_score = client.Column(client.Float)
    last_updated = client.Column(client.DateTime)
    comparable_properties = client.Column(ARRAY(client.Integer))

class SearchLog(client.Model):
    id = client.Column(client.Integer, primary_key=True)
    user_id = client.Column(client.Integer, client.ForeignKey('user.id'), nullable=True)
    search_params = client.Column(JSON)
    results_count = client.Column(client.Integer)
    timestamp = client.Column(client.DateTime)

class PerformanceMetric(client.Model):
    id = client.Column(client.Integer, primary_key=True)
    metric_name = client.Column(client.String(100))
    metric_value = client.Column(client.Float)
    timestamp = client.Column(client.DateTime)

# This model would be used to cache complex query results
class QueryCache(client.Model):
    id = client.Column(client.Integer, primary_key=True)
    query_hash = client.Column(client.String(64), unique=True)
    result = client.Column(JSON)
    created_at = client.Column(client.DateTime)
    expires_at = client.Column(client.DateTime)