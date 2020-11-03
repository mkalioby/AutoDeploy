import socket, threading, subprocess, os, base64, xml.dom.minidom
import config


def parseRequest(message):
    doc = xml.dom.minidom.parseString(message)
    Job = doc.getElementsByTagName('job')
    owner = Job[0].getAttribute('owner')
    requestType = Job[0].getAttribute('type')
    sec = Job[0].getAttribute('sec')
    scm = Job[0].getAttribute('scm')
    return {"Owner": owner, "requestType": requestType, "sec": sec,"scm":scm}


def getValue(node, name):
    res = node.getElementsByTagName(name)[0].firstChild.nodeValue
    if res == "None":
        return None
    return res


def parseCloneJob(message):
    #print message
    params = {}
    optionsDict = {}
    doc = xml.dom.minidom.parseString(message)
    Job = doc.getElementsByTagName('job')[0]
    repo= getValue(Job, 'repo')
    key= getValue(Job, 'sshkey')
    scm=Job.getAttribute("scm")
    workdir= getValue(Job, 'workdir')

    requestType = Job.getAttribute('type')
    owner = Job.getAttribute('owner')
    """options = (Job.getElementsByTagName('option'))
    for option in options:
        name = option.getAttribute("name")
        optionsDict[name] = option.firstChild.nodeValue
    """
    print('Recieved New Job from  ' + owner + '.....')
    params = {"repo":repo, "key": key,"workdir": workdir,"owner": owner,  "requestType": requestType,
              "scm":scm,"options": optionsDict}
    return params

def parsePullJob(message):
    return parseListTagsJob(message)

def parseListTagsJob(message):
    params = {}
    optionsDict = {}
    doc = xml.dom.minidom.parseString(message)
    Job = doc.getElementsByTagName('job')[0]
    key= getValue(Job, 'sshkey')
    scm=Job.getAttribute("scm")
    workdir= getValue(Job, 'workdir')

    requestType = Job.getAttribute('type')
    owner = Job.getAttribute('owner')
    """options = (Job.getElementsByTagName('option'))
    for option in options:
        name = option.getAttribute("name")
        optionsDict[name] = option.firstChild.nodeValue
    """
    print('Recieved New Job from  ' + owner + '.....')
    params = {"workdir": workdir,"owner": owner,  "requestType": requestType,"key":key,
              "scm":scm,"options": optionsDict}
    return params


def parseListBranchsJob(message):
    params = {}
    optionsDict = {}
    doc = xml.dom.minidom.parseString(message)
    Job = doc.getElementsByTagName('job')[0]
    scm=Job.getAttribute("scm")
    workdir= getValue(Job, 'workdir')

    requestType = Job.getAttribute('type')
    owner = Job.getAttribute('owner')
    """options = (Job.getElementsByTagName('option'))
    for option in options:
        name = option.getAttribute("name")
        optionsDict[name] = option.firstChild.nodeValue
    """
    print('Recieved New Job from  ' + owner + '.....')
    params = {"workdir": workdir,"owner": owner,  "requestType": requestType,"scm":scm,"options": optionsDict}
    return params


def parseSwitchTagJob(message):
    params = {}
    optionsDict = {}
    doc = xml.dom.minidom.parseString(message)
    Job = doc.getElementsByTagName('job')[0]
    scm=Job.getAttribute("scm")
    workdir= getValue(Job, 'workdir')
    tag=getValue(Job,"tag")
    requestType = Job.getAttribute('type')
    owner = Job.getAttribute('owner')
    """options = (Job.getElementsByTagName('option'))
    for option in options:
        name = option.getAttribute("name")
        optionsDict[name] = option.firstChild.nodeValue
    """
    print('Recieved New Job from  ' + owner + '.....')
    params = {"workdir": workdir,"owner": owner,  "requestType": requestType,"tag":tag,
              "scm":scm,"options": optionsDict}
    return params


def parseDeployJob(message):
    params = {}
    optionsDict = {}
    doc = xml.dom.minidom.parseString(message)
    Job = doc.getElementsByTagName('job')[0]
    scm=Job.getAttribute("scm")
    workdir= getValue(Job, 'workdir')
    configFile=getValue(Job,"configFile")
    requestType = Job.getAttribute('type')
    owner = Job.getAttribute('owner')
    fileBase64=getValue(Job,"file")
    if not os.path.exists(os.path.dirname(configFile)):
        os.makedirs(os.path.dirname(configFile))
    open(configFile,"w").write(base64.decodestring(fileBase64))

    """options = (Job.getElementsByTagName('option'))
    for option in options:
        name = option.getAttribute("name")
        optionsDict[name] = option.firstChild.nodeValue
    """
    print('Recieved New Job from  ' + owner + '.....')
    params = {"workdir": workdir,"owner": owner,  "requestType": requestType,"configFile":configFile,
              "scm":scm,"options": optionsDict}
    return params

def parseIntegrateJob(message):
    params = {}
    optionsDict = {}
    doc = xml.dom.minidom.parseString(message)
    Job = doc.getElementsByTagName('job')[0]
    scm=Job.getAttribute("scm")
    project_name=Job.getAttribute("project_name")
    change_type=Job.getAttribute("change_type")
    change_id=Job.getAttribute("change_id")
    workdir= getValue(Job, 'workdir')
    jobID=getValue(Job,"jobID")
    configFile=getValue(Job,"configFile")
    requestType = Job.getAttribute('type')
    owner = Job.getAttribute('owner')
    art_dir = doc.getElementsByTagName('art_dir')[0].childNodes[0].nodeValue
    if configFile:
        fileBase64=getValue(Job,"file")
        if not os.path.exists(os.path.dirname(configFile)):
            os.makedirs(os.path.dirname(configFile))
        open(configFile,"w").write(fileBase64)
    print('Recieved New Job from  ' + owner + '.....')
    params = {"jobID": jobID, "workdir": workdir, "art_dir": art_dir, "owner": owner,  "requestType": requestType, "configFile": configFile,
              "scm": scm, "options": optionsDict, "project_name": project_name, "change_type": change_type, "change_id": change_id}
    return params

def parseGetCommitsJob(message):
    optionsDict={}
    doc = xml.dom.minidom.parseString(message)
    Job = doc.getElementsByTagName('job')[0]
    scm=Job.getAttribute("scm")
    workdir= getValue(Job, 'workdir')
    requestType = Job.getAttribute('type')
    key= getValue(Job, 'sshkey')
    owner = Job.getAttribute('owner')
    options = (Job.getElementsByTagName('option'))
    for option in options:
        name = option.getAttribute("name")
        optionsDict[name] = option.firstChild.nodeValue
    params = {"workdir": workdir, "owner": owner, "requestType": requestType, "key": key,
              "scm": scm, "options": optionsDict}
    return params


def parseSwitchCommitJob(message):
    params = {}
    optionsDict = {}
    doc = xml.dom.minidom.parseString(message)
    Job = doc.getElementsByTagName('job')[0]
    scm=Job.getAttribute("scm")
    workdir= getValue(Job, 'workdir')
    commit=getValue(Job,"commit")
    requestType = Job.getAttribute('type')
    owner = Job.getAttribute('owner')
    """options = (Job.getElementsByTagName('option'))
    for option in options:
        name = option.getAttribute("name")
        optionsDict[name] = option.firstChild.nodeValue
    """
    print('Recieved New Job from  ' + owner + '.....')
    params = {"workdir": workdir,"owner": owner,  "requestType": requestType,"commit":commit,
              "scm":scm,"options": optionsDict}
    return params


def parseGetCommitDiff(message):
    return parseSwitchCommitJob(message)

def parseGetChangeLog(message):
    params = {}
    optionsDict = {}
    doc = xml.dom.minidom.parseString(message)
    Job = doc.getElementsByTagName('job')[0]
    scm = Job.getAttribute("scm")
    workdir = getValue(Job, 'workdir')

    requestType = Job.getAttribute('type')
    owner = Job.getAttribute('owner')
    options = (Job.getElementsByTagName('option'))
    for option in options:
        name = option.getAttribute("name")
        optionsDict[name] = option.firstChild.nodeValue

    print('Recieved New Job from  ' + owner + '.....')
    params = {"workdir": workdir, "owner": owner, "requestType": requestType,
              "scm": scm, "options": optionsDict}
    return params