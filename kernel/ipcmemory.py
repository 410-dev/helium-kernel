import inspect
import time
import os
import copy
import kernel.registry as Registry


# Interprocess Communication Memory: This is a class that stores all the objects that are shared between processes
class IPCMemory():
    
    objects = []
    
    @staticmethod
    def getObj(name: str, fullData = False, includeEligiblePermissionData = False):

        # Find the object
        object = None
        for i in range(len(IPCMemory.objects)-1, -1, -1):
            obj = IPCMemory.objects[i]
            if obj["name"] == name:

                # Update last access time
                IPCMemory.objects[i]["lastAccess"] = round(time.time()*1000)

                # Copy object
                object = copy.deepcopy(obj)
                break

        # If not found, return None
        if object == None:
            if includeEligiblePermissionData:
                return None, "2"
            else:
                return None

        # [Permission Check] Get the system root location
        rootloc = "./"
        for obj in IPCMemory.objects:
            if obj["name"] == "System.Location.Root":
                rootloc = obj["value"]
                break

        # [Permission Check] Define spaces for each permission level
        rootloc = os.path.abspath(rootloc)
        publicSpace = [os.path.join(rootloc, "data")]
        userSpace   = [os.path.join(rootloc, "data")]
        systemSpace = [os.path.join(rootloc, "data", "hooks")]
        kernelSpace = [os.path.join(rootloc, "kernel")]
        spaces = [publicSpace, userSpace, systemSpace, kernelSpace]

        # [Permission Check] Get the execution location
        execLocation = inspect.stack()[1].filename
        execLocation = os.path.abspath(execLocation)

        # [Permission Check] If the execution location is states.py itself, get the location of the caller
        idx = 2
        while execLocation.endswith("kernel/states.py"):
            execLocation = inspect.stack()[idx].filename
            execLocation = os.path.abspath(execLocation)
            idx += 1


        lvl = 0  # If lvl is 0, it means it is in no space. 1 means public, 2 means user, 3 means system, 4 means kernel
        permission = "0"

        # [Permission Check] Check if the execution location is in any of the spaces
        for space in spaces:
            for singleSpace in space:
                if execLocation.startswith(singleSpace):
                    if space == publicSpace:
                        lvl = 1
                    elif space == userSpace:
                        lvl = 2
                    elif space == systemSpace:
                        lvl = 3
                    elif space == kernelSpace:
                        lvl = 4
                    break
        
        # [Permission Check] Update permission. If the execution location and the object's writtenBy location is the same, set permission to 2 (read and write)
        permission = object["permission"][lvl-1]
        if execLocation == object["writtenBy"]:
            permission = "2"


        # [Permission Check] Otherwise, if the object is persistent, set space level to 1 (public space)
        else:
            if lvl == 0:
                if Registry.read("SYSTEM.Helium.Settings.PrintIPCWarning") == "1":
                    print("[KRNL] [IPCMemory] WARNING: Executing script is not in any space. This is not recommended.")
                lvl = 1

        # [Permission Check] If the object is not accessible, return None
        if permission == "0":
            if Registry.read("SYSTEM.Helium.Settings.PrintIPCWarning") == "1":
                print(f"[KRNL] [IPCMemory] WARNING: Executing script ({execLocation}) does not have permission in its space to access this object '{name}'. Permission: {object['permission']}")
            if includeEligiblePermissionData:
                return None, None
            else:
                return None
        
        # If permission is ok, return the object
        if not fullData:
            if includeEligiblePermissionData:
                return object["value"], permission
            else:
                return object["value"]
        else:
            if includeEligiblePermissionData:
                return object, permission
            else:
                return object


    @staticmethod
    def deleteObj(name: str):
        object, permission = IPCMemory.getObj(name, fullData=True, includeEligiblePermissionData=True)
        if object == None:
            if Registry.read("SYSTEM.Helium.Settings.PrintIPCWarning") == "1":
                print(f"[KRNL] [IPCMemory] Failed to delete object: {name}, Permission: {permission}")
            return False
        else:
            if permission == "2":
                IPCMemory.objects.remove(object)
                return True
            else:
                return False

    @staticmethod
    # Permission notation:    Public, User, System, Kernel    (Public means sub processes executed by user)
    # Default permission:       0       0      1      2       (0 means no access, 1 means read, 2 means read and write)
    def setObj(name: str, data, persistent = False, permission = "0012"):
        if len(permission) != 4:
            if Registry.read("SYSTEM.Helium.Settings.PrintIPCWarning") == "1":
                print("[KRNL] [IPCMemory] Invalid permission length. Setting to default: 0012")
            permission = "0012"

        if not permission.isnumeric():
            if Registry.read("SYSTEM.Helium.Settings.PrintIPCWarning") == "1":
                print("[KRNL] [IPCMemory] Invalid permission type. Setting to default: 0012")
            permission = "0012"

        # If the object already exists, remove for update
        object, existingPermission = IPCMemory.getObj(name, fullData=True, includeEligiblePermissionData=True)
        if object != None:
            if existingPermission != "2":
                if Registry.read("SYSTEM.Helium.Settings.PrintIPCWarning") == "1":
                    print(f"[KRNL] [IPCMemory] WARNING: Executing script does not have permission to update (write) this object '{name}'. Permission: {object['permission']}")
                return False

            if not IPCMemory.deleteObj(name):
                return False

        stateObject: dict = {
            "name": name,
            "writtenBy": inspect.stack()[1].filename,
            "writtenAt": round(time.time()*1000),
            "lastAccess": round(time.time()*1000),
            "permission": permission,
            "persistent": persistent,
            "value": data
        }
        IPCMemory.objects.append(stateObject)
        return True        
    