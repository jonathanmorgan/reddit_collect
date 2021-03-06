# imports
import datetime
import gc

# django imports
import django.db

# import python_utilities
from python_utilities.logging.summary_helper import SummaryHelper

# TODO - see if using the QuerySetHelper.queryset_generator() helps.
#from python_utilities.django_utils.queryset_helper import QuerySetHelper

# import reddit_collect models.
import reddit_collect.models

# declare variables
my_summary_helper = None
slice_size = -1
comment_qs = None
query_set_helper = None
comment_qs_iterator = None
total_comment_count = -1
comment_count = -1
comment_counter = -1
aggregate_counter = -1
overall_progress_summary = ""
output_details = True

comment = None
related_post = None
related_subreddit = None
summary_string = ""

# init summary helper
my_summary_helper = SummaryHelper()

# set slice size
slice_size = 10000

# 10000 - want to maximize work done between queries, but not do so much that you
#    cause slowdown, or have the result set so large that python and django have
#    trouble with loading all the objects into memory.  100 or 10 were too few
#    (too little work between queries).  1000 was OK, but I think still not
#    enough work between query calls.

# retrieve comments that don't have a related subreddit.
comment_qs = reddit_collect.models.Comment.objects.filter( subreddit = None ) 

# get count of comments.
comment_count = comment_qs.count()
total_comment_count = comment_count

print( "- " + str( datetime.datetime.now() ) + " - After initial filtering - total count = " + str( total_comment_count ) )

# while loop for testing.
#while ( ( comment_count > 0 ) and ( aggregate_counter < 101 ) ):

# keep looping while count is greater than 0
aggregate_counter = 0
while ( comment_count > 0 ):

    # create current overall progress summary.
    overall_progress_summary = "( " + str( aggregate_counter ) + " done, " + str( comment_count ) + " left of " + str( total_comment_count ) + " )"
    
    # limit to ten or less
    if ( comment_count > slice_size ):
    
        # comment count is 10 or greater - slice down to slice_size.
        comment_qs = comment_qs[ :slice_size ]
        
    #-- END check to see how few we limit to --#

    # loop over current set of comments
    comment_counter = 0
    for comment in comment_qs:
    
        # increment counter
        comment_counter += 1
    
        # print details?
        if ( output_details == True ):
        
            print( "==> " + str( comment_counter ) + " of " + str( slice_size ) + " " + overall_progress_summary + " - " + str( datetime.datetime.now() ) + " - " + str( comment ) )
            
        #-- END check to see if we output details. --#
        
        # see if there is an associated post.
        if ( ( comment.post ) and ( comment.post is not None ) ):
    
            # store reference to post.
            related_post = comment.post
    
            # does the post reference a subreddit?
            if ( ( related_post.subreddit ) and ( related_post.subreddit is not None ) ):
            
                # yes - put reference to it in comment.
                comment.subreddit = related_post.subreddit
                
                # save the comment.
                comment.save()
            
            #-- END check to see if post has a subreddit. --#
            
        #-- END check to see if related post passed in. --#
    
    #-- END loop over comments. --#
    
    # update aggregate counter
    aggregate_counter += comment_counter

    # memory management
    gc.collect()
    django.db.reset_queries()

    # do query again to see if more to process.
    comment_qs = reddit_collect.models.Comment.objects.filter( subreddit = None ) 

    # get count of comments.
    comment_count = comment_qs.count()

    print( " - Bottom of loop - After count() - processed " + str( aggregate_counter ) + " of " + str( total_comment_count ) + " - " + str( comment_count ) + " to go - " + str( datetime.datetime.now() ) )

#-- END loop over all comments. --#

# set stop time.
my_summary_helper.set_stop_time()

# set aggregate comment counter
my_summary_helper.set_prop_value( "aggregate_comment_count", aggregate_counter )
my_summary_helper.set_prop_desc( "aggregate_comment_count", "Comments Processed" )

# generate summary string.
summary_string += my_summary_helper.create_summary_string( item_prefix_IN = "==> " )
print( summary_string )