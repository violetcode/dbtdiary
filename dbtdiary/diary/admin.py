from django.contrib import admin
from .models import UsedSkills, Diary, UserProfile

class DiaryAdmin(admin.ModelAdmin):
   search_fields = ['user','time',]
   list_display = ('user', 'time',) 

class UserProfileAdmin(admin.ModelAdmin):
    search_fields = ['user', 'active']
    list_display = ('user', 'active')

admin.site.register(UsedSkills)
admin.site.register(Diary,DiaryAdmin)
admin.site.register(UserProfile,UserProfileAdmin)
