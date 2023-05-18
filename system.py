import kernel.argsParser as argsParser
import kernel.procmgr as procmgr

from kernel.ipcmemory import IPCMemory
from typing import List


# This is a very simple interactive user interface directly connected to kernel process manager.
class System():
    
    def __init__(self, lineArgs) -> None:
        self.args: list = lineArgs

    def main(args: List[str]) -> int:
        val = 0
        while True:
            userIn: str = input(f"{val} >>> ")
            if userIn == "exit":
                break
            args = argsParser.parse(userIn.split())
            if len(args) == 0:
                continue
            val = procmgr.launch(args[0], args[1:], Registry.read("SOFTWARE.Helium.Settings.RawReturnFlag") == "1")
            