from django.shortcuts import render
from django.views.generic import View
from boards.models import Board
from allauth.account.views import password_change

class HomeView(View):
    
    def get(self, *args, **kwargs):
        boards = Board.objects.order_by('name')
        context = {"board_list": boards}
        return render(self.request, "home.html", context)