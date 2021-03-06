# Generated by Django 2.2.5 on 2019-10-30 06:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FacebookPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_title', models.CharField(max_length=400)),
                ('job_type', models.CharField(max_length=400)),
                ('post_url', models.URLField(max_length=2000, unique=True)),
                ('posted_via', models.URLField(max_length=2000)),
                ('number_of_likes', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='InstagramPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_url', models.URLField(max_length=2000, unique=True)),
                ('post_image_url', models.URLField(max_length=2000, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TwitterUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=400)),
                ('user_id', models.BigIntegerField(unique=True)),
                ('username', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('html_tweet_data', models.TextField(blank=True, null=True)),
                ('is_retweet', models.BooleanField(default=True)),
                ('likes', models.IntegerField()),
                ('replies', models.IntegerField()),
                ('retweets', models.IntegerField()),
                ('tweet_text', models.CharField(max_length=400)),
                ('timestamp', models.DateTimeField()),
                ('tweet_id', models.BigIntegerField(unique=True)),
                ('tweet_url', models.TextField(unique=True)),
                ('twitter_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tweets', to='socialfeeds.TwitterUser')),
            ],
        ),
        migrations.CreateModel(
            name='SocialFeedPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_tweet', models.BooleanField(default=False)),
                ('is_facebook_post', models.BooleanField(default=False)),
                ('is_instagram_post', models.BooleanField(default=False)),
                ('social_media_type', models.IntegerField(choices=[(0, 'Twitter'), (1, 'Facebook'), (2, 'Instagram')], default=0)),
                ('facebook_post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='social_feed_posts', to='socialfeeds.FacebookPost')),
                ('instagram_post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='social_feed_posts', to='socialfeeds.InstagramPost')),
                ('tweet', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='social_feed_posts', to='socialfeeds.Tweet')),
            ],
        ),
    ]
