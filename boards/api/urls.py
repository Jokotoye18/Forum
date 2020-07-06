from django.urls import path
from .views import (
    BoardList,
    BoardDetail,
    BoardTopicList,
    TopicPostList,
    ProfileView,
)

urlpatterns = [
    path('', BoardList.as_view(), name='board-list'),
    path('board/<slug:slug>/', BoardDetail.as_view(), name='board-detail'),
    path('board/<slug:slug>/topics/', BoardTopicList.as_view(), name='board-topic-list'),
    path('board/<slug:slug>/topics/<slug:topic_slug>/', TopicPostList.as_view(), name='topic-post-list'),
    path('profile/<username>/', ProfileView.as_view(), name='user-profile'),
]