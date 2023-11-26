import kernel.registry as Registry
from kernel.ipcmemory import IPCMemory

import os

def writeToDisk(path: str, data: str, append=False) -> None:
    # Writes data to a file
    # If the file does not exist, it will be created
    # If the file exists, it will be overwritten
    # This function will create the directory if it does not exist
    # This function will return None if the file could not be written to
    # This function will return True if the file was written to successfully

    # Create the directory if it does not exist
    directory: str = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Write the file
    try:
        # with open(path, "w") as file:
        #     file.write(data)
        with open(path, "a" if append else "w") as file:
            file.write(data)
    except:
        return None

    return True


def getRoot() -> str:
    return IPCMemory.getObj("System.Location.Root") + os.sep


def mkdirInData(path: str) -> bool:
    return mkdirInRoot(Registry.read("SYSTEM.Helium.Values.Paths.Data.Root") + path)

def mkdirInRoot(path: str) -> bool:
    # Creates a directory
    # This function will create the directory if it does not exist
    # This function will return None if the directory could not be created
    # This function will return True if the directory was created successfully

    # Create the directory if it does not exist
    path = getRoot() + path
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except:
            return False

    return True


def listFilesInDirectory(path: str) -> list:
    # Lists all files in a directory
    # This function will return None if the directory does not exist
    # This function will return a list of files if the directory exists

    # Check if the directory exists
    path = getRoot() + path
    if not os.path.exists(path):
        return None

    # List all files in the directory
    files: list = []
    for file in os.listdir(path):
        files.append(file)

    return files

def listFilesInDataDirectory(path: str) -> list:
    return listFilesInDirectory(Registry.read("SYSTEM.Helium.Values.Paths.Data.Root") + path)