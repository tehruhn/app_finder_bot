import praw
import re

from datetime import date, timedelta
import random
import decimal
import time
import os

reddit = praw.Reddit("app-finder-bot")
subreddit = reddit.subreddit("all")


def generate_message():
    """
    Generates message to be posted
    """

    rand_imgs = str("{:,}".format(random.randrange(100000000, 500000000)))
    rand_posts = str("{:,}".format(random.randrange(100000000, 500000000)))
    rand_time = str(decimal.Decimal(random.randrange(1000000))/100000) + 's'
    android_num = random.randrange(2,5)
    ios_num = random.randrange(2,5)
    name_file = open("names.txt", "r")
    names = name_file.read().splitlines()
    names_idx = random.sample(range(len(names)), android_num+ios_num)

    output_str = "Are you looking for an app for this?\n\n" +\
                 "I found {android} Android apps, and {ios} iOS apps that match your use case! \n\n".format(android=android_num, ios=ios_num) +\
                 "Here they are in descending order of match percentage : \n\n"

    # android apps
    output_str += "**Android apps**\n\n"

    for i in range(android_num):
        percent_start = 90 - i*10
        percent_end = 99 - i*10
        rand_percent1 = str(random.randrange(percent_start, percent_end))
        rand_percent2 = str(random.randrange(percent_start, percent_end))
        output_str += "{num}. Check out **{name}** on the Google Playstore : [link](https://www.youtube.com/watch?v=dQw4w9WgXcQ) | ".format(num=i+1, name=names[names_idx[i]]) +\
                      "{pct1}.{pct2} % match. \n".format(pct1=rand_percent1, pct2=rand_percent2)

    output_str += "\n\n"

    # ios apps
    output_str += "**iOS apps**\n\n"

    for i in range(ios_num):
        percent_start = 90 - i*10
        percent_end = 99 - i*10
        rand_percent1 = str(random.randrange(percent_start, percent_end))
        rand_percent2 = str(random.randrange(percent_start, percent_end))
        output_str += "{num}. Check out **{name}** on the Apple app store : [link](https://www.youtube.com/watch?v=dQw4w9WgXcQ) | ".format(num=i+1, name=names[names_idx[i+android_num]]) +\
                      "{pct1}.{pct2} % match. \n".format(pct1=rand_percent1, pct2=rand_percent2)

    output_str += "\n\n"

    # final line showing indexed apps
    output_str += "**Searched Apps**: {imgs} | **Indexed Apps**: {posts} | **Search Time**: {rand_time} \n\n".format(imgs=rand_imgs, posts=rand_posts, rand_time=rand_time) +\
                  "*Feedback? Hate? Visit [r/app-finder-bot](https://www.youtube.com/watch?v=6n3pFFPSlW4) - I\'m not perfect, but you can help. Report [ [False Positive](https://www.youtube.com/watch?v=d1YBv2mWll0) ]*"

    return output_str


def check_if_app_suggestion_needed(post_body):
    """
    Checks if given post satisfies constraints
    Expects lowercase string
    Looks for the phrases :
        (app OR application OR tool) AND (recommend  OR suggest OR recommendation)
    """
    word_list = re.sub("[^\w]", " ",  post_body).split()
    if "app" in word_list or "application" in word_list or "tool" in word_list:
        if "recommend" in word_list or "suggest" in word_list or "recommendation" in word_list:
            return True

    return False


def reply_to_particular_post(post_url):
    """
    Replies to a particular post with app link
    """
    post = reddit.submission(url=post_url)
    post.reply(generate_message())



def reply_to_all_posts():
    """
    Replies in rickroll to all possible comments which match criteria
    """
    for post in subreddit.hot(limit=5):
        if check_if_app_suggestion_needed(post.selftext.lower()):
            post.reply(generate_message())
            print("Replied to https://www.reddit.com" + post.permalink)
    return


if __name__ == "__main__": 
    reply_to_all_posts()