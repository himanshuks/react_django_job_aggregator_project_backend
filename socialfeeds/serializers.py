from rest_framework import serializers
from .models import Tweet, TwitterUser, FacebookPost, InstagramPost, SocialFeedPost


class TwitterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TwitterUser
        fields = ['fullname', 'user_id', 'username']


class TweetSerializer(serializers.ModelSerializer):

    twitter_user = TwitterUserSerializer()

    class Meta:
        model = Tweet
        fields = [
            'html_tweet_data',
            'is_retweet',
            'likes',
            'replies',
            'retweets',
            'tweet_text',
            'timestamp',
            'tweet_id',
            'tweet_url',
            'twitter_user',
        ]


class FacebookPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacebookPost
        fields = [
            'job_title',
            'job_type',
            'post_url',
            'posted_via',
            'number_of_likes',
        ]


class InstagramPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstagramPost
        fields = [
            'post_url',
            'post_image_url',
        ]


class SocialFeedPostSerializer(serializers.ModelSerializer):

    tweet = TweetSerializer()
    facebook_post = FacebookPostSerializer()
    instagram_post = InstagramPostSerializer()

    class Meta:
        model = SocialFeedPost
        fields = [
            'is_tweet',
            'is_facebook_post',
            'is_instagram_post',
            'tweet',
            'facebook_post',
            'instagram_post',
        ]
