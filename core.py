import kernel.procmgr as procmgr
import kernel.argsParser as argsParser
import kernel.hookmgr as hookmgr
import time
from kernel.states import States

States.setObj("Core.Cache.StartTime.Epoch", round(time.time()*1000))

hookmgr.runHooks([], kernelHooks = True)
hookmgr.runHooks([], kernelHooks = False)



procmgr.main("system.py", "System", [])
