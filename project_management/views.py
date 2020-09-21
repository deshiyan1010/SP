from django.shortcuts import render
from project_management.models import *
from . import forms 

from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from taggit.models import Tag

# Create your views here.
def project_creation(request):

    projects = ProjectCreation.objects.order_by('-published')
    common_tags = ProjectCreation.tags.most_common()[:4]
    form = forms.ProjectCreationForm()
    if request.method == 'POST':
        form = forms.ProjectCreationForm(request.POST,request.FILES)

        if form.is_valid():
            newproject = form.save(commit=False)
            newproject.team_lead = request.user
            newproject.save()
            form.save_m2m()
            lead = ProjectMembers(member=request.user,accepted_by=request.user,project=newproject)
            lead.save()
            return HttpResponseRedirect(reverse('project_management:project_creation'))
    
    context = {
        'projects':projects,
        'common_tags':common_tags,
        'form':form,
    }
    return render(request, 'project_management/project_form.html', context)

def project_application(request,project_id):


    form = forms.ProjectInductionRequestForm()
    if request.method == 'POST':
        form = forms.ProjectInductionRequestForm(request.POST,request.FILES)

        if form.is_valid():
            print(project_id,"\n"*3)
            newapplicant = form.save(commit=False)
            newapplicant.user = request.user
            newapplicant.project = ProjectCreation.objects.get(id=project_id)
            newapplicant.save()
            return HttpResponseRedirect(reverse('networking:project_view',args=(project_id,)))
    
    context = {

        'form':form,
    }
    return render(request, 'project_management/project_applicant_form.html', context)
