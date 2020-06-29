from django.shortcuts import render, get_object_or_404,redirect
from django.contrib import messages
from django.http import Http404
from django.db.models import Q
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Board, Topic, Post
from .forms import  NewTopicForm, NewTopicPostForm
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView,DetailView, View
from django.views.generic.edit import UpdateView, DeleteView
from django.utils import timezone


class BoardTopicsView(View):
    def get(self, request, *args, **kwargs):
        board = get_object_or_404(Board, slug=self.kwargs['board_slug'])
        board_topics = board.topics.order_by('-created_on')
        context = {'board':board, 'board_topics': board_topics}
        return render(request, 'boards/board_topics.html', context)



class NewBoardTopicView(LoginRequiredMixin, View):
    login_url = 'account_login'
    def get(self, request, *args, **kwargs):
        form = NewTopicForm()
        context = {'form': form}
        return render(request, 'boards/new_board_topic.html', context)


    def post(self, request, *args, **kwargs):
        board = get_object_or_404(Board, slug=self.kwargs['board_slug'])
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            post = request.POST.get('subject')
            post = Post.objects.create(
                topic = topic,
                post = post,
                created_by = request.user
            )
            # messages.success(request, 'Topic created successfully')
            # Todo : change the redirect url
            return redirect(reverse("boards:board_topics", kwargs={"board_slug":board.slug}))



class TopicPostsView(DetailView):

    def get(self, request, *args, **kwargs):
        topic = get_object_or_404(Topic, slug=self.kwargs.get('topic_slug'), pk=self.kwargs.get('topic_pk'))
        subject = topic.posts.first()
        replies = topic.posts.all()[1:]
        print(topic.posts.count())
        print(replies.count())
        topic.views += 1
        topic.save()
        context = {'topic':topic, 'subject': subject, 'replies': replies}
        return render(request, 'boards/topic_posts.html', context)

class NewTopicPostView(LoginRequiredMixin, View):
    
    def get(self, request, *args, **kwargs):
        form = NewTopicPostForm()
        topic = get_object_or_404(Topic, slug=self.kwargs["topic_slug"], pk=self.kwargs["topic_pk"])
        subject = topic.posts.first()
        replies = topic.posts.all()[1:]
        context = {"form":form, "topic": topic, "subject":subject, "replies": replies}
        return render(request, "boards/new_topic_post.html", context)


    def post(self, request, *args, **kwargs):
        form = NewTopicPostForm(request.POST)
        topic = get_object_or_404(Topic, slug=self.kwargs["topic_slug"], pk=self.kwargs["topic_pk"])
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            topic.updated_on = timezone.now()
            topic.save()
            messages.info(request, 'post successfully added')
            return redirect(reverse("boards:topic_posts", kwargs={"board_slug":topic.board.slug, "topic_slug":topic.slug, "topic_pk":topic.pk}))
        

class PostUpdateView(View):
    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        form = NewTopicPostForm(instance=post)
        context = {'form': form}
        return render(request, 'boards/post_update.html', context)

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        topic = post.topic
        form = NewTopicPostForm(instance=post, data=request.POST)
        if form.is_valid():
            post = form.save()
            post.updated_on = timezone.now()
            messages.info(request, 'post updated successfully')
            return redirect(reverse("boards:topic_posts", kwargs={"board_slug":topic.board.slug, "topic_slug":topic.slug, "topic_pk":topic.pk}))

class SearchView(View):
    def get(self, request, *args, **kwargs):
        q = request.GET.get('q', None)
        if q is None:
            search_list = None
        else:
            search_list = Topic.objects.filter(topic__icontains=q)        
        context = {'search_list': search_list}
        return render(request, 'search.html', context)
