from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.utils import timezone

#from ckeditor_uploader.fields import RichTextUploadingField


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    h1 = models.CharField(max_length=200)
    img = models.ImageField()
    url = models.SlugField()
    #content = RichTextUploadingField()
    content = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    #discription = RichTextUploadingField()
    discription = models.TextField()
    tag = TaggableManager()

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_name')
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.text