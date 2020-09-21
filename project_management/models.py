from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

class ProjectCreation(models.Model):
    title = models.CharField(max_length=264,unique=True)
    team_lead = models.ForeignKey(User,on_delete=models.CASCADE,default='',null=True,blank=True)
    project_file = models.FileField(upload_to='project_management/',blank=True)
    tags = TaggableManager(blank=True)
    published = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ProjectInductionRequest(models.Model):
    
    user = models.ForeignKey(User,on_delete=models.CASCADE,)
    project = models.ForeignKey(ProjectCreation,on_delete=models.CASCADE)
    description = models.TextField(max_length=1024)
    resume_file = models.FileField(upload_to='project_management/',blank=True)
    applied_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class ProjectMembersManager(models.Manager):

    def add_member(self,super_member,member,project_id):
        request_entry = ProjectInductionRequest.objects.get(project__id=project_id, user=member)
        ProjectInductionRequest.objects.get(project__id=project_id, user=member).delete()
        entry = ProjectMembers(member=request_entry.user,project=request_entry.project,accepted_by=super_member,requested_time=request_entry.applied_time) #User.objects.get(username='deshiyan')
        entry.save()

    def remove_member(self,member,project_id):
        ProjectMembers.objects.get(member=member,project__id=project_id).delete()        

    def reject_member(self,member,project_id):
        ProjectInductionRequest.objects.get(project__id=project_id, user=member).delete()

class ProjectMembers(models.Model):

    member = models.ForeignKey(User,on_delete=models.CASCADE)
    accepted_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='accepted_by')
    project = models.ForeignKey(ProjectCreation,on_delete=models.CASCADE)
    requested_time = models.DateTimeField(blank=True)
    accepted_time = models.DateTimeField(auto_now_add=True)
    
    objects = models.Manager()
    func = ProjectMembersManager()

    def __str__(self):
        return self.member.username
    
