import subprocess
EOM = "\n\n###"



def run(executer,raiseError=True,id=None,wait=True):
    PIPE = subprocess.PIPE
    p = subprocess.Popen(executer, stdout=PIPE, stderr=PIPE, shell=True)
    if wait:
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

        if len(stderr) > 0:
            if raiseError:
                raise Exception(stderr[5:])
            return "ERR:"+stderr
        return stdout
    else:
        return p
