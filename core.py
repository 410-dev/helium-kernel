import kernel.procmgr as procmgr
import kernel.argsParser as argsParser
import kernel.hookmgr as hookmgr
import kernel.registry as Registry
import time
from kernel.states import States

Registry.build("defaults/registry-reserved", silent = True)

States.setObj("Core.Cache.StartTime.Epoch", round(time.time()*1000))

hookmgr.runHooks([], kernelHooks = True)
hookmgr.runHooks([], kernelHooks = False)



procmgr.exec("system.py", "System", [])
