import kernel.procmgr as procmgr
import kernel.argsParser as argsParser
import kernel.hookmgr as hookmgr
import kernel.registry as Registry
import time
import os
import signal
from kernel.ipcmemory import IPCMemory

IPCMemory.setObj("System.Cache.StartTime.Epoch", round(time.time()*1000), True, "1111")
IPCMemory.setObj("System.Location.Root", os.path.abspath("./"), True, "1111")
IPCMemory.setObj("System.kernel.session", 0, True, "2222")

Registry.build("defaults/registry-default", os.path.join("./", "registry"), silent=True, overwrite=False)
Registry.build("defaults/registry-enforced", os.path.join("./", "registry"), silent = True, overwrite=True)


hookmgr.runHooks([], kernelHooks = True)
hookmgr.runHooks([], kernelHooks = False)

Registry.build("defaults/registry-enforced", os.path.join("./", "registry"), silent = True, overwrite=True)

procmgr.exec("system.py", "System", [])

current_pid = os.getpid()
os.kill(current_pid, signal.SIGTERM)
