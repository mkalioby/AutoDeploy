__author__ = 'mohamed'
from django import forms
import models
repo_type=[('git','git')]
class addProjectsForm(forms.ModelForm):
    working_dir=forms.CharField(label="Working Directory")
    repo_type=forms.ChoiceField(choices=repo_type,label="Repo Type")
    class Meta:
        model= models.Project
        fields=("name","repo","repo_link","working_dir","repo_type","sshKey","deployment_link")
class addServerForm(forms.ModelForm):
    class Meta:
        model=models.Server
        fields=('name','dns','port')
class addSSHKeyForm(forms.ModelForm):
    class Meta:
        model=models.sshKey
        fields=('name','key')

class CloneForm(forms.Form):
    server=forms.ModelChoiceField(queryset=models.Server.objects.all(),label="Server")


