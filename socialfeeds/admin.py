from django.contrib import admin

from .models import Tweet, TwitterUser, FacebookPost, InstagramPost, SocialFeedPost
# Register your models here.

admin.site.register(Tweet)
admin.site.register(TwitterUser)
admin.site.register(FacebookPost)
admin.site.register(InstagramPost)
admin.site.register(SocialFeedPost)
