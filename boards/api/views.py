from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from accounts.models import Profile
from boards.models import Board, Topic, Post
from rest_framework.response import Response
from rest_framework.parsers import FormParser
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveUpdateAPIView
from .serializers import BoardSerializer, TopicSerializer, PostSerializer, UserProfileSerializer

class BoardList(ListAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    filter_fields = [
        'name',
    ]
    search_fields = [
        'name',
    ]
    ordering_fields = [
        'name',
    ]

class BoardDetail(RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    lookup_field = 'slug'

class BoardTopicList(ListCreateAPIView):
    serializer_class = TopicSerializer
    lookup_field = 'board__slug'
    def get_queryset(self):
        queryset = Topic.objects.filter(board__slug=self.kwargs.get('slug'))
        return queryset

    def post(self, request, *args, **kwargs):
        board = get_object_or_404(Board, slug=self.kwargs.get('slug'))
        serializer = TopicSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(board=board, starter=request.user)
            # Post.objects.create(
            #     topic=request.data.get('topic'),
            #     subject = request.data.get('subject'),
            #     created_by = request.user
            # )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class TopicPostList(APIView):
    def get(self, request, *args, **kwargs):
        subject = Post.objects.filter(topic__slug=self.kwargs.get('topic_slug')).first()
        replies = Post.objects.filter(topic__slug=self.kwargs.get('topic_slug'))[1:]
        if replies:
            subject_serializer = PostSerializer(subject)
            replies_serializer = PostSerializer(replies, many=True)
            return Response({
                'subject': subject_serializer.data,
                'replies': replies_serializer.data
            })
        else:
            subject_serializer = PostSerializer(subject)
            return Response({
                'subject': subject_serializer.data,
                'replies': 'No reply yet!'
            })

    def post(self, request, *args, **kwargs):
        topic = get_object_or_404(Topic, slug=self.kwargs.get('topic_slug'))
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(topic=topic, created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    queryset = Profile.objects.all()
    lookup_field = 'user__username'
    lookup_url_kwarg = 'username'

    # def get(self, request, *args, **kwargs):
    #     profile = get_object_or_404(Profile, user__username=self.kwargs.get('username'))
    #     serializer = UserProfileSerializer(profile)
    #     return Response(serializer.data)

    # def patch(self, request, *args, **kwargs):
    #     profile = get_object_or_404(Profile, user__username=self.kwargs.get('username'))
    #     serializer = UserProfileSerializer(profile, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

