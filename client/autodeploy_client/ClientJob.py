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


def createGetBranchs(workdir, scm, owner,options=None):
    sec = base64.encodestring(importKey().encrypt(owner + scm + "LIST-BRNACHS", "")[0])
    f = '<job  owner="%s" type="%s" sec="%s" scm="%s">\n' % (owner, "LIST-BRNACHS", sec, scm)
    f += '<workdir>%s</workdir>' % workdir

    if options:
        f += '<options>'
        for option in options.keys():
            f += "<option name='%s'>%s</option>" % (option, options[option])

        f += "</options>"
    f += '</job>'
    return f


# Provide id, owner and command as string
# inputsFiles as List of file path
def createCloneMessage(owner, repo, workdir, key, scm, options=None):
    sec=base64.encodestring(importKey().encrypt(owner+scm+"CLONE","")[0])
    f = '<job  owner="%s" type="%s" sec="%s" scm="%s">\n'%( owner,"CLONE",sec,scm)
    f += '<workdir>%s</workdir>'%workdir
    f += '<repo>%s</repo>'%repo
    f += '<sshkey>%s</sshkey>'%key
    if options:
        f += '<options>'
        for option in options.keys():
            f += "<option name='%s'>%s</option>" % (option, options[option])

        f += "</options>"
    f += '</job>'


    return f


def createPullMessage(owner,workdir,key, scm, options=None):
    sec=base64.encodestring(importKey().encrypt(owner+scm+"PULL","")[0])
    f = '<job  owner="%s" type="%s" sec="%s" scm="%s">\n'%( owner,"PULL",sec,scm)
    f += '<workdir>%s</workdir>'%workdir
    #f += '<repo>%s</repo>'%repo
    f += '<sshkey>%s</sshkey>'%key
    if options:
        f += '<options>'
        for option in options.keys():
            f += "<option name='%s'>%s</option>" % (option, options[option])

        f += "</options>"
    f += '</job>'
    return f

def createListTagsMessage(owner, workdir,key, scm, options=None):
    sec=base64.encodestring(importKey().encrypt(owner+scm+"LIST-TAGS","")[0])
    f = '<job  owner="%s" type="%s" sec="%s" scm="%s">\n'%( owner,"LIST-TAGS",sec,scm)
    f += '<workdir>%s</workdir>'%workdir
    f += '<sshkey>%s</sshkey>'%key

    if options:
        f += '<options>'
        for option in options.keys():
            f += "<option name='%s'>%s</option>" % (option, options[option])

        f += "</options>"
    f += '</job>'
    return f

def createSwitchTagMessage(owner, workdir, scm, tag, options=None):
    sec=base64.encodestring(importKey().encrypt(owner+scm+"SWITCH-TAG","")[0])
    f = '<job owner="%s" type="%s" sec="%s" scm="%s">\n'%( owner,"SWITCH-TAG",sec,scm)
    f += '<workdir>%s</workdir>'%workdir
    f += '<tag>%s</tag>'%tag

    if options:
        f += '<options>'
        for option in options.keys():
            f += "<option name='%s'>%s</option>" % (option, options[option])

        f += "</options>"
    f += '</job>'
    return f

def createDeployMessage(owner, workdir, scm, configFile, update_type, update_version, key, options=None):
    sec=base64.encodestring(importKey().encrypt(owner+scm+"DEPLOY","")[0])
    f = '<job owner="%s" type="%s" sec="%s" scm="%s">\n'%( owner,"DEPLOY",sec,scm)
    f += '<workdir>%s</workdir>'%workdir
    f += '<configFile>%s</configFile>'%configFile
    f += '<update_type>%s</update_type>'%update_type
    f += '<update_version>%s</update_version>'%update_version
    conf=open(str(configFile)).read()
    f += '<file>%s</file>'%(base64.encodestring(conf))
    f += '<sshkey>%s</sshkey>' % key
    if options:
        f += '<options>'
        for option in options.keys():
            f += "<option name='%s'>%s</option>" % (option, options[option])

        f += "</options>"
    f += '</job>'
    return f

def createListCommitsMessage(owner, workdir, key, scm, options=None):
    sec=base64.encodestring(importKey().encrypt(owner+scm+"LIST-COMMITS","")[0])
    f = '<job  owner="%s" type="%s" sec="%s" scm="%s">\n'%( owner,"LIST-COMMITS",sec,scm)
    f += '<workdir>%s</workdir>'%workdir
    f += '<sshkey>%s</sshkey>'%key

    if options:
        f += '<options>'
        for option in options.keys():
            f += "<option name='%s'>%s</option>" % (option, options[option])

        f += "</options>"
    f += '</job>'
    return f


def createSwitchCommitMessage(owner, workdir, commit,scm, options=None):
    sec=base64.encodestring(importKey().encrypt(owner+scm+"SWITCH-COMMIT","")[0])
    f = '<job owner="%s" type="%s" sec="%s" scm="%s">\n'%( owner,"SWITCH-COMMIT",sec,scm)
    f += '<workdir>%s</workdir>'%workdir
    f += '<commit>%s</commit>'%commit

    if options:
        f += '<options>'
        for option in options.keys():
            f += "<option name='%s'>%s</option>" % (option, options[option])

        f += "</options>"
    f += '</job>'
    return f

def creategetCommitsDiffMessage(owner, workdir, commit, scm,options=None):
    print owner,workdir,commit,scm
    sec=base64.encodestring(importKey().encrypt(owner+str(scm)+"DIFF-COMMIT","")[0])
    #sec=base64.encodestring(importKey().encrypt(owner+scm+"DIFF-COMMIT","")[0])
    f = '<job owner="%s" type="%s" sec="%s" scm="%s">\n'%( owner,"DIFF-COMMIT",sec,scm)
    f += '<workdir>%s</workdir>'%workdir
    f += '<commit>%s</commit>'%commit

    if options:
        f += '<options>'
        for option in options.keys():
            f += "<option name='%s'>%s</option>" % (option, options[option])

        f += "</options>"
    f += '</job>'
    return f