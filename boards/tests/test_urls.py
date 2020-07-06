from django.test import SimpleTestCase
from django.urls import reverse, resolve
from boards.views import (
    BoardTopicsView, 
    TopicPostsView,  
    NewBoardTopicView, 
    NewTopicPostView, 
    PostUpdateView, 
    SearchView, 
)


class TestUrls(SimpleTestCase):
    def setUp(self):
        pass

    def test_board_topics_url_is_resolved(self):
        url = reverse('boards:board_topics', args=['some-slug'])
        self.assertEqual(resolve(url).func.view_class, BoardTopicsView)

    def test_topic_posts_url_is_resolved(self):
        url = reverse('boards:topic_posts', args=['some-slug', 'topic-slug', 1])
        self.assertEqual(resolve(url).func.view_class, TopicPostsView)
    
    def test_new_board_topic_url_is_resolved(self):
        url = reverse('boards:new_board_topic', args=['some-slug'])
        self.assertEqual(resolve(url).func.view_class, NewBoardTopicView)

    def test_new_topic_post_url_is_resolved(self):
        url = reverse('boards:new_topic_post', args=['some-slug', 'topic-slug', 1])
        self.assertEqual(resolve(url).func.view_class, NewTopicPostView)

    def test_post_update_url_is_resolved(self):
        url = reverse('boards:post_update', args=['some-slug', 'topic-slug', 1, 1,])
        self.assertEqual(resolve(url).func.view_class, PostUpdateView)
    
    def test_search_is_resolved(self):
        url = reverse('boards:search')
        self.assertEqual(resolve(url).func.view_class, SearchView)
