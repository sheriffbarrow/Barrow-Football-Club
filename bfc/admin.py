from django.contrib import admin
from .models import Post, Match, PlayerProfile, CurrentUpdate, Staff, Banner,FirstTeamStaff
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.


admin.site.site_header = "Barrow Football Club"


class FirstTeamStaffAdmin(SummernoteModelAdmin):
  list_display = ['first_Name','last_Name','role','created','year_joined']
  prepopulated_fields = {'slug':('role','first_Name','last_Name',)}


class PlayerProfileAdmin(SummernoteModelAdmin):
  list_display = ['firstName', 'surname','nationality', 'position', 'dob', 'jerseyNumber']
  list_filter = ('firstName', 'surname')
  prepopulated_fields = {'slug':('firstName','surname',)}


class CurrentUpdateAdmin(SummernoteModelAdmin):
  list_display = ('title', 'dateTime')
  prepopulated_fields = {'slug':('title',)}


class PostAdmin(SummernoteModelAdmin):
  list_display = ('author','title','publish','approve_to_post')
  list_filter = ('tags','created')
  prepopulated_fields = {'slug':('title',)}

  

class MatchAdmin(admin.ModelAdmin):
  list_display = ('homeTeam','awayTeam', 'scoreline_home','scoreline_away', 'fixture_date_and_time')
  ordering = ['-fixture_date_and_time']
  list_filter = ('created','slug')
  prepopulated_fields = {'slug':('homeTeam','awayTeam',)}



class StaffAdmin(SummernoteModelAdmin):
  list_display = ('surName', 'firstName','position')
  list_filter = ('firstName','position')
  prepopulated_fields = {'slug':('surName','firstName',)}



#admin.site.index_template = 'memcache_status/admin_index.html'

admin.site.register(Staff, StaffAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(CurrentUpdate, CurrentUpdateAdmin)
admin.site.register(PlayerProfile, PlayerProfileAdmin)
admin.site.register(Banner)
admin.site.register(FirstTeamStaff, FirstTeamStaffAdmin)
