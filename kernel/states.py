import inspect
import datetime

class States():
    
    objects = []
    
    @staticmethod
    def getObj(name: str, fullData = False):
        # print(inspect.stack())
        for obj in States.objects:
            if obj["name"] == name:
                if not fullData:
                    return obj["value"]
                else:
                    return obj
        
        return None
        

    @staticmethod
    def setObj(name: str, data, persistent = False, permission = None):
        # print(inspect.stack())
        # print(f"Setting: {name}   with {data}, permission of {permission}")
        stateObject: dict = {
            "name": name,
            "permission": permission,
            "writtenBy": inspect.stack()[1],
            "writtenAt": datetime.datetime.now(),
            "persistent": persistent,
            "value": data
        }
        States.objects.append(stateObject)
        
    