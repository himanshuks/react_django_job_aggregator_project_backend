import os
import json
import pytz
import random
from datetime import datetime

from .models import FacebookPost, TwitterUser, Tweet, SocialFeedPost


def populate_facebook_posts(*args, **kwargs):

    if kwargs['offset']:
        offset = kwargs['offset']
    else:
        offset = 0

    if kwargs['limit']:
        limit = kwargs['limit'] - 1
        limit = limit + offset
    else:
        limit = None

    # Read the file
    file = os.path.join('json_data', 'Facebook.json')
    with open(file, 'r', encoding='utf-8') as fp:
        json_data = json.load(fp)

    iteration = 0
    failed_data = []

    for entry in json_data[offset:limit]:
        iteration += 1

        try:

            facebook_post, created = FacebookPost.objects.get_or_create(
                job_title=entry['Job Title'],
                job_type=entry['Job Company'],
                post_url=entry['Page Url'],
                posted_via=entry['Posted Via'],
                number_of_likes=entry['NoOfLikes'],
            )

            if created:
                facebook_post.save()

            print(f"Iteration {iteration} - successful.")

        except Exception as e:
            failed_data.append((entry, iteration, str(e)))
            print(f"Failed at iteration {iteration}")

    print(f"total number of records that were erroneous = {len(failed_data)}")

    # error log
    error_files = os.path.join('json_data', 'temp', 'facebook_error_data.json')
    with open(error_files, 'w', encoding='utf-8') as fp:
        json.dump(failed_data, fp, indent=4)


def populate_tweets(*args, **kwargs):
    if kwargs['offset']:
        offset = kwargs['offset']
    else:
        offset = 0

    if kwargs['limit']:
        limit = kwargs['limit'] - 1
        limit = limit + offset
    else:
        limit = None

    # Twitter data first
    # Read the file
    file = os.path.join('json_data', 'Twitter.json')
    with open(file, 'r', encoding='utf-8') as fp:
        json_data = json.load(fp)

    iteration = 0
    failed_data = []

    for entry in json_data[offset:limit]:
        iteration += 1

        try:

            twitter_user, created = TwitterUser.objects.get_or_create(
                fullname=entry['fullname'],
                user_id=entry['user_id'],
                username=entry['username'],
            )

            tweet, created = Tweet.objects.get_or_create(
                html_tweet_data=entry['html'],
                is_retweet=entry['is_retweet'],
                likes=entry['likes'],
                replies=entry['replies'],
                retweets=entry['retweets'],
                tweet_text=entry['text'],
                timestamp=datetime.utcfromtimestamp(entry['timestamp_epochs']).replace(tzinfo=pytz.utc),
                tweet_id=entry['tweet_id'],
                tweet_url=entry['tweet_url'],
                twitter_user=twitter_user,
            )

            print(f"Iteration {iteration} - successful.")

        except Exception as e:
            failed_data.append((entry, iteration, str(e)))
            print(f"Failed at iteration {iteration}")

    print(f"total number of records that were erroneous = {len(failed_data)}")

    # error log
    error_files = os.path.join('json_data', 'temp', 'twitter_error_data.json')
    with open(error_files, 'w', encoding='utf-8') as fp:
        json.dump(failed_data, fp, indent=4)


def populate_social_feed_posts(*args, **kwargs):

    if kwargs['offset']:
        offset = kwargs['offset']
    else:
        offset = 0

    if kwargs['limit']:
        limit = kwargs['limit'] - 1
        limit = limit + offset
    else:
        limit = None
    iteration = 0
    failed_data = []

    tweets = Tweet.objects.all()[offset:limit]
    facebook_posts = FacebookPost.objects.all()[offset:limit]

    tweets = list(tweets)
    facebook_posts = list(facebook_posts)

    combined_data = tweets + facebook_posts
    random.seed(6)
    random.shuffle(combined_data)

    for entry in combined_data:
        iteration += 1

        try:

            if type(entry) == Tweet:
                social_feed_post, created = SocialFeedPost.objects.get_or_create(
                    social_media_type=0,
                    tweet=entry,
                )

            if type(entry) == FacebookPost:
                social_feed_post, created = SocialFeedPost.objects.get_or_create(
                    social_media_type=1,
                    facebook_post=entry,
                )

            print(f"Iteration {iteration} - successful.")

        except Exception as e:
            failed_data.append((entry, iteration, str(e)))
            print(f"Failed at iteration {iteration}")

    print(f"total number of records that were erroneous = {len(failed_data)}")

    # error log
    error_files = os.path.join('json_data', 'temp', 'social_feed_post_error_data.json')
    with open(error_files, 'w', encoding='utf-8') as fp:
        json.dump(failed_data, fp, indent=4)
