# run within ipython (started using "python manage.py shell") using "%run testing.py"

# import the RedditCollector class
from reddit_collect.redditCollector import RedditCollector

# python standard library imports
import datetime

# import python_utilities
from python_utilities.logging.summary_helper import SummaryHelper

# import reddit_collect models.
import reddit_collect.models

# declare variables
my_summary_helper = None
summary_string = ""
my_user_agent = "<user_agent>"
my_username = "<reddit_username>"
my_password = "<reddit_password>"
reddit_collector = None
post_qs = None
django_post = None
comment_rw_post = None
reddiwrap = None
top_comments = None

# init connection information

# BEFORE RUNNING, SET reddit_post_id
#reddit_post_id = '1cp0i3' # 113
reddit_post_id = '1d67nv' # 569
print( "testing post " + reddit_post_id )

#================================================================================
# collect comments using RedditCollector
#================================================================================

# make an instance
reddit_collector = RedditCollector()

# initialize connection parameters.
reddit_collector.user_agent = my_user_agent
reddit_collector.username = my_username
reddit_collector.password = my_password

# set collector to output details
reddit_collector.do_output_details = False

# set bulk collection flag (defaults to True)
#reddit_collector.do_bulk_create = False

# initialize summary helper
my_summary_helper = SummaryHelper()

# get post QuerySet
#post_qs = reddit_collect.models.Post.objects.filter( reddit_id = reddit_post_id )
post_qs = reddit_collect.models.Post.objects.filter( reddit_id__in = [ '1cp0i3', '1d67nv' ] )

# num_comments?
django_post = post_qs[ 0 ]
print( "==> num_comments: " + str( django_post.num_comments ) ) # 115, at time of collection

my_summary_helper.set_prop_value( "num_comments", django_post.num_comments )
my_summary_helper.set_prop_desc( "num_comments", "num_comments (post)" )
    
# pass the QuerySet to the collect_comments() method.
reddit_collector.collect_comments( post_qs )

#================================================================================
# Now, compare collect_comments() output to just grabbing comments with reddiwrap
#================================================================================

# refresh post.
# reddit_post_id = '1cp0i3'
django_post = reddit_collect.models.Post.objects.get( reddit_id = reddit_post_id )

# get reddiwrap post, so we can pull comments from reddit.
comment_rw_post = django_post.create_reddiwrap_post()

# get reddiwrap instance
reddiwrap = reddit_collector.create_reddiwrap_instance()

# fetch comments
reddiwrap.fetch_comments( comment_rw_post, limit = 1500 )

# get top-level comments
top_comments = comment_rw_post.comments

# print top-level comment count
print( "==> top-level comment count: " + str ( len( top_comments ) ) )

# get first comment
top_comment_1 = top_comments[ 0 ]

# make recursive function to count total comments.
def count_comments( comment_list_IN = None, indent_IN = "" ):
    
    # return reference
    count_OUT = -1
    
    # declare variables
    comment = None

    # loop over comments in list
    count_OUT = 0
    for comment in comment_list_IN:
    
        # increment counter
        count_OUT += 1
        
        # print comment summary
        created_from_obj = comment.created_utc
        created_dt = datetime.datetime.fromtimestamp( created_from_obj )
        print( indent_IN + "- comment " + comment.id + " - created " + str( created_dt ) + " - by " + comment.author + " - score: " + str( comment.score ) + "; up = " + str( comment.upvotes ) + "; down = " + str( comment.downvotes ) + " - child count: " + str( len( comment.children ) ) )
        
        # see if comment has children
        if ( len( comment.children ) > 0 ):
        
            # yes, there are children.  Recurse!
            count_OUT += count_comments( comment_list_IN = comment.children, indent_IN = indent_IN + "    " )

        #-- END check to see if children --#
    
    #-- END loop over comments. --#
    
    return count_OUT
    
#-- END function count_comments() --#

# count comments
comment_count = count_comments( comment_list_IN = top_comments )
my_summary_helper.set_prop_value( "comment_count", comment_count )
my_summary_helper.set_prop_desc( "comment_count", "Comment Count" )

# set stop time.
my_summary_helper.set_stop_time()

# generate summary string.
summary_string += my_summary_helper.create_summary_string( item_prefix_IN = "==> " )
print( summary_string )


'''
Collected comments for /r/boston
==> Posts passed in: 2421
==> Posts processed: 2421
==> Comments created: 17448
==> Collection started: 2013-04-28 13:37:49.949195
==> Collection ended: 2013-04-28 15:00:38.835510
==> Duration: 1:22:48.886315
'''