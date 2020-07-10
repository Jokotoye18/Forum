from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.html import mark_safe
from markdown import markdown
from django.template.defaultfilters import slugify
from martor.models import MartorField


BADGES_CATEGORY = (
    ('P', 'primary'),
    ('S', 'success'),
    ('D', 'dark'),
    ('W', 'warning'),
)

class Board(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=200)
    badge = models.CharField(max_length=1, choices=BADGES_CATEGORY)
    slug = models.SlugField(blank=True, max_length=100)

    objects = models.Manager()


    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def get_post_count(self):
        post_count = Post.objects.filter(topic__board=self).count()
        return post_count

    def get_last_post(self):
        last_post = Post.objects.filter(topic__board=self).order_by("-created_on").first()
        return last_post
        
    def get_last_post_API(self):
        last_post = Post.objects.filter(topic__board=self).order_by("-created_on").first()
        if last_post:
            return last_post.created_by
        return 'No post yet'

class Topic(models.Model):
    board = models.ForeignKey(Board, related_name='topics', on_delete=models.CASCADE)
    topic = models.CharField(max_length=200, unique=True) 
    slug = models.SlugField(blank=True, max_length=200)
    views = models.PositiveIntegerField(default=0)
    starter = models.ForeignKey(get_user_model(), related_name="topics", on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return self.topic


    def save(self, *args, **kwargs):
        self.slug = slugify(self.topic)
        return super().save(*args, **kwargs)
    

class Post(models.Model):
    topic = models.ForeignKey(Topic, related_name='posts',on_delete=models.CASCADE)
    post = MartorField()
    slug = models.SlugField(blank=True, max_length=200)
    created_by = models.ForeignKey(get_user_model(), related_name='posts', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(get_user_model(), related_name="+", on_delete=models.CASCADE, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()


    def __str__(self):
        return self.post

    def save(self, *args, **kwargs):
        self.slug = slugify(self.topic)
        return super().save(*args, **kwargs)

    def get_post_as_markdown(self):
        return mark_safe(markdown(self.post, safe_mode='escape'))
    



