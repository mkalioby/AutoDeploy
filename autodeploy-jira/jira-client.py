__author__ = 'mohamed'

from jira.client import JIRA

class jiraClient():
    server=""
    username=""
    password=""

    def __init__(self,server,username,password):
        self.server=server
        self.username=username
        self.password=password

    def getProjects(self):
        options = {'server': self.server}

        jira = JIRA(options,basic_auth=(self.username, self.password))    # a username/password tuple

        # Get the mutable application properties for this server (requires jira-system-administrators permission)
        props = jira.application_properties()
        projects = jira.projects()
        return projects
    def getProjectKeys(self):
        return [project.key for project in self.getProjects()]

if __name__=="__main__":
    c=jiraClient("http://shgp.kfshrc.edu.sa/jira",'mkalioby','wanted85')
    print(c.getProjectKeys())