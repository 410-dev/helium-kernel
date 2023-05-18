import kernel.registry as Registry
import kernel.procmgr as procmgr

import os
import json

def runHooks(parameters: list, kernelHooks: bool) -> list:
    # Returns list of hooks executed with the exit code
    # If kernelHooks is True, it will run kernel hooks, otherwise it will run user hooks
    
    hooksPath: str = ""
    blacklists: list = []
    if kernelHooks:
        
        if Registry.read("SOFTWARE.Helium.Settings.Hooks.Enabled") == "0":
            return []
        
        hooksPath = "kernel/hooks/"
        blacklistData = Registry.read("SOFTWARE.Helium.Hooks.KernelBlacklist")
        if blacklistData != None:
            blacklistData = json.loads(blacklistData)
            blacklists = blacklistData['data']
    else:
        
        if Registry.read("SOFTWARE.Helium.Settings.Hooks.OthersEnabled") == "0":
            return []
        
        hooksPath = Registry.read("SOFTWARE.Helium.Values.Data.Struct.Hooks")
        blacklistData = Registry.read("SOFTWARE.Helium.Hooks.OtherBlacklist")
        if blacklistData != None:
            blacklistData = json.loads(blacklistData)
            blacklists = blacklistData['data']

    hooks: list = os.listdir(hooksPath)
    
    report: list = []
    
    for hook in hooks:
        if hook.startswith("_") or hook.startswith("."):
            continue
        
        if hook in blacklists:
            if Registry.read("SOFTWARE.Helium.Settings.KernelModulesVerbose") == "1": 
                print(f"Hook '{hook}' is blacklisted, skipping...")
            continue
        
        if Registry.read("SOFTWARE.Helium.Settings.KernelModulesVerbose") == "1":
            print(f"Running hook '{hook}'...")
        
        hookPath: str = os.path.join(hooksPath, hook)
        try:
            with open(hookPath, 'r') as f:
                exitcode = procmgr.execScript(hookPath, parameters)
                reportRow = [hook, exitcode]
                report.append(reportRow)
                if Registry.read("SOFTWARE.Helium.Settings.KernelModulesVerbose") == "1":
                    print(f"Hook '{hook}' exited with code {exitcode}")
        except Exception as e:
            print(f"ERROR: Failed running hook {hookPath}: {e}")
            