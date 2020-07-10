from django.contrib import admin
from django import forms
from .models import Board, Topic, Post
from martor.widgets import AdminMartorWidget
# Register your models here.
class BoardAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Board, BoardAdmin)

class TopicAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("topic",)}

admin.site.register(Topic, TopicAdmin)


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("topic",)}
    list_display = ['post']
    formfield_overrides = {
        Post.post: {'widget': AdminMartorWidget},
    }

admin.site.register(Post, PostAdmin)