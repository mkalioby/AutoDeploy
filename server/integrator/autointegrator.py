__author__ = 'mohamed'

import subprocess
import json
import config as configFile
import requests
import os
from jose import jwt
EOM = "\n\n###"
debug = False
slient = False


class autointegrator():
    def __init__(self, config, workdir, jobID, change_type, change_id, art_dir, project_name):
        self.config = config
        self.workdir = workdir
        self.jobID = jobID
        self.change_type = change_id
        self.change_id = change_type
        self.art_dir = art_dir
        self.project_name = project_name
        self.result = {"output": {}, "jobID": self.jobID}

    def encrypt_result(self):
        file = open(configFile.publicKey, 'r')
        st = "".join(file.readlines())
        return jwt.encode(self.result, st, algorithm="RS256")

    def update_database(self, isRunning):
        self.result['isRunning'] = isRunning
        client_url = configFile.client_url + "api/ris"
        try:
            serverStatus = requests.get(client_url).status_code
            if serverStatus == 200:
                encoded_token = self.encrypt_result()
                r = requests.post(client_url,
                                  data=json.dumps(encoded_token))  # TODO : If the client is die what to do ?
                if r.status_code == 200:
                    if not slient: print("Sent : ", True)
                else:
                    if not slient: print("Sent : ", False, "Code : ", r.status_code)
        except Exception as exp:
            import traceback
            if not slient: print("Sent : ", False, " ", exp)
            if not slient: print(traceback.format_exc())

    def artifactor_dir(self):
        dir = self.art_dir + '/' + self.project_name + '/' + self.jobID + '/'
        if not os.path.exists(dir):
            os.makedirs(os.path.join(dir))
        return "export artifact_dir='" + dir + "'; "

    def run(self, executer, id=None, interpreter="/bin/bash"):
        PIPE = subprocess.PIPE
        cmd = self.artifactor_dir()
        newExecuter = cmd + "export work_dir='" + self.workdir + "'; cd $work_dir ;" + executer
        print("Command => ", newExecuter)
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
        if p.returncode in [0, '0']:
            if stdout.decode('utf-8') in ['', None, ' ']:
                result = stderr.decode('utf-8')
            else:
                result = stdout.decode('utf-8')
        else:
            if stderr.decode('utf-8') in ['', None, ' ']:
                result = stdout.decode('utf-8')
            else:
                result = stderr.decode('utf-8')
        return {"exit_code": exit_code, "result": result}

    def printNotication(self, message):
        if slient: return
        print("=" * 10)
        print(message)
        print("=" * 10)

    def runEvents(self, event):
        if not "events" in self.config:
            print("Nothing in events section")
        if event in self.config["events"].keys():
            for script in self.config["events"][event]:
                if not "location" in script.keys():
                    print("location event not exists")
                    pass
                cmd = script["location"]
                if "interpreter" in script.keys(): cmd = "%s %s" % (script["interpreter"], cmd)
                if "run-as" in script.keys() and not script["run-as"] == "root": cmd = "su %s -c %s" % (
                    script["run-as"], cmd)
                if not slient: print("Running")
                run_res = self.run(cmd)
                if not slient: print("Done")
                if run_res['exit_code'] not in [0, '0']:
                    self.result['output'][cmd] = run_res
                if event == 'afterRun' and run_res['result'].find("Coverage: ") not in [-1, '-1']:
                    self.result["output"]['Coverage'] = run_res['result'].split(": ")[1].replace("\n", "")
        self.update_database(True)

    def handleRuns(self, tasks):
        result = {}
        for task in tasks:
            cmd = "%s" % task["location"]
            print("TASK : ", cmd)
            task_result = self.run(cmd, interpreter=task.get('interpreter', '/bin/bash'))
            print("RESULT : ", task_result['exit_code'])
            result[cmd] = task_result
            self.result["output"].update({cmd:task_result})
            self.update_database(True)
        return result

    def switch_change(self):
        if self.change_type == 'tag':
            switch_command = "git checkout tags/%s" % (self.change_id)
        else:
            switch_command = "git reset --hard % s" % (self.change_id)
        run_res = self.run(switch_command)
        if run_res['exit_code'] not in [0, '0']:
            self.result['output'][switch_command] = run_res

    def get_author(self):
        author_command = 'git log -n1 --pretty=format:"%H,,%h,,%an,,%ae,,%ar,,%s,,%cd" | cat -'
        author = self.run(author_command)
        if author['exit_code'] in [0, '0']:
            author_info = author['result'].split(",,")[2:4]
            self.result['output']['author_name'] = author_info[0]
            self.result['output']['author_email'] = author_info[1]
        else:
            self.result['output'][author_command] = author

    def get_branch(self):
        branch_command = 'git rev-parse --abbrev-ref HEAD | cat -'
        branch = self.run(branch_command)
        if branch['exit_code'] in [0, '0']:
            self.result['output']['branch'] = branch['result'].replace("\n", "")
        else:
            self.result['output'][branch_command] = branch

    def get_config(self):
        import yaml
        import os
        yaml_file = None
        for file in os.listdir(self.workdir):
            if file.endswith("ci.yaml"):
                yaml_file = yaml.safe_load(open(os.path.join(self.workdir, file)))
        return yaml_file

    def runTest(self):
        self.switch_change()
        self.get_author()
        self.get_branch()
        self.update_database(True)
        if not self.config:
            self.config = self.get_config()
            if not self.config:
                self.result['output']["configuration file"] = {"exit_code": 1, "result": "ci.yaml file cannot be found"}
                self.update_database(False)
                return
        self.printNotication("Before Run Scripts:")
        self.runEvents("beforeRun")
        self.printNotication("Test Scripts")
        output = None
        if "tasks" in self.config.keys():
            output = self.handleRuns(self.config['tasks'])

        success = True
        for item in output.values():
            if item['exit_code'] not in [0, '0']:
                success = False
                break
        if success:
            self.printNotication("After Success Scripts:")
            self.runEvents("afterSuccess")
        else:
            self.printNotication("After Fail Scripts:")
            self.runEvents("afterFail")

        self.printNotication("After Run Scripts:")
        self.runEvents("afterRun")
        self.update_database(False)