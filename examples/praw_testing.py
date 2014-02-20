# SET THE FOLLOWING EITHER BEFORE RUNNING THIS FILE OR BELOW, BEFORE INITIALIZING
#    PRAW!

# set variables for interacting with reddit.
# my_user_agent = ""
# my_username = ""
# my_password = ""
# reddit_post_id = -1


# import praw - install: pip install praw
# Praw doc: https://praw.readthedocs.org/en/latest/index.html
import praw

# python base imports
import datetime
import pprint

# import python_utilities
from python_utilities.logging.summary_helper import SummaryHelper

# declare variables.
my_summary_helper = None
r = None
post = None
comments = None
flat_comments = None
test_comment = None
comment_prop_map = None
summary_string = ""

# set variables for interacting with reddit.
my_user_agent = "<user_agent>"
my_username = "<reddit_username>"
my_password = "<reddit_password>"
#reddit_post_id = "1cp0i3"
reddit_post_id = "1bvkol"

# init summary helper.
my_summary_helper = SummaryHelper()

print( "Starting PRAW test at " + str( start_dt ) )

# set user agent.
r = praw.Reddit( user_agent = my_user_agent )

# got login set?
if ( ( ( my_username ) and ( my_username != "" ) ) and ( ( my_password ) and ( my_password != "" ) ) ):

    # yes.  Login.
    r.login( my_username, my_password )

    print( "==> Logged in." )

#-- END check to see if we log in. --#

print( "==> Created reddit instance." )

# retrieve post 
# - post with lots of comments - 1bvkol has 22014
#reddit_post_id = "1bvkol"
post = r.get_submission( submission_id = reddit_post_id, comment_limit = 1500, comment_sort = "old" )

print( "Retrieved post " + str( reddit_post_id ) )

# output number of comments based on post
print( "==> post.permalink: " + post.permalink )
print( "==> post.num_comments: " + str( post.num_comments ) )

# use the replace_more_comments() method to pull in as many comments as possible.
post.replace_more_comments( limit = None, threshold = 0 )

print( "==> After replace_more_comments()" )

# get the comments
comments = post.comments

# print out number of comments
print( "==> len( comments ): " + str( len( comments ) ) ) # 3,915 and counting

# these are objects where parent comments reference children.  flatten...
flat_comments = praw.helpers.flatten_tree( post.comments )

# how many now?
print( "==> after flatten_tree(), comment count: " + str ( len( flat_comments ) ) ) # 13364 - closer to 22000, but still not all of them.

# get a comment
test_comment = flat_comments[ 0 ]

print( "Looking at comment 0:")

# what is in it?
print( "==> str( comment ): " + str( test_comment ) ) # outputs the text of comment, nothing more.

# reddit ID of comment:
print( "==> comment id: " + str( test_comment.id ) )

# body of comment
print( "==> comment body: " + test_comment.body )

# to get map of property names to values in a praw object:
comment_prop_map = vars( test_comment )

# pretty-print it with pprint library.
pprint.pprint( comment_prop_map )

'''
Example:
{'_info_url': 'http://www.reddit.com/api/info/',
 '_replies': [<praw.objects.MoreComments object at 0x4867550>],
 '_submission': <praw.objects.Submission object at 0x4867790>,
 '_underscore_names': ['replies'],
 'approved_by': None,
 'author': Redditor(user_name='worldclasssteez'),
 'author_flair_css_class': None,
 'author_flair_text': None,
 'banned_by': None,
 'body': u'Using the "J" and "K" keys on VLC player to sync up the audio. ',
 'body_html': u'&lt;div class="md"&gt;&lt;p&gt;Using the &amp;quot;J&amp;quot; and &amp;quot;K&amp;quot; keys on VLC player to sync up the audio. &lt;/p&gt;\n&lt;/div&gt;',
 'created': 1365399487.0,
 'created_utc': 1365395887.0,
 'distinguished': None,
 'downs': 44,
 'edited': False,
 'gilded': 0,
 'has_fetched': True,
 'id': u'c9ap3fp',
 'json_dict': None,
 'likes': None,
 'link_id': u't3_1bvkol',
 'name': u't1_c9ap3fp',
 'num_reports': None,
 'parent_id': u't3_1bvkol',
 'reddit_session': <praw.Reddit object at 0x48539d0>,
 'saved': False,
 'score_hidden': False,
 'subreddit': Subreddit(display_name='AskReddit'),
 'subreddit_id': u't5_2qh1i',
 'ups': 201}
'''

# each name in that map can be invoked as a variable on the object itself.

# test summary counter
my_summary_helper.set_prop_value( "comment_count", 0 )


# look at utc date order of comments:
# for comment in flat_comments[ 0:15 ]:
for index in range( 0, len( flat_comments ) ):

    # get vars
    comment = flat_comments[ index ]
    comment_prop_map = vars( comment )
    created_from_map = comment_prop_map[ 'created_utc' ]
    created_from_obj = comment.created_utc
    created_dt = datetime.datetime.fromtimestamp( created_from_map )
    comment_id = comment.name
    print( "==> " + str( index ) + " ( " + comment_id + " ) - Created UTC: " + str( created_from_map ) + " (map); " + str( created_from_obj ) + " (obj); " + str( created_dt ) )

    # increment comment count
    my_summary_helper.increment_prop_value( "comment_count" )

#-- END loop over comments --#

print( "==> Created: " + str( created_from_map ) + " (map); " + str( created_from_obj ) + " (obj); " + str( created_dt ) )

summary_string = "\nPRAW testing complete!\n"

# generate summary string

# set stop time.
my_summary_helper.set_stop_time()

# generate summary string.
summary_string += my_summary_helper.create_summary_string( item_prefix_IN = "==> " )
print( summary_string )