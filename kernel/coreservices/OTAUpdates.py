from kernel.ipcmemory import IPCMemory
import kernel.fs as Filesystem
import kernel.procmgr as procmgr
import kernel.registry as Registry
import kernel.journal as Journal

import time

async def main(args) -> int:

    # if Registry.read("SOFTWARE.Helium.LabConfigs.EnableBrokenFeatures") != "1":
    #     return

    otaURL = Registry.read("SOFTWARE.Helium.Services.OTAUpdates.URL")
    otaLastIndex = Registry.read("SOFTWARE.Helium.Services.OTAUpdates.LastIndex")
    delayUntilNextLoop = Registry.read("SOFTWARE.Helium.Services.OTAUpdates.CheckCyclePeriod")

    Journal.addJournal(f"Settings: otaURL={otaURL}, otaLastIndex={otaLastIndex}, delayUntilNextLoop={delayUntilNextLoop}")

    # Notify that the service is running
    if Registry.read("SOFTWARE.Helium.Services.OTAUpdates.Verbose") == "1":
        print("[SRVC] [otaUpdates] Sleeping")

    # Sleep
    Journal.addJournal(f"Sleeping for {delayUntilNextLoop} seconds")
    time.sleep(int(delayUntilNextLoop))

    try:
        otaLastIndex = int(otaLastIndex)
    except:
        otaLastIndex = 0

    Journal.addJournal(f"Checking for updates from {otaURL} with index {otaLastIndex}")
    
    requestURL: str = otaURL.replace("%INDEX%", str(otaLastIndex))
    '''
    basic return structure:
    {
        "otaIndex": 10,
        "format": 1,
        "updates": [
            {
                "name": "",
                "type": "",
                "version": "",
                "url": "",
                "description": "",
                "hash": ""
                "target": "SYSTEM.Helium.Values.Paths.Kernel.Services"
            }
        ]
    }
    '''

    # Notify that the service is running
    if Registry.read("SOFTWARE.Helium.Services.OTAUpdates.Verbose") == "1":
        print("[SRVC] [otaUpdates] Running")

    # Get the JSON from the server
    try:
        import requests
        response = requests.get(requestURL)
    except:
        if Registry.read("SOFTWARE.Helium.Services.OTAUpdates.Verbose") == "1":
            print(f"[SRVC] [otaUpdates] Failed to connect to server - {requestURL}")
        return 0

    # Check if the request was successful
    if response.status_code != 200:
        Journal.addJournal(f"Failed to connect to server - {requestURL}")
        if Registry.read("SOFTWARE.Helium.Services.OTAUpdates.Verbose") == "1":
            print(f"[SRVC] [otaUpdates] Failed to parse from server - {response.status_code}")
        return 0

    # Parse the JSON
    try:
        json = response.json()
        Journal.addJournal(f"Successfully parsed from server - JSON")
    except:
        Journal.addJournal(f"Failed to parse from server - JSON")
        if Registry.read("SOFTWARE.Helium.Services.OTAUpdates.Verbose") == "1":
            print(f"[SRVC] [otaUpdates] Failed to parse from server - JSON")
        return 0
    
    # Check if format matches
    if "format" not in json:
        Journal.addJournal(f"Error opening format from server - JSON")
        if Registry.read("SOFTWARE.Helium.Services.OTAUpdates.Verbose") == "1":
            print(f"[SRVC] [otaUpdates] Error opening format from server - JSON")
        return 0
    
    # Check if the JSON is valid
    if "otaIndex" not in json:
        Journal.addJournal(f"Error opening index from server - JSON")
        if Registry.read("SOFTWARE.Helium.Services.OTAUpdates.Verbose") == "1":
            print(f"[SRVC] [otaUpdates] Error opening index from server - JSON")
        return 0

    # Check if the index is valid
    if json["otaIndex"] <= otaLastIndex:
        Journal.addJournal(f"No updates available")
        if Registry.read("SOFTWARE.Helium.Services.OTAUpdates.Verbose") == "1":
            print(f"[SRVC] [otaUpdates] No updates available")
        return 0
    
    # Check if the updates are valid
    if "updates" not in json:
        Journal.addJournal(f"Error opening updates from server - JSON")
        if Registry.read("SOFTWARE.Helium.Services.OTAUpdates.Verbose") == "1":
            print(f"[SRVC] [otaUpdates] Error opening updates from server - JSON")
        return 0
    
    # Check if the updates are valid
    if len(json["updates"]) == 0:
        Journal.addJournal(f"No updates available")
        if Registry.read("SOFTWARE.Helium.Services.OTAUpdates.Verbose") == "1":
            print(f"[SRVC] [otaUpdates] No updates available")
        return 0
    
    # Notify that the service is running
    Journal.addJournal(f"Found {len(json['updates'])} updates")
    if Registry.read("SOFTWARE.Helium.Services.OTAUpdates.Verbose") == "1":
        print(f"[SRVC] [otaUpdates] Found {len(json['updates'])} updates")

    # Loop through the updates
    try:
        for update in json["updates"]:
            # Notify that the service is running
            Journal.addJournal(f"Downloading {update['name']}")
            if Registry.read("SOFTWARE.Helium.Services.OTAUpdates.Verbose") == "1":
                print(f"[SRVC] [otaUpdates] Downloading {update['name']}")

            # Download the update
            try:
                import requests
                response = requests.get(update["url"])
            except:
                Journal.addJournal(f"Failed to download update - {update['name']}")
                if Registry.read("SOFTWARE.Helium.Services.OTAUpdates.Verbose") == "1":
                    print(f"[SRVC] [otaUpdates] Failed to download update - {update['name']}")
                continue

            # Check if the request was successful
            if response.status_code != 200:
                Journal.addJournal(f"Failed to download update - {update['name']}")
                if Registry.read("SOFTWARE.Helium.Services.OTAUpdates.Verbose") == "1":
                    print(f"[SRVC] [otaUpdates] Failed to download update - {update['name']}")
                continue

            # Write the update to disk
            try:
                Journal.addJournal(f"Writing update to disk - {update['name']}")
                Filesystem.mkdir("/data/tmp")
                with open(f"/data/tmp/{update['name']}", "wb") as file:
                    file.write(response.content)
                    Journal.addJournal(f"Successfully wrote update to disk - {update['name']}")
            except:
                Journal.addJournal(f"Failed to write update to disk - {update['name']}")
                if Registry.read("SOFTWARE.Helium.Services.OTAUpdates.Verbose") == "1":
                    print(f"[SRVC] [otaUpdates] Failed to write update to disk - {update['name']}")
                continue
            
            # Notify that the service is running
            Journal.addJournal(f"Installing {update['name']}")
            if Registry.read("SOFTWARE.Helium.Services.OTAUpdates.Verbose") == "1":
                print(f"[SRVC] [otaUpdates] Installing {update['name']}")

            # Install the update
            try:
                Journal.addJournal(f"Installing update - {update['name']}")
                procmgr.launch("install", [f"/data/tmp/{update['name']}"])
            except:
                Journal.addJournal(f"Failed to install update - {update['name']}")
                if Registry.read("SOFTWARE.Helium.Services.OTAUpdates.Verbose") == "1":
                    print(f"[SRVC] [otaUpdates] Failed to install update - {update['name']}")
                continue

            # Notify that the service is running
            Journal.addJournal(f"Update installed - {update['name']}")
            if Registry.read("SOFTWARE.Helium.Services.OTAUpdates.Verbose") == "1":
                print(f"[SRVC] [otaUpdates] Update installed - {update['name']}")
    except:
        Journal.addJournal(f"Failed to install updates")
        if Registry.read("SOFTWARE.Helium.Services.OTAUpdates.Verbose") == "1":
            print(f"[SRVC] [otaUpdates] Failed to install updates")
        return 0
