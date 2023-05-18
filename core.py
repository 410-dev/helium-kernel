import kernel.procmgr as procmgr
import kernel.argsParser as argsParser
import kernel.hookmgr as hookmgr
import kernel.registry as Registry
import time
import os
from kernel.states import States

Registry.build("defaults/registry-default", os.path.join("./", "registry"), silent=True, overwrite=False)
Registry.build("defaults/registry-enforced", os.path.join("./", "registry"), silent = True, overwrite=True)

States.setObj("Core.Cache.StartTime.Epoch", round(time.time()*1000))

hookmgr.runHooks([], kernelHooks = True)
hookmgr.runHooks([], kernelHooks = False)

Registry.build("defaults/registry-enforced", os.path.join("./", "registry"), silent = True, overwrite=True)

procmgr.exec("system.py", "System", [])
