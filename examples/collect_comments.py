# import the RedditCollector class
from reddit_collect.redditCollector import RedditCollector

# make an instance
reddit_collector = RedditCollector()

# initialize bare minimum connection parameters.
reddit_collector.user_agent = "reddit comment collector v0.1 by /u/jonathan_morgan"

# optional - if your version of mysql doesn't support utf8mb4 (unicode
#    characters greater than 3-bytes), set this to true and it will keep all
#    unicode characters 3 bytes and less, turn those that are 4 bytes long
#    into XML entities, so they are preserved, but don't break database.
# set to escape 4-byte Unicode characters (cursed mysql).
reddit_collector.convert_4_byte_unicode_to_entity = True

# first, retrieve one or more posts from database using Django QuerySets
# - https://docs.djangoproject.com/en/dev/ref/models/querysets/
import reddit_collect.models
post_qs = reddit_collect.models.Post.objects.filter( num_comments__gt = 0 )

# pass the QuerySet to the collect_comments() method.
reddit_collector.collect_comments( post_qs )