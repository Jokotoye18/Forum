from django.contrib import admin
from .models import Board, Topic, Post

# Register your models here.
class BoardAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Board, BoardAdmin)

class TopicAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("topic",)}

admin.site.register(Topic, TopicAdmin)

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("topic",)}

admin.site.register(Post, PostAdmin)
