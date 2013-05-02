# run within ipython (started using "python manage.py shell") using "%run testing.py"

# import the RedditCollector class
from reddit_collect.redditCollector import RedditCollector

# make an instance
reddit_collector = RedditCollector()

# initialize bare minimum connection parameters.
reddit_collector.user_agent = "reddit comment collector v0.1 by /u/jonathan_morgan"

import reddit_collect.models
post_qs = reddit_collect.models.Post.objects.filter( reddit_id = '1cp0i3' )

# num_comments?
django_post = post_qs[ 0 ]
print( django_post.num_comments ) # 115, at time of collection
    
# pass the QuerySet to the collect_comments() method.
reddit_collector.collect_comments( post_qs )

# refresh post.
django_post = reddit_collect.models.Post.objects.get( reddit_id = '1cp0i3' )

# get reddiwrap post, so we can pull comments from reddit.
comment_rw_post = django_post.create_reddiwrap_post()

# get reddiwrap instance
reddiwrap = reddit_collector.create_reddiwrap_instance()

# fetch comments
reddiwrap.fetch_comments( comment_rw_post )

# get top-level comments
top_comments = comment_rw_post.comments

# print top-level comment count
print( "top-level comment count: " + str ( len( top_comments ) ) )

# get first comment
top_comment_1 = top_comments[ 0 ]

# loop over all the top_comments, outputting id, user, score.
for comment in top_comments:

    print( "- comment " + comment.id + " - by " + comment.author + " - score: " + str( comment.score ) + "; up = " + str( comment.upvotes ) + "; down = " + str( comment.downvotes ) + " - child count: " + str( len( comment.children ) ) )

    if ( len( comment.children ) > 0 ):

        for child_comment in comment.children:

            print( "    - comment " + child_comment.id + " - by " + child_comment.author + " - score: " + str( child_comment.score ) + "; up = " + str( child_comment.upvotes ) + "; down = " + str( child_comment.downvotes ) + " - child count: " + str( len( child_comment.children ) ) )

            if ( len( child_comment.children ) > 0 ):
            
                for child_comment_2 in child_comment.children:
                
                    print( "        - comment " + child_comment_2.id + " - by " + child_comment_2.author + " - score: " + str( child_comment_2.score ) + "; up = " + str( child_comment_2.upvotes ) + "; down = " + str( child_comment_2.downvotes ) + " - child count: " + str( len( child_comment_2.children ) ) )
        
                    if ( len( child_comment_2.children ) > 0 ):
                    
                        for child_comment_3 in child_comment_2.children:
                        
                            print( "            - comment " + child_comment_3.id + " - by " + child_comment_3.author + " - score: " + str( child_comment_3.score ) + "; up = " + str( child_comment_3.upvotes ) + "; down = " + str( child_comment_3.downvotes ) + " - child count: " + str( len( child_comment_3.children ) ) )
                
                            if ( len( child_comment_3.children ) > 0 ):
                            
                                for child_comment_4 in child_comment_3.children:

                                    print( "                - comment " + child_comment_4.id + " - by " + child_comment_4.author + " - score: " + str( child_comment_4.score ) + "; up = " + str( child_comment_4.upvotes ) + "; down = " + str( child_comment_4.downvotes ) + " - child count: " + str( len( child_comment_4.children ) ) )
                        
                                    if ( len( child_comment_4.children ) > 0 ):

                                        print( "And there's more!" )                                    

                                    #-- END check to see if child comments --#

                                #-- END loop over child comments four levels deep. --#
                                
                            #-- END check to see if child comments --#
                            
                        #-- END loop over child comments at level 3 --#
        
                    #-- END check to see if child comments --#
                    
                #-- END loop over child coments at level 1 --#

            #-- END check to see if child comments --#
        
        #-- END look over level 1 child comments --#

    #-- END check for child comments --#

#-- END loop over top-level comments --#

'''
Collected comments for /r/boston
==> Posts passed in: 2421
==> Posts processed: 2421
==> Comments created: 17448
==> Collection started: 2013-04-28 13:37:49.949195
==> Collection ended: 2013-04-28 15:00:38.835510
==> Duration: 1:22:48.886315
'''

