from kernel.ipcmemory import IPCMemory

import kernel.registry as Registry
import kernel.journal as Journal

import time

async def main(args) -> int:

    # if Registry.read("SOFTWARE.Helium.LabConfigs.EnableBrokenFeatures") != "1":
    #     return
    
    expirey = int(Registry.read("SOFTWARE.Helium.Services.IPCMemoryPeriodicPurger.ExpireyInSeconds"))
    waitingTime = int(Registry.read("SOFTWARE.Helium.Services.IPCMemoryPeriodicPurger.CheckCyclePeriod"))

    Journal.addJournal(f"Settings: expirey={expirey}, waitingTime={waitingTime}")

    # Notify that the service is running
    if Registry.read("SOFTWARE.Helium.Services.IPCMemoryPeriodicPurger.Verbose") == "1":
        print("[SRVC] [IPCMemoryPeriodicPurger] Running")
    
    if Registry.read("SOFTWARE.Helium.Services.IPCMemoryPeriodicPurger.Enabled") == "1":
        # Notify that the service is running
        Journal.addJournal(f"Waiting for {waitingTime} seconds")
        time.sleep(waitingTime)
        if Registry.read("SOFTWARE.Helium.Services.IPCMemoryPeriodicPurger.Verbose") == "1":
            print("[SRVC] [IPCMemoryPeriodicPurger] Waiting finished. Running")
    else:
        if Registry.read("SOFTWARE.Helium.Services.IPCMemoryPeriodicPurger.Verbose") == "1":
            print("[SRVC] [IPCMemoryPeriodicPurger] Disabled")
        Journal.addJournal(f"Disabled")
        return 0
    
    
    # Iterate through all objects in the IPCMemory
    for i in range(0, len(IPCMemory.objects)):
        object = IPCMemory.objects[i]
        if object["persistent"] == True:
            Journal.addJournal(f"Skipping {object['name']} because it is persistent")
            if Registry.read("SOFTWARE.Helium.Services.IPCMemoryPeriodicPurger.Verbose") == "1":
                print(f"[SRVC] [IPCMemoryPeriodicPurger] Skipping {object['name']} because it is persistent")
            continue

        timeSinceLastAccess = round(time.time()*1000) - object["lastAccess"]
        if timeSinceLastAccess > expirey:
            Journal.addJournal(f"Deleting {object['name']} because it has expired")
            if Registry.read("SOFTWARE.Helium.Services.IPCMemoryPeriodicPurger.Verbose") == "1":
                print(f"[SRVC] [IPCMemoryPeriodicPurger] Deleting {object['name']} because it has expired")
            IPCMemory.deleteObj(object["name"])
        else:
            Journal.addJournal(f"Skipping {object['name']} because it has not expired")
            if Registry.read("SOFTWARE.Helium.Services.IPCMemoryPeriodicPurger.Verbose") == "1":
                print(f"[SRVC] [IPCMemoryPeriodicPurger] Skipping {object['name']} because it has not expired")
        
    if Registry.read("SOFTWARE.Helium.Services.IPCMemoryPeriodicPurger.Verbose") == "1":
        print(f"[SRVC] [IPCMemoryPeriodicPurger] Sleeping for {waitingTime} seconds")

    Journal.addJournal(f"Sleeping for {waitingTime} seconds")
    time.sleep(waitingTime)



    