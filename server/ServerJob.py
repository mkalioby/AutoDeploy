import socket,threading,subprocess,os,base64,xml.dom.minidom
def perpareJobStatusMessage(req,status):
        st = """<job id="%s" owner="%s" status="%s"/>""" % (req["JobID"],req["Owner"], status)
#        print st
        return st
