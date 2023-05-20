from kernel.ipcmemory import IPCMemory

import kernel.registry as Registry
import time

async def main(args) -> int:

    if Registry.read("SOFTWARE.Helium.LabConfigs.EnableBrokenFeatures") != "1":
        return
    
    expirey = int(Registry.read("SOFTWARE.Helium.Services.IPCMemoryPeriodicPurger.ExpireyInSeconds"))
    waitingTime = int(Registry.read("SOFTWARE.Helium.Services.IPCMemoryPeriodicPurger.CheckCyclePeriod"))

    if Registry.read("SOFTWARE.Helium.Services.IPCMemoryPeriodicPurger.Enabled") == "1":
        time.sleep(waitingTime)
        return 0

    
    
    # Notify that the service is running
    if Registry.read("SOFTWARE.Helium.Services.IPCMemoryPeriodicPurger.Verbose") == "1":
        print("IPCMemoryPeriodicPurger: Running")
    
    # Iterate through all objects in the IPCMemory
    for i in range(0, len(IPCMemory.objects)):
        object = IPCMemory.objects[i]
        if object["persistent"] == True:
            if Registry.read("SOFTWARE.Helium.Services.IPCMemoryPeriodicPurger.Verbose") == "1":
                print(f"IPCMemoryPeriodicPurger: Skipping {object['name']} because it is persistent")
            continue

        timeSinceLastAccess = round(time.time()*1000) - object["lastAccess"]
        if timeSinceLastAccess > expirey:
            if Registry.read("SOFTWARE.Helium.Services.IPCMemoryPeriodicPurger.Verbose") == "1":
                print(f"IPCMemoryPeriodicPurger: Deleting {object['name']} because it has expired")
            IPCMemory.deleteObj(object["name"])
        else:
            if Registry.read("SOFTWARE.Helium.Services.IPCMemoryPeriodicPurger.Verbose") == "1":
                print(f"IPCMemoryPeriodicPurger: Skipping {object['name']} because it has not expired")
        
    if Registry.read("SOFTWARE.Helium.Services.IPCMemoryPeriodicPurger.Verbose") == "1":
        print(f"IPCMemoryPeriodicPurger: Sleeping for {waitingTime} seconds")

    time.sleep(waitingTime)



    