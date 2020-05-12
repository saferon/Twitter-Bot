import tweepy
import time
import random
import os
import threading
import datetime
import json

with open('keys.json', 'r') as keys:
    keys_dict = json.load(keys)

auth = tweepy.OAuthHandler(keys_dict["api"], keys_dict["secret"])
auth.set_access_token(keys_dict["auth"], keys_dict["authsec"])

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

try:
    api.verify_credentials()
    print("Tweet bot online.")
except:
    print("Error during authentication")

user = api.me()

path_to_images = '/media/pi/8A02-DF82/wjsn/'

def follow_back():
    threading.Timer(300.0, follow_back).start()  # sets timing for checking for followers
    for follower in tweepy.Cursor(api.followers).items():
        try:
            follower.follow()
            print("followed:" + str(follower.screen_name))
        except:
            pass


def tweet_random_image():
    """tweet random picture with the name of who is in the picture"""
    threading.Timer(3600.0, tweet_random_image).start()  # sets timing for tweets
    paths = []
    # list out all of the directories of the path
    for directory in os.listdir(path_to_images):
        paths.append(directory)  # append these directories to the list paths

    alpha = random.choice(paths)
    beta = os.listdir(path_to_images + alpha + '/')
    beta_refined = []
    for images in beta:
        with open('wjsn_paths.json', 'r') as used_paths:
            used_paths_list = json.load(used_paths)
        if ".webm" not in images and ".mp4" not in images and ".gif" not in images and ".ini" not in images:
            if path_to_images + alpha + images not in used_paths_dict["list"]:
                beta_refined.append(images)
                used_paths_list.append(path_to_images + alpha + images)  # add full file name for duplicate file names in different directories
                with open('wjsn_paths', 'w') as pathdump:
                    json.dump(used_paths_list, pathdump)

    gamma = random.choice(beta_refined)
    delta = path_to_images + alpha + '/' + gamma
    if alpha == "wjsn":
        api.update_with_media(delta, '#WJSN #우주소녀')
    else:
        api.update_with_media(delta, '#WJSN #우주소녀 #' + alpha.title())
    print("tweeted " + delta + " at " + str(datetime.datetime.now()))

tweet_random_image()
follow_back()

