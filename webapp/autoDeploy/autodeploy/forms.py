__author__ = 'mohamed'
from django import forms
import models
repo_type=[('git','git')]
class addProjects(forms.ModelForm):
    working_dir=forms.CharField(label="Working Directory")
    repo_type=forms.ChoiceField(choices=repo_type,label="Repo Type")
    class Meta:
        model= models.Project
        fields=("name","repo","working_dir","repo_type")
