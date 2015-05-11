__author__ = 'mohamed'

import sys
import os

import yaml
import Common


debug=False
slient=False

def printNotication(message):
    if slient: return
    print message
    print "="*len(message)

def runEvents(config,workdir,event,raiseErrorOnStdErr=True):
    if event in config["events"].keys():
        for script in config["events"][event]:
            wait=True
            cmd=workdir+script["location"]
            if "interpreter" in script.keys():
                cmd="%s %s"%(script["interpreter"],cmd)
            if "run-as" in script.keys():
                if not script["run-as"]=="root":
                    cmd="su %s -c %s"%(script["run-as"],cmd)
            if not slient: print "Running:", cmd
            if "wait" in script.keys():
                wait=script["wait"]
            Common.run(cmd,raiseErrorOnStdErr,wait=wait)

def handleFiles(files,workdir):
    for file in files:
        if file["destination"].endswith("/") and not file["source"].endswith("/"):
            if not os.path.exists(file["destination"]):
                os.makedirs(file["destination"])
        if file["source"].endswith("/"):
            Common.run("sudo rsync -rz --delete --exclude='.git' %s %s"%(workdir+file["source"],file["destination"]))

def handlePermissions(permissions,raiseErrorOnStdErr):
    for permission in permissions:
        if "owner" in permission.keys():
            cmd="sudo chown %s:%s %s"%(permission["owner"],permission["group"],permission["object"])
            if "dir" in permission["type"].lower():
                cmd += " -R"
                if debug:
                    print "         ", cmd
            Common.run(cmd,raiseErrorOnStdErr)
        if "mode" in permission.keys():
            cmd="sudo chmod %s %s"%(permission["mode"],permission["object"])
            if "dir" in permission["type"].lower():
                cmd += " -R"
                if debug:  print "         ",cmd
            Common.run(cmd,raiseErrorOnStdErr)

def deploy(config,workdir=".",raiseErrorOnStdErr=True):
    if workdir[-1] != '/': workdir += "/"
    printNotication("Running Before Install scripts:")
    runEvents(config,workdir,"beforeInstall",raiseErrorOnStdErr)

    printNotication("Starting Deployment")
    if not slient: print "     Copying Files"
    handleFiles(config["files"],workdir)
    if not slient: print "     Copying done"

    if not slient: print "     Setting Permissions"
    handlePermissions(config["permissions"],raiseErrorOnStdErr)
    if not slient: print "     Permissions Done"

    printNotication("Deployment Done.......")

    printNotication("Starting After Install Scripts")
    runEvents(config,workdir,"afterInstall",raiseErrorOnStdErr)
    return "Done"
if __name__=="__main__":
    config=None
    workdir=None
    stdErr=True
    for arg in sys.argv[1:]:
        if "--config" in arg:
            yamlFile=arg.split("=")[1]
            config=yaml.safe_load(open(yamlFile))
            print  config
        elif "--workdir" in arg:
            workdir=arg.split("=")[1]
        elif "--no-stderr" in arg:
            stdErr=False
        elif "--slient" in arg:
            slient=True
        elif "--debug" in arg:
            debug=True
    if not config or not workdir:
        print "--config and --workdir should be set"
        exit()
    deploy(config,workdir,stdErr)

