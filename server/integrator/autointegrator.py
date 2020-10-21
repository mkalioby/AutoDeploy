__author__ = 'mohamed'

import subprocess
import json
import config
import requests
from jose import jwt

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
            if r.status_code == 200:
                if not slient: print("Sent : ", True)
            else:
                if not slient: print("Sent : ", False, "Code : ",r.status_code)
    except Exception as exp:
        import traceback
        if not slient: print("Sent : ", False, " ", exp)
        if not slient: print(traceback.format_exc())


def run(executer, workdir, id=None, interpreter="/bin/bash"):
    PIPE = subprocess.PIPE
    newExecuter = "export work_dir='" + workdir + "'; cd $work_dir ;" + executer
    print("Command => ",newExecuter)
    p = subprocess.Popen(newExecuter, stdout=PIPE, stderr=PIPE, shell=True, executable=interpreter)
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
    exit_code = p.returncode
    if p.returncode in [0,'0']:
        if stdout.decode('utf-8') in ['',None,' ']:
            result = stderr.decode('utf-8')
        else:
            result = stdout.decode('utf-8')
    else:
        if stderr.decode('utf-8') in ['',None,' ']:
            result = stdout.decode('utf-8')
        else:
            result = stderr.decode('utf-8')
    return {"exit_code": exit_code,"result": result}


def printNotication(message):
    if slient: return
    print("=" * 10)
    print(message)
    print("=" * 10)


def runEvents(config, workdir, result, event):
    if not "events" in config:
        print("Nothing in events section")
    if event in config["events"].keys():
        for script in config["events"][event]:
            if not "location" in script.keys():
                print("location event not exists")
                pass
            cmd = script["location"]
            if "interpreter" in script.keys(): cmd = "%s %s" % (script["interpreter"], cmd)
            if "run-as" in script.keys() and not script["run-as"] == "root": cmd = "su %s -c %s" % (
                script["run-as"], cmd)
            if not slient: print("Running")
            run_res = run(cmd, workdir)
            if not slient: print("Done")
            if run_res['exit_code'] not in [0, '0']:
                result['output'][cmd] = run_res
            else:
                Coverage = None
                if event == 'afterRun' and run_res['result'].find("Coverage: ") not in [-1, '-1']:
                    Coverage = run_res['result'].split(": ")[1].replace("\n", "")
                result["output"]['Coverage'] = Coverage


def handleRuns(tasks, workdir):
    result = {}
    for task in tasks:
        cmd = "%s" % task["location"]
        print("TASK : ", cmd)
        task_result = run(cmd, workdir, interpreter=task.get('interpreter', '/bin/bash'))
        print("RESULT : ",task_result['exit_code'])
        result[cmd] = task_result
    return result


def switch_change(workdir, change_type, change_id, result):
    if change_type == 'tag':
        switch_command = "git checkout tags/%s" % (change_id)
    else:
        switch_command = "git reset --hard % s" % (change_id)
    run_res = run(switch_command, workdir)
    if run_res['exit_code'] not in [0, '0']:
        result['output'][switch_command] = run_res


def get_author(workdir, result):
    author_command = 'git log -n1 --pretty=format:"%H,,%h,,%an,,%ae,,%ar,,%s,,%cd" | cat -'
    author = run(author_command, workdir)
    if author['exit_code'] in [0, '0']:
        author_info = author['result'].split(",,")[2:4]
        result['output']['author_name'] = author_info[0]
        result['output']['author_email'] = author_info[1]
    else:
        result['output'][author_command] = author


def get_branch(workdir, result):
    branch_command = 'git rev-parse --abbrev-ref HEAD | cat -'
    branch = run(branch_command, workdir)
    if branch['exit_code'] in [0, '0']:
        result['output']['branch'] = branch['result'].replace("\n","")
    else:
        result['output'][branch_command] = branch

def get_config(workdir):
    import yaml
    import os
    yaml_file = None
    for file in os.listdir(workdir):
        if file.endswith("ci.yaml"):
            yaml_file = yaml.safe_load(open(os.path.join(workdir, file)))
    return yaml_file


def runTest(config=None,workdir=".", project_name=None, change_type=None, change_id=None, jobID=None):
    result = {"output": {}, "jobID": jobID}
    switch_change(workdir, change_type, change_id, result)
    get_author(workdir, result)
    get_branch(workdir, result)
    if not config:
        config = get_config(workdir)
        if not config:
            result['output']["configuration file"] = {"exit_code": 1,"result": "ci.yaml file cannot be found"}
            update_database(result)
            return
    printNotication("Before Run Scripts:")
    runEvents(config, workdir, result, "beforeRun")
    printNotication("Test Scripts")
    if "tasks" in config.keys():
        output = handleRuns(config['tasks'], workdir)
        result["output"].update(output)

    printNotication("After Run Scripts:")
    runEvents(config, workdir, result, "afterRun")
    update_database(result)
