import inspect
import time
import os

import kernel.fs as fs
import kernel.registry as Registry

def createJournalLocation(id: str) -> str:
    lib: str = Registry.read("SYSTEM.Helium.Values.Paths.Data.Library")
    fs.mkdirInData(f"{lib}/logs/journal/{id}")


def addJournal(content: str) -> None:
    # Add a journal entry
    # This function will create the journal directory if it does not exist.
    # Then, it will create a journal file if not exist. If the journal file exists, it will append to it.

    # Get the journal ID from the caller - get module name
    callerModulePath: str = inspect.stack()[1].filename
    callerModulePath: str = os.path.abspath(callerModulePath)
    callerModulePath: str = callerModulePath.replace("\\", "/")
    callerModulePath: str = callerModulePath.split("/")
    callerModulePath: str = callerModulePath[-1]

    # Get the parent process of the caller
    callerParent: str = inspect.stack()[2].filename
    callerParent: str = os.path.abspath(callerParent)
    callerParent: str = callerParent.replace("\\", "/")
    callerParent: str = callerParent.split("/")
    callerParent: str = callerParent[-1]
    
    # Create the journal directory if it does not exist
    createJournalLocation(callerModulePath)

    # Get the journal file path
    lib: str = Registry.read("SYSTEM.Helium.Values.Paths.Data.Library")
    journalPath: str = f"{lib}/logs/journal/{callerModulePath}/journal.log"

    # Create the journal file if it does not exist
    if not os.path.exists(journalPath):
        fs.mkdirInData(f"{lib}/logs/journal/{callerModulePath}")
        fs.writeToDisk(journalPath, "")

    # Add the timestamp at the beginning of the journal entry
    timestamp: str = time.strftime("%Y-%m-%d %H:%M:%S")
    content = f"[{timestamp}] [From {callerParent}] {content}"

    # Append to the journal file
    fs.writeToDisk(journalPath, content + "\n", append=True)
