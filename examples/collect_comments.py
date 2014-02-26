# import the RedditCollector class
from reddit_collect.redditCollector import RedditCollector

# initialize variables
reddit_collector = None
my_user_agent = ""
my_username = ""
my_password = ""
smtp_host = ""
smtp_port = -1
smtp_use_ssl = False
smtp_username = ""
smtp_password = ""

# variables for looking up posts to collect comments for.
matching_subreddit_qs = None
subreddit_id_list = None
post_qs = None
ordered_post_qs = None

# make a collector instance
reddit_collector = RedditCollector()

# configure reddit connection
my_user_agent = "<user_agent>"
my_username = "<reddit_username>"
my_password = "<reddit_password>"

# initialize connection parameters.
reddit_collector.user_agent = my_user_agent
reddit_collector.username = my_username
reddit_collector.password = my_password

# set collector to output details
reddit_collector.do_output_details = False

# optional - if your version of mysql doesn't support utf8mb4 (unicode
#    characters greater than 3-bytes), set this to true and it will keep all
#    unicode characters 3 bytes and less, turn those that are 4 bytes long
#    into XML entities, so they are preserved, but don't break database.
#    Not needed for PostgreSQL.
# set to escape 4-byte Unicode characters (cursed mysql).
#reddit_collector.convert_4_byte_unicode_to_entity = True

# initialize email helper and status helper.
'''
smtp_host = "localhost"
smtp_port = -1
smtp_use_ssl = FalseTrue
smtp_username = ""
smtp_password = ""
'''
# If using SSL on port 587, and you get this error:
#     ssl.SSLError: [Errno 1] _ssl.c:504: error:140770FC:SSL routines:SSL23_GET_SERVER_HELLO:unknown protocol
# use port 465 rather than 587.
# - http://stackoverflow.com/questions/12854572/connect-to-smtp-ssl-or-tls-using-python
smtp_host = "<smtp_host>"
smtp_port = 465
smtp_use_ssl = True
smtp_username = "<smtp_username>"
smtp_password = "<smtp_password>"
reddit_collector.email_initialize( smtp_host_IN = smtp_host, smtp_port_IN = smtp_port, smtp_use_ssl_IN = smtp_use_ssl, smtp_username_IN = smtp_username, smtp_password_IN = smtp_password )

# set email address to which status updates will be sent.
reddit_collector.set_email_status_address( "<email_address>" )

# test sending email status (from and to the email_status_address).
#reddit_collector.email_send_status( "test message", "test subject" )

# first, retrieve one or more posts from database using Django QuerySets
# - https://docs.djangoproject.com/en/dev/ref/models/querysets/
import reddit_collect.models

# get all posts where the related subreddit has filter_1 = True.
#matching_subreddit_qs = reddit_collect.models.Subreddit.objects.filter( filter_1 = True ).values( 'id' )

# get all posts where the related subreddit has filter_2 = True AND filter_1 = False.
matching_subreddit_qs = reddit_collect.models.Subreddit.objects.filter( filter_2 = True )
matching_subreddit_qs = matching_subreddit_qs.filter( filter_1 = False )
matching_subreddit_qs = matching_subreddit_qs.values( 'id' )

# retrieve post query set
post_qs = reddit_collect.models.Post.objects.filter( subreddit_id__in = matching_subreddit_qs )

# OR less fancy
#subreddit_id_list = [ 't5_2qh1o', 't5_2t22d', 't5_2qh2p', 't5_2qh13', 't5_2r9vp', 't5_2tqat', 't5_2r84s', 't5_2s7tt', 't5_2qh1e', 't5_2rfxx', 't5_2qpp6', 't5_2s3qj', 't5_2qh03', 't5_2qh0u', 't5_2qh61', 't5_2qh1i' ]
#post_qs = reddit_collect.models.Post.objects.filter( subreddit_reddit_id__in = subreddit_id_list )

# limit to num_comments >= 10
post_qs = post_qs.filter( num_comments__gte = 10 )

# limit to num_comments <= 1500
post_qs = post_qs.filter( num_comments__lte = 1500 )

# limit to just those we haven't collected comments on yet.
#post_qs = post_qs.filter( comment_collection_status = "new" )

# order by number of comments, DESC
post_qs = post_qs.order_by( "-num_comments" )

# limit? to first 5...
post_qs = post_qs[ :5 ]

# OR don't
#post_qs = ordered_post_qs

# pass the QuerySet to the collect_comments() method.

# update existing (still defaults to using bulk create for any new records).
reddit_collector.collect_comments( posts_qs_IN = post_qs, do_update_existing_IN = True )

# don't update existing
#reddit_collector.collect_comments( posts_qs_IN = post_qs, do_update_existing_IN = False )