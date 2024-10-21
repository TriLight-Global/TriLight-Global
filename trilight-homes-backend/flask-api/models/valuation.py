# models/valuation.py

class PropertyValuation(db.Document):
    property_id = db.StringField(required=True)
    estimated_value = db.DecimalField(precision=2)
    confidence_score = db.FloatField()
    valuation_date = db.DateTimeField(default=datetime.utcnow)
    factors = db.DictField()

    meta = {'collection': 'property_valuations'}

class PropertyValuation(client.Model):
    id = client.Column(client.Integer, primary_key=True)
    property_id = client.Column(client.Integer, client.ForeignKey('property.id'))
    estimated_value = client.Column(client.Numeric(12, 2))
    confidence_score = client.Column(client.Float)
    last_updated = client.Column(client.DateTime)
    comparable_properties = client.Column(ARRAY(client.Integer))
