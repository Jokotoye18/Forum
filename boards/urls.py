from django.urls import path
from .views import BoardTopicsView, TopicPostsView,  NewBoardTopicView, NewTopicPostView, PostUpdateView, SearchView, cookie
from pages.views import HomeView
app_name = 'boards'

urlpatterns = [
    path('cookie/', cookie),
    path('boards/<slug:board_slug>/', BoardTopicsView.as_view(), name='board_topics' ),
    path('boards/<slug:board_slug>/topics/<slug:topic_slug>-<int:topic_pk>/', TopicPostsView.as_view(), name='topic_posts' ),
    path('boards/<slug:board_slug>/create-new/', NewBoardTopicView.as_view(), name='new_board_topic' ),
    path('boards/<slug:board_slug>/topics/<slug:topic_slug>-<int:topic_pk>/reply/', NewTopicPostView.as_view(), name='new_topic_post' ),
    path('boards/<slug:board_slug>/topics/<slug:topic_slug>-<int:topic_pk>/posts/<int:pk>/edit/', PostUpdateView.as_view(), name='post_update' ),
    path('search/', SearchView.as_view(), name='search'),
]