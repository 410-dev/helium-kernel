import kernel.procmgr as procmgr
import kernel.argsParser as argsParser
import kernel.hookmgr as hookmgr

hookmgr.runHooks([], True)
hookmgr.runHooks([], False)

while True:
    userIn: str = input(">>> ")
    if userIn == "exit":
        break
    args = argsParser.parse(userIn.split())
    procmgr.launch(args[0], args[1:])
    
