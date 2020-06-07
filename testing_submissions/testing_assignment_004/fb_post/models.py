from django.db import models

class User(models.Model):
    name=models.CharField(max_length=100)
    profile_pic=models.TextField(blank=True,null=True)


class Post(models.Model):
    content=models.CharField(max_length=1000)
    posted_at=models.DateTimeField(auto_now=True)
    posted_by=models.ForeignKey(User,on_delete=models.CASCADE,related_name="posts")

class Comment(models.Model):
    content=models.CharField(max_length=1000)
    commented_at=models.DateTimeField(auto_now=True)
    commented_by=models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_comments")
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments")
    parent_comment = models.ForeignKey('self', null=True, blank=True, related_name='comment',on_delete=models.CASCADE)

class Reaction(models.Model):
    REACTIONS=(
        ("WOW","wow"),
        ("LIT","lit"),
        ("LOVE","love"),
        ("HAHA","haha"),
        ("THUMBS-UP","thumps_up"),
        ("THUMBS-DOWN","thumps_down"),
        ("ANGRY","angry"),
        ("SAD","sad")
        )
    post=models.ForeignKey(Post,null=True,on_delete=models.CASCADE,related_name="reaction")
    comment=models.ForeignKey(Comment,null=True,on_delete=models.CASCADE,related_name="reaction")
    reaction=models.CharField(max_length=100,choices=REACTIONS)
    reacted_at=models.DateTimeField(auto_now=True)
    reacted_by=models.ForeignKey(User,on_delete=models.CASCADE)

