# import the RedditCollector class
from reddit_collect.redditCollector import RedditCollector

# make an instance
reddit_collector = RedditCollector()

# initialize bare minimum connection parameters.
reddit_collector.user_agent = "reddit post collector v0.1 by /u/jonathan_morgan"

# OR reddit_collector.user_agent = "reddit comment collector v0.1 by /u/jonathan_morgan"

# optional, if you need to log in:
#reddit_collector.username = "<reddit_username>"
#reddit_collector.password = "<reddit_password>"

# optional - also can set path to store cookies, if you want to persist them.
reddit_collector.cookie_file_path = "cookies.txt"

# optional - if your version of mysql doesn't support utf8mb4 (unicode
#    characters greater than 3-bytes), set this to true and it will keep all
#    unicode characters 3 bytes and less, turn those that are 4 bytes long
#    into XML entities, so they are preserved, but don't break database.
# set to escape 4-byte Unicode characters (cursed mysql).
reddit_collector.convert_4_byte_unicode_to_entity = True

#============================================================================
# ==> Collect Posts
#============================================================================

# collect latest 10 entries from /r/all, store them in database.
#reddit_collector.collect_posts( 10 )

# collect posts until you get to ID t3_1d64j4
#reddit_collector.collect_posts( -1, "t3_1d64j4" )

# OR, posts through ID t3_1d68lz
#reddit_collector.collect_posts( until_id_IN = "t3_1d68lz" )

# collect posts through date - start of 2013/04/26
#boundary_date = datetime.datetime( 2013, 4, 26, 0, 0, 0, 0 )
#reddit_collector.collect_posts( until_date_IN = boundary_date )

# in the event of a crash, find ID of last record retrieved, then combine
#    arguments to pick up where you left off.
#reddit_collector.collect_posts( until_date_IN = boundary_date, after_id_IN = "t3_1d63sm" )

# or combine to test - just 350 posts, no more.
#reddit_collector.collect_posts( post_count_limit_IN = 350, after_id_IN = "t3_1d4wyy" )

# just grab 300 posts, update if already in the database.
#reddit_collector.collect_posts( post_count_limit_IN = 300, after_id_IN = "t3_1dk89v", do_update_existing_IN = True )

# update existing posts after a certain ID until a certain datetime.
boundary_date = datetime.datetime( 2013, 4, 1, 0, 0, 0 )

# first, just try 300.
reddit_collector.collect_posts( until_date_IN = boundary_date, after_id_IN = "t3_1dk89v", do_update_existing_IN = True, post_count_limit_IN = 300 )