from django.test import TestCase, Client
from django.urls import reverse
from boards.models import Post, Topic, Board
from django.contrib.auth import get_user_model

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username = 'user1',
            password = 'testpassword',
            email = 'user1@gmail.com',
        )
        self.board = Board.objects.create(
            name = 'board1',
            description = 'board1 description',
            badge = 'P'
        )
        self.topic = Topic.objects.create(
            board = self.board,
            topic = 'Some topic',
            starter = self.user
        )
        # login = self.client.login(username=self.user.username, password=self.user.password) 
        # self.assertTrue(login) 

    def test_board_topic_view(self):
        response = self.client.get(reverse('boards:board_topics', args=[self.board.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'boards/board_topics.html')

    
    def test_board_topic_POST_view(self):
        data = {
            'board': self.board,
            'topic': 'board2 topic',
            'starter': self.user,
            'subject': 'Some subject'
        }
        response = self.client.post(reverse('boards:new_board_topic', 
            args=[self.board.slug]), 
            data
        )
        self.assertEqual(response.status_code, 302)
