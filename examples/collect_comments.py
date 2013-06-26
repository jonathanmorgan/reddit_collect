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
smtp_host = "<smtp_server>"
smtp_port = 465
smtp_use_ssl = True
smtp_username = "<username>"
smtp_password = "<password>"
reddit_collector.email_initialize( smtp_host_IN = smtp_host, smtp_port_IN = smtp_port, smtp_use_ssl_IN = smtp_use_ssl, smtp_username_IN = smtp_username, smtp_password_IN = smtp_password )

# set email address to which status updates will be sent.
reddit_collector.set_email_status_address( "jonathan.morgan.007@gmail.com" )

# test sending email status (from and to the email_status_address).
#reddit_collector.email_send_status( "test message", "test subject" )

# first, retrieve one or more posts from database using Django QuerySets
# - https://docs.djangoproject.com/en/dev/ref/models/querysets/
import reddit_collect.models

# get all posts where num_comments is greater than 0.
post_qs = reddit_collect.models.Post.objects.filter( num_comments__gt = 0 )

# order by number of comments, DESC
ordered_post_qs = post_qs.order_by( "-num_comments" )

# limit? to first 5...
post_qs = ordered_post_qs[ :5 ]

# pass the QuerySet to the collect_comments() method.

# update existing (one update per comment, instead of batch inserts - makes it slower?)
#reddit_collector.collect_comments( posts_qs_IN = post_qs, do_update_existing_IN = True )

# don't update existing
reddit_collector.collect_comments( posts_qs_IN = post_qs, do_update_existing_IN = False )