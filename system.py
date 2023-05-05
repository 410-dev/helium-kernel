import kernel.procmgr as procmgr
import kernel.argsParser as argsParser
import kernel.hookmgr as hookmgr

hookmgr.runHooks([], True)
hookmgr.runHooks([], False)

val = 0
while True:
    userIn: str = input(f"{val} >>> ")
    if userIn == "exit":
        break
    args = argsParser.parse(userIn.split())
    val = procmgr.launch(args[0], args[1:])
    
