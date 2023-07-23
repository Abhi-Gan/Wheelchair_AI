# TODO: actually complete 
from dotenv import load_dotenv
import os

load_dotenv()
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")

import praw

reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent="extractor by u/silversur4_",
)


def get_top_n_reddit(n=10, subreddit="wheelchairs"):
    submissions = reddit.subreddit(subreddit).hot(limit=n)
    return [{"submission":subm.title, "url":subm.url} for subm in submissions]