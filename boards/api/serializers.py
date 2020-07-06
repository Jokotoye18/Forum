from rest_framework import serializers
from boards.models import Board, Topic, Post, BADGES_CATEGORY
from accounts.models import Profile
from django.contrib.auth import get_user_model
   


class BoardSerializer(serializers.HyperlinkedModelSerializer):
    badge = serializers.SerializerMethodField()
    total_post = serializers.CharField(source='get_post_count', read_only=True)
    last_post_by = serializers.CharField(source='get_last_post_API', read_only=True)
    total_topics = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(view_name='board-detail', lookup_field='slug')

    def get_total_topics(self, obj):
        return obj.topics.count()

    def get_badge(self, obj):
        return obj.get_badge_display()
        
    class Meta:
        model = Board
        fields = ['id', 'url', 'name', 'description', 'badge', 'total_post', 'last_post_by', 'total_topics']
        read_only_fields = ['badge']

class BoardTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = [ 'name', 'description']

class TopicSerializer(serializers.ModelSerializer):
    starter = serializers.ReadOnlyField(source='starter.username')
    replies = serializers.SerializerMethodField()
    last_updated = serializers.SerializerMethodField()
    board = BoardTopicSerializer(read_only=True)
    subject = serializers.CharField(write_only=True, max_length=1000, style={'base_template': 'textarea.html', 'rows': 10})

    def get_last_updated(self, obj):
        last_post = obj.posts.last()
        return last_post.created_on
    def get_replies(self, obj):
        if obj.posts.count() >= 2:
            return int(obj.posts.count()) - 1
        return 0

    class Meta:
        model = Topic
        fields = [ 'id', 'topic', 'board', 'slug', 'subject', 'views', 'starter', 'replies', 'last_updated', 'created_on', 'updated_on',]
        read_only_fields = ['views', 'slug']

    def create(self, validated_data):
        subject = validated_data.pop('subject')
        topic = Topic.objects.create(**validated_data)
        Post.objects.create(topic=topic, **subject)
        return topic


class PostSerializer(serializers.ModelSerializer):
    topic = serializers.ReadOnlyField(source='topic.topic')
    class Meta:
        model = Post
        fields = ['id', 'topic', 'post', 'created_by', 'updated_by', 'created_on', 'updated_on']
        read_only_fields = ['created_by']

class UserSerializer(serializers.ModelSerializer):
    # full_name = serializers.CharField(source='get_full_name')
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name']
        # read_only_fields = ['full_name']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Profile
        fields = ['user', 'image']