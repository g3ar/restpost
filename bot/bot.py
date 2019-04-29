#!/usr/bin/env python

import requests
import configparser
from random import randint, shuffle
import hashlib
import time

config = configparser.ConfigParser()
config.read('config.ini')
root_url = 'http://127.0.0.1:8000/'
number_of_users = int(config['bot']['number_of_users'])
max_posts_per_user = int(config['bot']['max_posts_per_user'])
max_likes_per_user = int(config['bot']['max_likes_per_user'])


def signup_user(user_postfix):
    username = f"test_{user_postfix}"
    password = "123qweasd"
    email = f"{username}@test.com"
    requests.post(
        f"{root_url}auth/signup/",
        data={
            'username': username,
            'password': password,
            'email': email
        }
    )
    return (username, password, email)


def get_jwt_token(user_postfix):
    r = requests.post(
        f"{root_url}jwt/get/",
        data={
            'username': f"test_{user_postfix}",
            'password': "123qweasd",
        }
    )
    return r.json()['token']


def post(token, user_postfix):
    r = requests.post(
        f"{root_url}api/posts/",
        data={
            'title': f"Title {user_postfix}",
            'text': f"Text {user_postfix}",
        },
        headers={
            'Authorization': f"JWT {token}"
        }
    )
    return r.json()['id']


def like(token, post_id):
    r = requests.post(
        f"{root_url}api/likes/",
        data={
            'post': post_id,
        },
        headers={
            'Authorization': f"JWT {token}"
        }
    )
    return r.json()['id']


def get_timestamp_md5():
    m = hashlib.md5()
    m.update(str(time.time()).encode())
    return m.hexdigest()


posts = []
for x in range(0, number_of_users):
    user_postfix = get_timestamp_md5()
    signup_user(user_postfix)
    print(f"User with postfix {user_postfix} created")
    user_post_num = randint(0, max_posts_per_user)
    print(f"Creating {user_post_num} posts")
    token = get_jwt_token(user_postfix)
    for p in range(0, user_post_num):
        post_id = post(token, user_postfix)
        posts.append(post_id)
        print(f"Post creted with id: {post_id}")
    user_likes_num = randint(0, max_likes_per_user)
    shuffle(posts)
    for l in range(0, user_likes_num):
        like_id = like(token, posts[l])
        print(f"Like creted with id: {like_id}")
