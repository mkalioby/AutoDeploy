import subprocess
EOM = "\n\n###"



def run(executer, id=None,exitcode=False,):
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

    if len(stderr) > 0 and b"fatal" in stderr:
        return b"ERR:"+stderr
    if stdout=="": return "Done"
    if exitcode: return str(p.returncode)
    return stdout
