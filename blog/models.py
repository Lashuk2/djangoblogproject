from django.db import models
from django.contrib.auth.models import User
from embed_video.fields import EmbedVideoField
from taggit.managers import TaggableManager


# Объвляем кортеж для статуса сообщений
STATUS = (
    (0, "Draft"),   # Черновик
    (1, "Publish")  # Опубликованное сообщение
)


class Post(models.Model):
    title = models.CharField(max_length=248, unique=True)
    slug = models.SlugField(max_length=248, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    video = EmbedVideoField(blank=True, verbose_name='Видео')
    tags = TaggableManager()
    count_views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title


class PostCountView(models.Model):
    sesId = models.CharField(max_length=150, db_index=True)
    postId = models.ForeignKey(Post, blank=True, null=True, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.sesId)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.content, self.name)
