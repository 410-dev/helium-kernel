import kernel.registry as Registry

class Version:
    
    def __init__(self, lineArgs) -> None:
        self.args: list = lineArgs

    def main(self) -> int:
        try: 
            baseName = Registry.read("SYSTEM.Helium.Settings.Profiles.Foundation")
            baseVersion = Registry.read("SYSTEM.Helium.Settings.Profiles.Version")
            print(f"BaseSystem: {baseName} {baseVersion}")
        except Exception as e:
            print(f"Error opening config.json e: {e}")