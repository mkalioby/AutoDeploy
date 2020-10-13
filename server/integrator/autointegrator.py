__author__ = 'mohamed'

import sys
import os
import yaml
import subprocess
import json
import config
import requests
from jose import jwt
from contextlib import contextmanager


EOM = "\n\n###"
debug = False
slient = False

def encrypt_result(msg):
    file = open(config.publicKey, 'r')
    st = "".join(file.readlines())
    return jwt.encode(msg, st, algorithm="RS256")

def update_database(result):
    client_url = config.client_url + "api/ris"
    try:
        serverStatus = requests.get(client_url).status_code
        if serverStatus == 200:
            encoded_token = encrypt_result(result)
            r = requests.post(client_url, data=json.dumps(encoded_token))  # TODO : If the client is die what to do ?
            if not slient: print("Sent : ", True if r.status_code == 200 else False)
    except Exception as exp:
        import traceback
        if not slient: print("Sent : ", False, " ", exp)
        if not slient: print(traceback.format_exc())

def run(executer, raiseError=True,exitcode=False, id=None, wait=True):
    PIPE = subprocess.PIPE
    p = subprocess.Popen(executer, stdout=PIPE, stderr=PIPE, shell=True)
    (stdout, stderr) = p.communicate()
    st = stderr
    if id:
        f = open("/tmp/" + id + ".err", 'w')
        f.write(st)
        f.flush()
        f.close()
        f = open("/tmp/" + id + ".out", 'w')
        f.write(stdout)
        f.flush()
        f.close()

    if len(stderr) > 0 and "fatal" in str(stderr):
        return "ERR:" + str(stderr)
    if stdout == "": return "Done"
    if exitcode:
        if p.returncode not in [0,'0']:
            return [p.returncode,"ERR:" + str(stderr)]
        return [p.returncode,stdout.decode('utf-8')]
    return stdout


def printNotication(message):
    if slient: return
    print(message)
    print("=" * len(message))


def runEvents(config, workdir, event, raiseErrorOnStdErr=True):
    if event in config["events"].keys():
        for script in config["events"][event]:
            wait = True
            if not script["location"].startswith("/"):
                cmd = workdir + script["location"]
            else:
                cmd = script["location"]
            if "interpreter" in script.keys():
                cmd = "%s %s" % (script["interpreter"], cmd)
            if "run-as" in script.keys():
                if not script["run-as"] == "root":
                    cmd = "su %s -c %s" % (script["run-as"], cmd)
            if not slient: print("Running:", cmd)
            if "wait" in script.keys():
                wait = script["wait"]
            if "ignore-stderr" in script.keys():
                if script["ignore-stderr"] in ("yes", "True", "true", "y", "True", True):
                    raiseErrorOnStdErr = False
            run(cmd, raiseErrorOnStdErr, wait=wait)


def handleRuns(tasks, workdir):
    result = {}
    for task in tasks:
        cmd = "%s %s" % (task['interpreter'], task["location"])
        print("TASK : ",cmd)
        task_result = run(cmd,exitcode=True)
        print("RESULT : ",task_result[0])
        result[cmd] = {"exit_code": task_result[0], "result": task_result[1]}
    return result

@contextmanager
def runTest(config,workdir=".",raiseErrorOnStdErr=True,jobID=None):
    printNotication("Running Before Run scripts:")
    runEvents(config, workdir, "beforeRun", raiseErrorOnStdErr)

    printNotication("Starting Test Scripts")

    if not "tasks" in config.keys():
        if not slient: print("  No tasks to run ... skipping")
    else:
        if not slient: print("     Running tasks")
        output=handleRuns(config['tasks'], workdir)
        if jobID:
            result = {"jobID":jobID,"output":output}
            update_database(result)
        if not slient: print("     Tasks done")
    printNotication("Test Scripts Done.......")

    printNotication("Starting After Install Scripts")
    runEvents(config, workdir, "afterRun", raiseErrorOnStdErr)


if __name__ == "__main__":
    config = None
    workdir = None
    stdErr = True
    for arg in sys.argv[1:]:
        if "--config" in arg:
            yamlFile = arg.split("=")[1]
            config = yaml.safe_load(open(yamlFile))
            print(config)
        elif "--workdir" in arg:
            workdir = arg.split("=")[1]
        elif "--no-stderr" in arg:
            stdErr = False
        elif "--slient" in arg:
            slient = True
        elif "--debug" in arg:
            debug = True
    if not config:
        print("--config  should be set")
        exit()
    runTest(config, workdir, stdErr)