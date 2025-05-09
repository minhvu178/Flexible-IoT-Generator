# src/utils/datetime_utils.py
import json
from datetime import datetime

class DateTimeEncoder(json.JSONEncoder):
    """JSON encoder that properly handles datetime objects."""
    
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

def datetime_json_dumps(obj):
    """Convert object to JSON string with datetime handling."""
    return json.dumps(obj, cls=DateTimeEncoder)