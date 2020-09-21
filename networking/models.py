from django.db import models
from django.contrib.auth.models import User

class Friends(models.Model):
    user = models.ManyToManyField(User,related_name='myfriend')
    current_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='current_user',null=True)
    
    @classmethod
    def add_friend(cls,current_user,new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.user.add(new_friend)

    @classmethod
    def remove_friend(cls,current_user,new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.user.remove(new_friend)   


# class Chat(models.Model):
#     users = models.ForeignKey(Friends,on_delete=models.CASCADE,)
#     cha
