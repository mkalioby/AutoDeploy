import socket,threading,subprocess,os,base64,xml.dom.minidom
import Common
EOM=Common.EOM
def sendData(clientsock,message):
	global EOM
#	print message+EOM
	if type(message) == type('a'):
		message = message.encode("utf8")
	clientsock.send(message+EOM.encode("utf8"))
	
def sendResult(clientsock):
	folder='result/'
	list = os.listdir(folder)
	import base64
	for file in list:
		path=folder+file
		if not os.path.isfile(path):
			continue
		base64.encode(open(path),open(path+'64','w'))
		f=open(path+'64','rb')
		e = f.read()
		print("'" + e + "'")
#		print base64.decodestring(e)
		clientsock.send(e)		
		f.close()
		run ('rm ' + path + '64')
import socket,threading,subprocess,os,base64,xml.dom.minidom		
def generateResponse(msg,outputList):
	doc = xml.dom.minidom.parseString(msg)
	job=doc.getElementsByTagName("job")[0]
	id=job.getAttribute("id")
	owner=job.getAttribute("owner")
	f= '<job id="' + id + '" owner="' + owner + '">'
	previousPath=""
	numOutputs = 0
	for file in outputList:
		if not os.path.isfile(file):
			continue
		numOutputs += 1
		parts= file.split("/")
		path="/".join(parts[:-1])
		out=open(file+'.64','w')
		base64.encode(open(file,'r'),out)
		out.flush()
		out.close()
		out=open(file+'.64','r')
		encoded=out.read().strip()
		out.close()
		if (path != previousPath):
			if (previousPath !=""):	f+="</folder>"
			f += '\t<folder path="' + path  + '">\n'
		f += '\t\t<output filename="'+parts[-1]+'">'+encoded +'</output>\n'
	if numOutputs > 0:
		f+='</folder>\n'
	f+='</job>'
	return f
