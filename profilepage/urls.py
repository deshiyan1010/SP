from django.urls import path
from . import views

app_name = "profilepage"

urlpatterns = [
    path('profilepage/',views.profilepage,name='profilepage'),
    path('<operation>-<current_user>-<other_user>/',views.friendship_operation,name='friendship_operation'),
    path('project/<operation>-<username>-<project_id>/',views.projectmember,name='projectmember'),
    path('update_info/',views.changeprofileinfo,name='changeprofileinfo'),
]
