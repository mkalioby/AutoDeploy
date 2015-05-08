import socket,threading,subprocess,os,base64,xml.dom.minidom
def getOutputList(message):
	doc = xml.dom.minidom.parseString(message)
	folders=doc.getElementsByTagName("folder")
	outputFilesList=[]
	for folder in folders:
			path=folder.getAttribute("path")
			#print 'In folder:' , path
			if (not os.path.exists(path)): os.makedirs(path)
			outputs = folder.getElementsByTagName("output")
			if (outputs!=None):
				for output in outputs:
					filename= output.getAttribute('filename')
					outputFilesList.append(path+'/' +filename)
	return outputFilesList

def parseRequest(message):
	doc = xml.dom.minidom.parseString(message)
	Job=doc.getElementsByTagName('job')
	owner=Job[0].getAttribute('owner')
	JobID=Job[0].getAttribute('id')
	requestType=Job[0].getAttribute('type')
	sec=Job[0].getAttribute('sec')
	return {'JobID':JobID,"Owner":owner,"requestType":requestType,"sec":sec}
	
def parseJob(message):
	import os
	allinputs=[]
	alloutputs=[]
	doc = xml.dom.minidom.parseString(message)
	Job=doc.getElementsByTagName('job')
	owner=Job[0].getAttribute('owner')
	JobID=Job[0].getAttribute('id')
	requestType=Job[0].getAttribute('type')
	print 'Recieved New Job' + JobID + '.....'
	command = base64.decodestring(doc.getElementsByTagName("command")[0].firstChild.nodeValue)
	#print 'command:' + command
	folders=doc.getElementsByTagName("folder")
	if folders !=None:
		for folder in folders:
			path=folder.getAttribute("path")
		#print 'In folder:' , path
			if (not os.path.exists(path)): 
				os.makedirs(path)
				run ("chmod 777 "  + path)
			inputs = folder.getElementsByTagName("input")
			if (inputs!=None):
				for input in inputs:
					filename= input.getAttribute('filename')
					text=input.firstChild.nodeValue
					content=base64.decodestring(text)
					#print "file '" , filename + "'\n" + content 
					allinputs.append(path+'/' +filename)
					file= open(path+"/"+filename,'w')
					file.write(content)
					file.flush()
					file.close()
			outputs=folder.getElementsByTagName("output")
			if (outputs!=None):
				for out in outputs:
					filename= out.getAttribute('filename')
					alloutputs.append(path+'/'+filename)	
	global JOBS
	#JOBS[JobID]=[owner,'R']	
	#print "output files: " , str(outputFilesList)
	return {"JobID":JobID,"Owner":owner, "command":command,"inputs":allinputs,"outputs":alloutputs}
#	return [command,outputFilesList,id]
def run(excuter,id=None):

        PIPE=subprocess.PIPE
        p=subprocess.Popen(excuter,stdout=PIPE,stderr=PIPE,shell=True)
        (stderr,stdout)=   p.communicate()
        st=stderr
        if (id!=None):
                 f = open("/tmp/"+id+".err",'w')
                 f.write(st)
                 f.flush()
                 f.close()
                 f = open("/tmp/"+id+".out",'w')
                 f.write(stdout)
                 f.flush()
                 f.close()

        return stderr
#       if len(st)>0:
               # f = open("/tmp/ToolService.err",'w')
               # f.write(st)
               # f.flush()
#                f.close()
 #               return "Childerr:", st

  #      else:
        return stdout

