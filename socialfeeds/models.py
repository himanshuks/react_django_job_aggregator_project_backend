from django.db import models

# Create your models here.


class TwitterUser(models.Model):
    fullname = models.CharField(max_length=400)
    user_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.username}"


class Tweet(models.Model):
    html_tweet_data = models.TextField(blank=True, null=True)
    is_retweet = models.BooleanField(default=True)
    likes = models.IntegerField()
    replies = models.IntegerField()
    retweets = models.IntegerField()
    tweet_text = models.CharField(max_length=400)
    timestamp = models.DateTimeField()
    tweet_id = models.BigIntegerField(unique=True)
    tweet_url = models.TextField(unique=True)
    twitter_user = models.ForeignKey(
        TwitterUser,
        related_name='tweets',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Tweet - {self.tweet_id}"


class FacebookPost(models.Model):
    job_title = models.CharField(max_length=400)
    job_type = models.CharField(max_length=400)
    post_url = models.URLField(max_length=2000, unique=True)
    posted_via = models.URLField(max_length=2000, )
    number_of_likes = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.job_title} | {self.job_type}"


class InstagramPost(models.Model):
    post_url = models.URLField(max_length=2000, unique=True)
    post_image_url = models.URLField(max_length=2000, unique=True)

    def __str__(self):
        return f"{self.post_url}"


SOCIAL_FEED_POSTS_CHOICES = (
    (0, 'Twitter'),
    (1, 'Facebook'),
    (2, 'Instagram'),
)


class SocialFeedPost(models.Model):
    is_tweet = models.BooleanField(default=False)
    is_facebook_post = models.BooleanField(default=False)
    is_instagram_post = models.BooleanField(default=False)

    social_media_type = models.IntegerField(
        choices=SOCIAL_FEED_POSTS_CHOICES, default=0)

    tweet = models.ForeignKey(Tweet, related_name='social_feed_posts',
                              blank=True, null=True, on_delete=models.CASCADE)
    facebook_post = models.ForeignKey(
        FacebookPost,
        related_name='social_feed_posts',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    instagram_post = models.ForeignKey(
        InstagramPost,
        related_name='social_feed_posts',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    def save(self, *args, **kwargs):
        if self.social_media_type == 0:
            self.is_tweet = True

        if self.social_media_type == 1:
            self.is_facebook_post = True

        if self.social_media_type == 2:
            self.is_instagram_post = True

        super().save(*args, **kwargs)

    def __str__(self):
        if self.is_tweet:
            return f"Twitter Post - {self.tweet}"
        if self.is_facebook_post:
            return f"Facebook Post - {self.facebook_post}"
        if self.is_instagram_post:
            return f"Instagram Post - {self.instagram_post}"
