import sys
import os

import registry as Registry

    
# Get parameters: --config x, --registry x, --target x
regBlueprintSrc: str = ""
target: str = ""
if len(sys.argv) != 5:
    print(f"Invalid number of arguments. Expected 4, got {len(sys.argv) - 1}")
    exit(1)

try:
    for i in range(0, len(sys.argv)):
        if sys.argv[i] == "--registry":
            regBlueprintSrc = sys.argv[i + 1]
        elif sys.argv[i] == "--target":
            target = sys.argv[i + 1]
except:
    pass

if regBlueprintSrc == "" or target == "":
    print(f"Invalid arguments. Expected --registry, and --target")
    print(f"Got --registry {regBlueprintSrc}, and --target {target}")
    exit(1)

# Build registry
Registry.build(regBlueprintSrc, os.path.join(target, "registry"), True)

exit(0)
