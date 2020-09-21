from django.db import models
from reg_sign_in_out.models import User

class Posts(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    time = models.DateTimeField(auto_now_add=True)
    post_text = models.CharField(max_length=1024)
    post_pic = models.ImageField(upload_to='post_pic',blank=True)
    
    def __str__(self):
        return self.post_text
    
class Comment(models.Model):
    post = models.ForeignKey(Posts,on_delete=models.CASCADE,)
    userid = models.ForeignKey(User,on_delete=models.CASCADE,default='')
    comment = models.CharField(max_length=256)
    time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return '{}-{}'.format(self.post.id,self.userid)
    
class Like(models.Model):
    post = models.ForeignKey(Posts,on_delete=models.CASCADE,)
    liked_by = models.ForeignKey(User,on_delete=models.CASCADE,)

    def __str__(self):
        return self.post.post_text
    


# class SubComment(models.Model):
#     post = models.ForeignKey(Posts,on_delete=models.CASCADE,)
#     userid = models.ForeignKey(User,on_delete=models.CASCADE,default='')
#     comment = models.CharField(max_length=256)
#     time = models.DateTimeField(auto_now_add=True)
#     commentx = models.ForeignKey(Comment,on_delete=models.CASCADE)
    
#     def __str__(self):
#         return '{}-{}'.format(self.post,self.userid)