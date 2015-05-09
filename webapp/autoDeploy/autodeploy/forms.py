__author__ = 'mohamed'
from django import forms
import models
repo_type=[('git','git')]
class addProjectsForm(forms.ModelForm):
    working_dir=forms.CharField(label="Working Directory")
    repo_type=forms.ChoiceField(choices=repo_type,label="Repo Type")
    class Meta:
        model= models.Project
        fields=("name","repo","working_dir","repo_type")
class addServerForm(forms.ModelForm):
    class Meta:
        model=models.Server
        fields=('name','dns','port')