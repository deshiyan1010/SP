from django import forms
from project_management.models import *

class ProjectCreationForm(forms.ModelForm):
    
    class Meta:
        model = ProjectCreation
        fields = [
            'title',
            'project_file',
            'tags',
        ]

class ProjectInductionRequestForm(forms.ModelForm):

    class Meta:
        model = ProjectInductionRequest
        fields = [
            'description',
            'resume_file',
        ]