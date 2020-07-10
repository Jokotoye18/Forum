from django.shortcuts import render, get_object_or_404,redirect
from django.contrib import messages
from django.http import Http404, HttpResponse
from django.db.models import Q
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Board, Topic, Post
from .forms import  NewTopicForm, NewTopicPostForm
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView,DetailView, View
from django.views.generic.edit import UpdateView, DeleteView
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required
from allauth.account.views import PasswordChangeView

#martor image uploader
import os
import json
import uuid

from django.conf import settings
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from martor.utils import LazyEncoder


class BoardTopicsView(View):
    def get(self, request, *args, **kwargs):
        board = get_object_or_404(Board, slug=self.kwargs['board_slug'])
        board_topics = board.topics.order_by('-created_on')
        context = {'board':board, 'board_topics': board_topics}
        return render(request, 'boards/board_topics.html', context)



class NewBoardTopicView(LoginRequiredMixin, View):
    login_url = 'account_login'
    redirect_field_name = 'next'
    def get(self, request, *args, **kwargs):
        form = NewTopicForm()
        context = {'form': form}
        return render(request, 'boards/new_board_topic.html', context)


    def post(self, request, *args, **kwargs):
        board = get_object_or_404(Board, slug=self.kwargs['board_slug'])
        form = NewTopicForm(request.POST)
        if form.is_valid() and form is not None:
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
            messages.success(request, 'Topic created successfully')
            # Todo : change the redirect url
            return redirect(reverse("boards:board_topics", kwargs={"board_slug":board.slug}))
        messages.warning(request, 'ValueError! Invalid input')
        return redirect(reverse("boards:new_board_topic", kwargs={"board_slug":board.slug}))



class TopicPostsView(View):
    def get(self, request, *args, **kwargs):
        topic = get_object_or_404(Topic, slug=self.kwargs.get('topic_slug'), pk=self.kwargs.get('topic_pk'))
        session_key = 'viewed_topic_{}'.format(topic.pk)
        print(session_key)
        if not request.session.get(session_key, False):
            topic.views += 1
            topic.save()
            request.session[session_key] = True
        subject = topic.posts.first()
        replies = topic.posts.all()[1:]
        print(request.session[session_key])
        context = {'topic':topic, 'subject': subject, 'replies': replies}
        return render(request, 'boards/topic_posts.html', context)

class NewTopicPostView(LoginRequiredMixin, View):
    login_url = 'account_login'
    redirect_field_name = 'next'
    def get(self, request, *args, **kwargs):
        form = NewTopicPostForm()
        topic = get_object_or_404(Topic, slug=self.kwargs["topic_slug"], pk=self.kwargs["topic_pk"])
        subject = topic.posts.first()
        replies = topic.posts.all()[1:]
        context = {"form":form, "topic": topic, "subject":subject, "replies": replies}
        return render(request, "boards/new_topic_post.html", context)


    def post(self, request, *args, **kwargs):
        form = NewTopicPostForm(data=request.POST)
        topic = get_object_or_404(Topic, slug=self.kwargs["topic_slug"], pk=self.kwargs["topic_pk"])
        if form.is_valid() and form is not None:
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            topic.updated_on = timezone.now()
            topic.save()
            messages.info(request, 'Reply successfully added')
            return redirect(reverse("boards:topic_posts", kwargs={"board_slug":topic.board.slug, "topic_slug":topic.slug, "topic_pk":topic.pk}))
        messages.warning(request, 'ValueError! Invalid input')
        return redirect(reverse("boards:new_topic_post", kwargs={"board_slug":topic.board.slug, 'topic_slug':topic.slug, 'topic_pk': topic.pk}))


class PostUpdateView(LoginRequiredMixin, View):
    login_url = 'account_login'
    redirect_field_name = 'next'
    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        form = NewTopicPostForm(instance=post)
        context = {'form': form, 'post':post}
        return render(request, 'boards/post_update.html', context)

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        topic = post.topic
        form = NewTopicPostForm(instance=post, data=request.POST)
        if form.is_valid() and form is not None:
            post = form.save()
            post.updated_on = timezone.now()
            messages.info(request, 'post updated successfully')
            return redirect(reverse("boards:topic_posts", kwargs={"board_slug":topic.board.slug, "topic_slug":topic.slug, "topic_pk":topic.pk}))
        messages.warning(request, 'ValueError! Invalid input')
        return redirect(reverse("boards:topic_posts", kwargs={"board_slug":topic.board.slug, "topic_slug":topic.slug, "topic_pk":topic.pk}))

class SearchView(View):
    def get(self, request, *args, **kwargs):
        q = request.GET.get('q', None)
        if q is None:
            search_list = []
        elif str(q).strip() ==  '':
            search_list = []
        else:
            search_list = Topic.objects.filter(topic__icontains=q)
            search_list = search_list.order_by('topic')       
        context = {'search_list': search_list, 'q':q}
        return render(request, 'search.html', context)






@login_required
def markdown_uploader(request):
    """
    Makdown image upload for locale storage
    and represent as json to markdown editor.
    """
    if request.method == 'POST' and request.is_ajax():
        if 'markdown-image-upload' in request.FILES:
            image = request.FILES['markdown-image-upload']
            image_types = [
                'image/png', 'image/jpg',
                'image/jpeg', 'image/pjpeg', 'image/gif'
            ]
            if image.content_type not in image_types:
                data = json.dumps({
                    'status': 405,
                    'error': _('Bad image format.')
                }, cls=LazyEncoder)
                return HttpResponse(
                    data, content_type='application/json', status=405)

            if image._size > settings.MAX_IMAGE_UPLOAD_SIZE:
                to_MB = settings.MAX_IMAGE_UPLOAD_SIZE / (1024 * 1024)
                data = json.dumps({
                    'status': 405,
                    'error': _('Maximum image file is %(size) MB.') % {'size': to_MB}
                }, cls=LazyEncoder)
                return HttpResponse(
                    data, content_type='application/json', status=405)

            img_uuid = "{0}-{1}".format(uuid.uuid4().hex[:10], image.name.replace(' ', '-'))
            tmp_file = os.path.join(settings.MARTOR_UPLOAD_PATH, img_uuid)
            def_path = default_storage.save(tmp_file, ContentFile(image.read()))
            img_url = os.path.join(settings.MEDIA_URL, def_path)

            data = json.dumps({
                'status': 200,
                'link': img_url,
                'name': image.name
            })
            return HttpResponse(data, content_type='application/json')
        return HttpResponse(_('Invalid request!'))
    return HttpResponse(_('Invalid request!'))