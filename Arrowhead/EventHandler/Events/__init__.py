import os
import json

class EventManager:
    
    @staticmethod
    def loadEvent(event_type):
        basepath = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(basepath, event_type + ".json")
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except:
            raise Exception("Event type \"" + event_type + "\" not configured")