from app import db
from flask.json import JSONEncoder

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, db.Model):
            return obj.to_dict()
        return super().default(obj)