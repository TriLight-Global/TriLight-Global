# models/user_activity.py

class UserSearchHistory(db.Document):
    user_id = db.StringField(required=True)
    query = db.StringField(required=True)
    filters = db.DictField()
    timestamp = db.DateTimeField(default=datetime.utcnow)

    meta = {'collection': 'user_search_history'}

class UserPropertyView(db.Document):
    user_id = db.StringField(required=True)
    property_id = db.StringField(required=True)
    timestamp = db.DateTimeField(default=datetime.utcnow)
    duration = db.IntField()  # Duration of view in seconds

    meta = {'collection': 'user_property_views'}

