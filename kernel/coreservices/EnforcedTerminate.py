import kernel.registry as Registry
import kernel.journal as Journal

import os
import signal

async def main(args) -> int:
    if Registry.read("SYSTEM.Helium.Values.Triggers.Terminate") != "1":
        return
    
    Journal.addJournal("Detected termination trigger, terminating...")
    Registry.delete("SYSTEM.Helium.Values.Triggers.Terminate")
    current_pid = os.getpid()
    os.kill(current_pid, signal.SIGTERM)
