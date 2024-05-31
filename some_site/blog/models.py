from django.db import models
from django.contrib.auth.models import User
from jsonfield import JSONField

class blog(models.Model):
    blog_id = models.CharField(max_length=777, help_text="id of blog", primary_key=True)
    themes = models.CharField(max_length=777, help_text="theme of blog")
    about = models.CharField(max_length=777, help_text="about of blog")
    name_of_blog = models.CharField(max_length=20, help_text="name of blog")
    cover = models.ImageField(upload_to='images/')
    followers = models.IntegerField(default=0)
    sub = JSONField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.blog_id

class states(models.Model):
    state_id = models.IntegerField()
    blog_id = models.IntegerField()
    time_of_publication = models.DateField()
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    topic = models.CharField(max_length=23, help_text="name of state")
    text = models.CharField(max_length=7777, help_text="text of state")
    likes = JSONField()
    dislikes = JSONField()

    def __str__(self):
        return str(self.state_id)

class comments(models.Model):
    state_id = models.IntegerField()
    user = models.CharField(max_length=7777)
    date = models.DateField()
    text = models.CharField(max_length=666)

    def __str__(self):
        return str(self.state_id)