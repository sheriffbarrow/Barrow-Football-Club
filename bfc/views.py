from contextvars import Context
from http.client import HTTPResponse
import mimetypes
from multiprocessing import context
from django.shortcuts import render
from .models import FirstTeamStaff, Post, Match, PlayerProfile, CurrentUpdate, Staff, Banner, Match
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from account.models import Registration
import datetime
from django.template.loader import get_template
from django.template import Context


# Create your views here.

"""
def index(request):
    latest_post1 = Post.objects.order_by('-created')[:3]
    latest_post2 = Post.objects.order_by('-created')[3:6]
    playerprofile = PlayerProfile.objects.all()
    latests = CurrentUpdate.objects.all()
    
    context = { 
        'post1': latest_post1,  
        'post2': latest_post2,  
        'profile': playerprofile,
        'latest': latests,   
    }
    return render(request, 'bfc/base/index1.html', context)
"""



class Home(ListView):
    model = Post
    template_name = 'bfc/base/index1.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['post0'] = Post.objects.all()[:1]
        context['post1'] = Post.objects.filter(approve_to_post=True)[:3]
        context['post2'] = Post.objects.all()[3:6]
        context['update'] = CurrentUpdate.objects.all()
        context['playerprofile'] = PlayerProfile.objects.all()
        #context['matches'] = Match.objects.all().order_by('-created')[:1]
        today = datetime.date.today()
        context['upcoming'] = Match.objects.filter(fixture_date_and_time__date__gte=today).order_by('fixture_date_and_time')
        context['upcomings'] = Match.objects.filter(fixture_date_and_time__date__gt=today)[1:]
        context['lastmatch'] = Match.objects.filter(fixture_date_and_time__date__lt=today).order_by('-fixture_date_and_time')
        return context


def firstteam(request):
    first_team = PlayerProfile.objects.all()
    team_goal = PlayerProfile.objects.filter(position__iexact= 'GOALKEEPER')
    team_defend = PlayerProfile.objects.filter(position__iexact = 'DEFENDER')
    team_midfield = PlayerProfile.objects.filter(position__iexact = 'MIDFIELDER')
    team_striker = PlayerProfile.objects.filter(position__iexact = 'STRIKER')
    team_loan = PlayerProfile.objects.filter(position__iexact = 'LOAN')
    banner = Banner.objects.all()
    first_team = FirstTeamStaff.objects.all()

    context = {
        'banner': banner,
        'firstteam': first_team,
        'team_goal': team_goal,
        'team_defend': team_defend,
        'team_midfield': team_midfield,
        'team_striker': team_striker,
        'team_loan': team_loan,
        'first_team': first_team,
    }
    return render(request, 'bfc/first-team.html', context)


"""
def player_Profile(request):
    players = PlayerProfile.objects.all()
    context = {
        'players': players,
    }
    return render(request, 'bfc/player-profile.html')
"""

class PlayersProfile(DetailView):
    model = PlayerProfile
    template_name = 'bfc/player-profile.html'
    context_object_name = 'player_profiles'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['players'] = PlayerProfile.objects.all()
        context['first_team'] = PlayerProfile.objects.all()
        context['team_goal'] = PlayerProfile.objects.filter(position__iexact= 'GOALKEEPER')
        context['team_defend'] = PlayerProfile.objects.filter(position__iexact = 'DEFENDER')
        context['team_midfield'] = PlayerProfile.objects.filter(position__iexact = 'MIDFIELDER')
        context['team_striker'] = PlayerProfile.objects.filter(position__iexact = 'STRIKER')
        return context


def news_first_team(request):
    post0 = Post.objects.all().order_by('-publish')[:1]
    post1 = Post.objects.all()
    context = {
        'posts': post0,
        'post1': post1,
    }
    return render(request, 'bfc/news-first-team.html', context)


class ArticleDetailView(DetailView):
    model = Post
    template_name = 'bfc/news-details.html'
    context_object_name = 'detailss'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["related_items"] = self.object.tags.similar_objects()
        context['post1'] = Post.objects.all()[:5]
        context['options'] = Post.objects.all()[2:]
        context['option1'] = Post.objects.all()[3:]
        context['update'] = CurrentUpdate.objects.all()
        context['writter'] = Post.objects.all()
        context['post_owner'] = Post.objects.all().values('title', 'author')
        return context


class UpdateDetailView(DetailView):
    model = CurrentUpdate
    template_name = 'bfc/update-details.html'
    context_object_name = 'updates'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["related_update"] = self.object.tags.similar_objects()
        context['post1'] = Post.objects.all()[:5]
        context['options'] = Post.objects.all()[2:]
        context['option1'] = Post.objects.all()[3:]
        context['update'] = CurrentUpdate.objects.all()
        
        return context



def staff(request):
    staff = Staff.objects.all()
    context = {
        'staff': staff,
    }
    return render(request, 'bfc/staff.html', context)


class StaffDetailView(DetailView):
    model = Staff
    template_name = 'bfc/staff-profile.html'
    context_object_name = 'staff'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['staff_profile'] = Staff.objects.all()
        return context

class FirstTeamDetails(DetailView):
    model = FirstTeamStaff
    template_name = 'bfc/teamstaff.html'
    context_object_name = 'team_staff'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['first_team'] = FirstTeamStaff.objects.all()
        return context


def error_404(request, exception):
        data = {}
        return render(request,'bfc/404.html', data)

def error_500(request):
        data = {}
        return render(request,'bfc/500.html', data)