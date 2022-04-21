from django.urls import path
from bfc import views
from .views import Home
from bfc.views import ArticleDetailView,PlayersProfile,StaffDetailView, FirstTeamDetails, UpdateDetailView
from bfc.feeds import LastPostFeed


app_name = 'bfc'

urlpatterns = [

    path('', Home.as_view(),name="myhome"),
   path('first-team/', views.firstteam, name='firstteam'),
   path('first-team-news/', views.news_first_team, name='news-first-team'),
   path('staff/', views.staff, name='staff'),
   #path('team-news/<slug:slug>/',views.news_details, name='news-details'),
   path('<slug:slug>/', ArticleDetailView.as_view(), name='news-details'),
   path('update/<slug>/', UpdateDetailView.as_view(), name='update-details'),
   path('player-profile/<slug>/', PlayersProfile.as_view(), name='player-profile'),
   path('staff/<slug>/', StaffDetailView.as_view(), name='staff-profile'),
   path('first-team/staff/<slug>/', FirstTeamDetails.as_view(), name='team-staff'),
   path('feed/', LastPostFeed(), name='post_feed'),  
 
   
]
