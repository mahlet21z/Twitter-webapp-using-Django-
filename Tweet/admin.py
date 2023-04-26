from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, Tweet

# Register your models here.


# unregister groups 
admin.site.unregister(Group)

#combine profile and iser info
class profileInline(admin.StackedInline):
    model = Profile 

#extend user model
class UserAdmin(admin.ModelAdmin):
    model = User
    #dispaly user name
    fields = ["username"]
    inlines = [profileInline] 

    #unregister the old user
admin.site.unregister(User)

    #Reregister user and profile
admin.site.register(User, UserAdmin)  
# admin.site.register(Profile)

#register tweets
admin.site.register(Tweet)
