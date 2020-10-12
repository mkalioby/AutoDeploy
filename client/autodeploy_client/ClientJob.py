import socket, base64, time, sys, subprocess
import os
import hashlib
from Crypto.PublicKey import RSA
from Crypto import Random

def importKey():
        mainPath=os.path.dirname(os.path.abspath( __file__ ))
        file=open(mainPath + "/my",'r')
        st = "".join(file.readlines())
        key = RSA.importKey(st)
        #print "KEY Opened" , key
        return key

def sign(owner,scm,msg):
    b = (owner + scm + msg).encode('utf-8')
    key = (importKey().encrypt(b, "")[0])
    return base64.encodebytes(key).decode("utf8")


def createGetBranchs(workdir, scm, owner,options=None):
    sec= sign(owner,scm,"LIST-BRNACHS")
    f = '<job  owner="%s" type="%s" sec="%s" scm="%s">\n' % (owner, "LIST-BRNACHS", sec, scm)
    f += '<workdir>%s</workdir>' % workdir

    if options:
        f += '<options>'
        for option in list(options.keys()):
            f += "<option name='%s'>%s</option>" % (option, options[option])

        f += "</options>"
    f += '</job>'
    return f


# Provide id, owner and command as string
# inputsFiles as List of file path
def createCloneMessage(owner, repo, workdir, key, scm, options=None):
    sec = sign(owner, scm, "CLONE")
    f = '<job  owner="%s" type="%s" sec="%s" scm="%s">\n'%( owner,"CLONE",sec,scm)
    f += '<workdir>%s</workdir>'%workdir
    f += '<repo>%s</repo>'%repo
    f += '<sshkey>%s</sshkey>'%key
    if options:
        f += '<options>'
        for option in list(options.keys()):
            f += "<option name='%s'>%s</option>" % (option, options[option])

        f += "</options>"
    f += '</job>'


    return f


def createPullMessage(owner,workdir,key, scm, options=None):
    sec = sign(owner, scm, "PULL")
    f = '<job  owner="%s" type="%s" sec="%s" scm="%s">\n'%( owner,"PULL",sec,scm)
    f += '<workdir>%s</workdir>'%workdir
    #f += '<repo>%s</repo>'%repo
    f += '<sshkey>%s</sshkey>'%key
    if options:
        f += '<options>'
        for option in list(options.keys()):
            f += "<option name='%s'>%s</option>" % (option, options[option])

        f += "</options>"
    f += '</job>'
    return f

def createListTagsMessage(owner, workdir,key, scm, options=None):
    sec = sign(owner, scm, "LIST-TAGS")
    f = '<job  owner="%s" type="%s" sec="%s" scm="%s">\n'%( owner,"LIST-TAGS",sec,scm)
    f += '<workdir>%s</workdir>'%workdir
    f += '<sshkey>%s</sshkey>'%key

    if options:
        f += '<options>'
        for option in list(options.keys()):
            f += "<option name='%s'>%s</option>" % (option, options[option])

        f += "</options>"
    f += '</job>'
    return f

def createSwitchTagMessage(owner, workdir, scm, tag, options=None):
    sec = sign(owner, scm, "SWITCH-TAG")
    f = '<job owner="%s" type="%s" sec="%s" scm="%s">\n'%( owner,"SWITCH-TAG",sec,scm)
    f += '<workdir>%s</workdir>'%workdir
    f += '<tag>%s</tag>'%tag

    if options:
        f += '<options>'
        for option in list(options.keys()):
            f += "<option name='%s'>%s</option>" % (option, options[option])

        f += "</options>"
    f += '</job>'
    return f

def createDeployMessage(owner, workdir, scm, configFile, options=None):
    sec = sign(owner, scm, "DEPLOY")
    f = '<job owner="%s" type="%s" sec="%s" scm="%s">\n'%( owner,"DEPLOY",sec,scm)
    f += '<workdir>%s</workdir>'%workdir
    f += '<configFile>%s</configFile>'%configFile
    print(configFile)
    conf=open(str(configFile)).read()
    f += '<file>%s</file>'%(base64.encodestring(conf))

    if options:
        f += '<options>'
        for option in list(options.keys()):
            f += "<option name='%s'>%s</option>" % (option, options[option])

        f += "</options>"
    f += '</job>'
    return f

def createIntegrateMessage(jobID,owner, workdir, scm, configFile, options=None):
    sec = sign(owner, scm, "INTEGRATE")
    f = '<job owner="%s" type="%s" sec="%s" scm="%s">\n'%(owner,"INTEGRATE",sec,scm)
    f += '<jobID>%s</jobID>'%jobID
    f += '<workdir>%s</workdir>'%workdir
    f += '<configFile>%s</configFile>'%str(configFile)
    conf=open(configFile).read()
    f += '<file>%s</file>'%(conf)

    if options:
        f += '<options>'
        for option in list(options.keys()):
            f += "<option name='%s'>%s</option>" % (option, options[option])

        f += "</options>"
    f += '</job>'
    return f

def createListCommitsMessage(owner, workdir, key, scm, options=None):
    sec = sign(owner, scm, "LIST-COMMITS")
    f = '<job  owner="%s" type="%s" sec="%s" scm="%s">\n'%( owner,"LIST-COMMITS",sec,scm)
    f += '<workdir>%s</workdir>'%workdir
    f += '<sshkey>%s</sshkey>'%key

    if options:
        f += '<options>'
        for option in list(options.keys()):
            f += "<option name='%s'>%s</option>" % (option, options[option])

        f += "</options>"
    f += '</job>'
    return f


def createSwitchCommitMessage(owner, workdir, commit,scm, options=None):
    sec = sign(owner, scm, "SWITCH-COMMIT")
    f = '<job owner="%s" type="%s" sec="%s" scm="%s">\n'%( owner,"SWITCH-COMMIT",sec,scm)
    f += '<workdir>%s</workdir>'%workdir
    f += '<commit>%s</commit>'%commit

    if options:
        f += '<options>'
        for option in list(options.keys()):
            f += "<option name='%s'>%s</option>" % (option, options[option])

        f += "</options>"
    f += '</job>'
    return f

def creategetCommitsDiffMessage(owner, workdir, commit, scm,options=None):
    print(owner,workdir,commit,scm)
    sec = sign(owner, scm, "DIFF-COMMIT")
    #sec=base64.encodestring(importKey().encrypt(owner+scm+"DIFF-COMMIT","")[0])
    f = '<job owner="%s" type="%s" sec="%s" scm="%s">\n'%( owner,"DIFF-COMMIT",sec,scm)
    f += '<workdir>%s</workdir>'%workdir
    f += '<commit>%s</commit>'%commit

    if options:
        f += '<options>'
        for option in list(options.keys()):
            f += "<option name='%s'>%s</option>" % (option, options[option])

        f += "</options>"
    f += '</job>'
    return f

def createGetChangeLog(owner,workdir,scm,options=None):
    sec = sign(owner, scm, "LIST-CHANGES")
    f = '<job  owner="%s" type="%s" sec="%s" scm="%s">\n' % (owner, "LIST-CHANGES", sec, scm)
    f += '<workdir>%s</workdir>' % workdir
    if options:
        f += '<options>'
        for option in list(options.keys()):
            f += "<option name='%s'>%s</option>" % (option, options[option])

        f += "</options>"
    f += '</job>'
    return f