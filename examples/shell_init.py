# run within ipython (started using "python manage.py shell") using "%run testing.py"

# imports
import datetime
import sys

# import the RedditCollector class
from reddit_collect.redditCollector import RedditCollector

# import reddit_collect models.
import reddit_collect.models

# make an instance
reddit_collector = RedditCollector()

# initialize bare minimum connection parameters.
reddit_collector.user_agent = "reddit comment collector v0.1"

# set to escape 4-byte Unicode characters (cursed mysql).
reddit_collector.convert_4_byte_unicode_to_entity = True

# get reddiwrap instance
reddiwrap = reddit_collector.create_reddiwrap_instance()
