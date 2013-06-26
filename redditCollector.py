'''
Copyright 2012, 2013 Jonathan Morgan

This file is part of http://github.com/jonathanmorgan/reddit_collect.

reddit_collect is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

reddit_collect is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with http://github.com/jonathanmorgan/reddit_collect. If not, see http://www.gnu.org/licenses/.
'''

#!/usr/bin/python

#================================================================================
# imports
#================================================================================

# base python libraries
import datetime
import gc
import sys
import time

# django imports
import django.db

# site-specific imports.
#site_path = '/home/socs/socs_reddit/'
#if site_path not in sys.path:
#    sys.path.append( site_path )

#import myLib
import reddit_collect.models

# python_utilities
from python_utilities.email.email_helper import EmailHelper
from python_utilities.exceptions.exception_helper import ExceptionHelper
from python_utilities.rate_limited.basic_rate_limited import BasicRateLimited
from python_utilities.strings.string_helper import StringHelper

# ReddiWrapper
from reddiwrap.ReddiWrap import ReddiWrap


#================================================================================
# class RedditCollector
#================================================================================

class RedditCollector( BasicRateLimited ):


    #============================================================================
    # CONSTANTS-ish
    #============================================================================


    STATUS_SUCCESS = "Success!"
    STATUS_PREFIX_ERROR = "ERROR: "
    
    # DEBUG - changed to instance variable.
    #DEBUG_FLAG = False


    #============================================================================
    # instance variables
    #============================================================================


    reddiwrap_instance = None
    user_agent = ""
    username = ""
    password = ""
    cookie_file_path = ""
    
    # email helpers.
    email_helper = None
    email_status_address = ""
    
    # rate limiting - in parent class BasicRateLimited.
    #do_manage_time = True
    #rate_limit_in_seconds = 2
    #request_start_time = None
    
    # performance
    do_bulk_create = True
    
    # encoding, to deal with utf8 in mysql actually just allowing for up to
    #    3-byte unicode characters, not all (4-byte and above).
    convert_4_byte_unicode_to_entity = False
    
    # error handling
    error_limit_count = 10
    exception_helper = ExceptionHelper()
    
    # debug_flag
    debug_flag = False
    
    
    #---------------------------------------------------------------------------
    # __init__() method
    #---------------------------------------------------------------------------

    
    def __init__( self ):
        
        '''
        Constructor
        '''
        
        # instance variables
        self.reddiwrap_instance = None
        self.user_agent = ""
        self.username = ""
        self.password = ""
        self.cookie_file_path = ""
        
        # flag to say if this instance should manage time.
        self.do_manage_time = True
        self.rate_limit_in_seconds = 2
        self.request_start_time = None
        
        # performance
        self.do_bulk_create = True
        
        # encoding
        self.convert_4_byte_unicode_to_entity = True
        
        # email
        self.email_helper = None
        self.email_status_address = ""
        
        # error handling
        self.error_limit_count = 10
        self.exception_helper = ExceptionHelper()
        
        # debug
        self.debug_flag = False

    #-- END constructor --#


    #============================================================================
    # instance methods
    #============================================================================
    

    def collect_comments( self, 
                          posts_qs_IN = None,
                          do_update_existing_IN = False,
                          *args,
                          **kwargs ):
    
        '''
        This method accepts a QuerySet of django reddit_collect Post() instances
           for which you want to collect comments.  Uses ReddiWrapper to do the
           actual retrieval, then stores them off in database using django.
           
        Parameters:
        - posts_qs_IN - defaults to None.  QuerySet containing posts you want to collect comments for.  If None, will collect for all posts in database whose comment status is not "done".
        - do_update_existing_IN - Boolean, True if we want to update existing comments that are already in the database, false if not.  Defaults to False.
           
        Postconditions: Stores comments for each post to database using django
           model classes.  Returns a status message.
           
        # Original Code
		posts =  myLib.posts_of_reddit(subreddit.name); # corrent

		print "saving Comments ... ";
		i = 0;
		for post in posts:
			pst = myLib.make_post_obj(post);
			reddit.fetch_comments(pst);
			myLib.iterate_comments(pst.comments); # iterates and save comments
			time.sleep(1);
			i = i + 1;
			print i;
                   
        '''

        # return reference
        status_OUT = self.STATUS_SUCCESS
        
        # declare variables
        me = "collect_comments"
        reddiwrap = None
        posts_to_process_qs = None
        post_count = -1
        current_post = None
        post_counter = -1
        continue_collecting = True
        current_rw_post = None
        do_update_existing = False
        
        # variables for dealing with intermittent connection problems.
        comments_collected = False
        connection_error_count = -1
        temp_exception_string = ""
        exception_details = ""
        exception_message = ""
        error_email_subject = ""
        error_email_message = ""
        error_email_status = ""

        # variables for storing post in database.
        django_do_bulk_create = True
        django_comment_create_list = []
        comment_create_count = -1
        django_current_create_count = -1
        
        # variables for exception handling.
        exception_type = ""
        exception_value = ""
        exception_traceback = ""
        
        # variables for summary information
        new_posts_processed = -1
        first_reddit_id_processed = ""
        start_dt = ""
        temp_string = ""
        summary_string = ""
        summary_email_subject = ""
        summary_email_message = ""

        # get reddiwrap instance
        reddiwrap = self.get_reddiwrap_instance()

        # initialize variables
        post_counter = 0
        comment_create_count = 0
        django_do_bulk_create = False
        django_bulk_create_list = []
        django_bulk_create_count = 0
        start_dt = datetime.datetime.now()
        
        # set bulk create flag - for now, always doing bulk create of comments
        #    unless update is true.
        #django_do_bulk_create =  self.do_bulk_create

        # updating existing?  If so, then can't do bulk create.
        do_update_existing = do_update_existing_IN
        if ( do_update_existing == True ):
        
            # we are updating existing.  No bulk create.
            django_do_bulk_create = False
        
        #-- END check to see if we update existing --#

        # check to see if we have a QuerySet
        if ( ( posts_qs_IN ) and ( posts_qs_IN != None ) ):
        
            # yes.  Use QuerySet passed in.
            posts_to_process_qs = posts_qs_IN
        
        else:
        
            # no - get all that are eligible to be processed.
            posts_to_process_qs = reddit_collect.models.Post.objects.filter( comment_collection_status != reddit_collect.models.Post.COMMENT_COLLECTION_STATUS_DONE )
        
        #-- END check to see if posts passed in --#
        
        # !TODO - big outer try/except.
        try:
        
            # loop over posts.
            post_counter = 0
            continue_collecting = True
            post_count = len( posts_to_process_qs )
            for current_post in posts_to_process_qs:
            
                # see if it is OK to continue.
    
                # call may_i_continue() if other than first post
                if ( post_counter > 0 ):
                
                    # not first post.  call may_i_continue()
                    continue_collecting = self.may_i_continue()
                
                #-- END check to see if first post --#
                
                # OK to continue?
                if continue_collecting == True:
                
                    # increment post counter
                    post_counter += 1
                    
                    print( "- " + str( post_counter ) + " of " + str( post_count ) + " - post " + str( current_post.id ) + " ( reddit ID: " + current_post.reddit_id + " ) by " + current_post.author_name + " - created on " + str( current_post.created_utc_dt ) )
    
                    # memory management.
                    gc.collect()
                    django.db.reset_queries()
        
                    # set request start time (OK to be a little inefficient)
                    self.start_request()
    
                    # populate a reddiwrap Post instance.
                    current_rw_post = current_post.create_reddiwrap_post()
                    
                    # use reddiwrap to load comments.
                    
                    # wrap in loop
                    comments_collected = False
                    connection_error_count = 0
                    while ( comments_collected == False ):
    
                        try:
                        
                            reddiwrap.fetch_comments( current_rw_post, 500 );
                            comments_collected = True
                        
                        except Exception as e:
                        
                            # set flag to False
                            comments_collected = False
                            
                            # increment error count.
                            connection_error_count += 1
    
                            # make exception message
                            exception_message = "In " + me + ": reddiwrap.fetch_comments() threw exception, fetching comments for post " + str( current_post.id ) + " ( reddit ID: " + current_post.reddit_id + " ); post " + str( post_counter ) + " of " + str( post_count )
    
                            # are we up to error limit yet?
                            if ( connection_error_count >= self.error_limit_count ):
    
                                # yes - send email about problems
                                error_email_subject = "Connection problem with comment collector."
                                exception_message = "Comment collector failed to connect " + str( self.error_limit_count ) + " times.  Details:\n" + exception_message
                                self.process_exception( e, exception_message, True, error_email_subject )
                                
                                # throw exception
                                raise( e )
                                
                            else:
                            
                                # haven't reached error limit yet. Process exception,
                                #    no email, pause 10 seconds, then try again.
                                self.process_exception( e, exception_message, False )
                                time.sleep( 10 )
                            
                            #-- END check to see if we've exceeded error limit. --#
                            
                        #-- END try/except around collecting comments from reddit. --#
                        
                    #-- END loop around collecting comments --#
                    
                    # bulk?
                    if ( django_do_bulk_create == True ):
                    
                        # process comment list in bulk (recursive)
                        django_bulk_create_list = self.process_comments_bulk( current_post, current_rw_post.comments )
                        
                        # do bulk_create()?
                        if ( ( django_bulk_create_list ) and ( len( django_bulk_create_list ) > 0 ) ):
                        
                            # try/except around saving.
                            try:
            
                                # yes.
                                reddit_collect.models.Comment.objects.bulk_create( django_bulk_create_list )
                                
                                # increment total count
                                django_bulk_create_count = len( django_bulk_create_list )
                                comment_create_count += django_bulk_create_count
    
                            except Exception as e:
                                
                                # error saving.  Probably encoding error.
            
                                # send email about problems
                                error_email_subject = "Problem bulk-saving comments."
                                exception_message = "In " + me + ": bulk_create() threw exception, processing comments for post " + str( current_post.id ) + " ( reddit ID: " + current_post.reddit_id + " ); count of comments being bulk created = " + str( django_bulk_create_count )
                                self.process_exception( e, exception_message, True, error_email_subject )
                                            
                                # throw exception?
                                raise( e )
                                    
                            #-- END try/except around saving. --#
    
                        #-- END check to see if anything to bulk create. --#
                        
                    else:
                    
                        # process comment list (recursive)
                        django_current_create_count = self.process_comments( post_IN = current_post, comment_list_IN = current_rw_post.comments, do_update_existing_IN = do_update_existing )
                    
                        # increment total count
                        comment_create_count += django_current_create_count
                        
                    #-- END check to see if bulk or not. --#
                    
                    # update the post to show that it has been comment-harvested.
                    if ( current_post.comment_collection_status == reddit_collect.models.Post.COMMENT_COLLECTION_STATUS_NEW ):
                    
                        # update status to "ongoing".
                        current_post.comment_collection_status = reddit_collect.models.Post.COMMENT_COLLECTION_STATUS_ONGOING
                        current_post.save()
                    
                    #-- END check to see if first-time updating comments. --#
    
                else:
                
                    # may_i_continue() returned False.  Once that happens once,
                    #    unlikely it will return True ever again.
                    print( "====> In " + me + ": may_i_continue() returned False.  This shouldn't be possible.  Falling out of loop." )
                    break                
                                
                #-- END check to see if we are OK to continue collecting. --#
            
            #-- END loop over posts. --#
            
        except Exception as e:
        
            # yes - send email about problems
            error_email_subject = "Unexpected problem with comment collector."
            exception_message = "Unexpected problem with comment collector.  Details:\n"
            self.process_exception( e, exception_message, True, error_email_subject )
            
            # throw exception?
            #raise( e )

        #-- END super try/except around entire loop.
        
        # output overall summary
        summary_string = ""

        temp_string = "==> Posts passed in: " + str( post_count )
        print( temp_string )
        summary_string += temp_string

        temp_string = "==> Posts processed: " + str( post_counter )        
        print( temp_string )
        summary_string += "\n" + temp_string

        temp_string = "==> Comments created: " + str( comment_create_count )
        print( temp_string )
        summary_string += "\n" + temp_string

        temp_string = "==> Collection started: " + str( start_dt )
        print( temp_string )
        summary_string += "\n" + temp_string

        end_dt = datetime.datetime.now()
        temp_string = "==> Collection ended: " + str( end_dt )
        print( temp_string )
        summary_string += "\n" + temp_string
        
        duration_td = end_dt - start_dt
        temp_string = "==> Duration: " + str( duration_td )
        print( temp_string )
        summary_string += "\n" + temp_string
        
        # email summary
        summary_email_subject = "Comment collection complete - " + str( datetime.datetime.now() )
        summary_email_message = "Comment collection summary:\n"
        summary_email_message += summary_string
        summary_email_status = self.email_send_status( summary_email_message, summary_email_subject )
        print( "==> Summary email status: " + summary_email_status )

        return status_OUT
    
    #-- END method collect_comments() --#


    def collect_posts( self, 
                       subreddit_IN = "all",
                       post_count_limit_IN = -1,
                       until_id_IN = "",
                       until_date_IN = None,
                       subreddit_in_list_IN = [],
                       after_id_IN = None,
                       before_id_IN = None,
                       do_update_existing_IN = False,
                       *args,
                       **kwargs ):
    
        '''
        This method collects posts from any subreddit you want, defaulting to the
           /r/all subreddit, which allows access to the entire history of reddit.
           Accepts parameters that let you collect from a given ID on (the 
           easiest way to collect starting at a certain date - find a post around
           the date you want, collect from that ID on), to a certain date, until
           you find a certain post ID, etc.
           
        Parameters:
        - subreddit_IN - defaults to "all". Subreddit you want to collect from.
        - post_count_limit_IN - number of posts we want to collect.
        - until_id_IN - value of ID we collect until we encounter in the stream (should include type - so begin with "t3_").
        - until_date_IN - datetime instance of UTC/GMT date and time we want to collect to (will stop collecting once a date after this is encountered).
        - subreddit_in_list_IN - list of subreddits to limit our collection to (each should begin with "t5_").  If you use this, in most cases, you should leave subreddit_IN = "all".
        - after_id_IN - ID you want to get posts after.  Must include type (start with "t3_").
        - before_id_IN - ID before which you want posts.  Must include type (start with "t3_").
        - do_update_existing_IN - Boolean, True if we want to update existing posts that are already in the database, false if not.  Defaults to False.
        
        Parameters to come (TK):
        - start_date_IN - datetime instance of date and time after which we want to collect (will ignore until a post is greater-than-or-equal to this date).  For now, to collect from a certain date, find a post around the date you want, collect from that ID on using the after_id_IN parameter.
           
        Postconditions: Stores each matching post to the database using django
           model classes.  Returns a status message.
        '''

        # return reference
        status_OUT = self.STATUS_SUCCESS
        
        # declare variables
        me = "collect_posts"
        reddiwrap = None
        post_count = -1
        api_url = ""
        post_list = None
        continue_collecting = True
        current_rw_post = None
        current_post_reddit_id = ""
        current_post_created = ""
        current_post_created_dt = None
        current_post_subreddit_id = ""
        do_update_existing = False

        # variables for storing post in database.
        django_do_bulk_create = True
        django_post_create_list = []
        django_bulk_create_count = -1
        django_current_create_count = -1
        django_post = None
        is_post_in_database = False
        
        # variables for exception handling.
        exception_type = ""
        exception_value = ""
        exception_traceback = ""
        
        # variables for summary information
        new_posts_processed = -1
        update_count = -1
        first_reddit_id_processed = ""
        start_dt = None
        temp_dt = None
        temp_string = ""
        summary_string = ""
        summary_email_subject = ""
        summary_email_message = ""

        # get reddiwrap instance
        reddiwrap = self.get_reddiwrap_instance()

        # initialize variables
        post_count = 0
        new_posts_processed = 0
        update_count = 0
        django_do_bulk_create = self.do_bulk_create
        django_bulk_create_count = 0
        start_dt = datetime.datetime.now()
        
        # updating existing?  If so, then can't do bulk create.
        do_update_existing = do_update_existing_IN
        if ( do_update_existing == True ):
        
            # we are updating existing.  No bulk create.
            django_do_bulk_create = False
        
        #-- END check to see if we update existing --#

        # create URL - first, add in reddit, limit.
        api_url = "/r/%s/new?limit=100" % subreddit_IN
        
        # add ability to add parameterized limit to URL?

        # after param?
        if ( ( after_id_IN ) and ( after_id_IN != None ) and ( after_id_IN != "" ) ):
        
            # yes.  Add it to the URL.
            api_url += "&after=" + after_id_IN
        
        #-- END check to see if after ID passed in. --#
        
        # before param?
        if ( ( before_id_IN ) and ( before_id_IN != None ) and ( before_id_IN != "" ) ):
        
            # yes.  Add it to the URL.
            api_url += "&before=" + before_id_IN
        
        #-- END check to see if after ID passed in. --#
        
        # !TODO - big outer try/except.
        try:

            # loop until flag is false
            while continue_collecting == True:
            
                print( "In " + me + ": top of loop - " + str( datetime.datetime.now() ) + " - latest post = " + current_post_reddit_id + " ( " + str( current_post_created_dt ) + " ), number " + str( post_count ) + "." )
    
                # memory management.
                gc.collect()
                django.db.reset_queries()
    
                # set request start time (OK to be a little inefficient)
                self.start_request()
                
                # bulk create?
                if ( django_do_bulk_create == True ):
                
                    # clear out the bulk create list.
                    django_post_create_list = []
                    
                #-- END check to see if doing bulk create. --#
    
                # get first set of results, or grab next set of results.
                if ( post_count == 0 ):
    
                    # get first set of results for /r/all
                    post_list = reddiwrap.get( api_url )
                    
                else:
                
                    # get next set of posts.
                    post_list = reddiwrap.get_next()
    
                #-- END check to see how we grab more posts. --#
                
                temp_dt = datetime.datetime.now()
                print( "In " + me + ": after retrieving stuff from reddit - " + str( temp_dt ) + "; elapsed: " + str( temp_dt - self.request_start_time ) + " - latest post = " + current_post_reddit_id + " ( " + str( current_post_created_dt ) + " ), number " + str( post_count ) + "." )
            
                #--------------------------------------------------------------------
                # loop over posts.
                #--------------------------------------------------------------------
    
                for current_rw_post in post_list:
    
                    # increment post counter.
                    post_count += 1
                
                    # get info. on current post.
                    current_post_reddit_id = current_rw_post.id
                    current_post_id_with_type = "t3_" + current_post_reddit_id
                    current_post_created = current_rw_post.created_utc
                    current_post_created_dt = datetime.datetime.fromtimestamp( int( current_post_created ) )
                    current_post_subreddit_id = current_rw_post.subreddit_id
                    current_post_subreddit_name = current_rw_post.subreddit
                    current_post_url = current_rw_post.url
                    
                    # initialize variables
                    is_post_in_database = False
                    
                    if ( self.debug_flag == True ):
        
                        print( "In " + me + ": reddit post " + current_post_id_with_type + " is post number " + str( post_count ) + ", subreddit = " + current_post_subreddit_name + ": URL = " + current_post_url )
                        
                    #-- END DEBUG --#
                    
                    # first post? (I know, couldn't think of a better way...)
                    if ( post_count == 1 ):
                    
                        # store the first ID.
                        first_reddit_id_processed = current_post_id_with_type
                        
                    #-- END check to see if post count = 1 --#
                    
                    #----------------------------------------------------------------
                    # conditions for stopping collection
                    #----------------------------------------------------------------
                    
                    # do we have a post count limit?
                    if ( ( post_count_limit_IN ) and ( post_count_limit_IN > 0 ) ):
                    
                        # yes - has post count exceded this count?
                        if ( post_count > post_count_limit_IN ):
                        
                            # it is.  stop.
                            continue_collecting = False
                            print( "In " + me + ": reddit post " + current_post_reddit_id + " is post number " + str( post_count ) + ", putting us over our limit of " + str( post_count_limit_IN ) + ".  Stopping collection." )
                            
                        #-- END check to see if current post puts us over our post limit. --#
                    
                    #-- END check for post count limit. --#
                    
                    # do we have an until ID?
                    if ( ( until_id_IN ) and ( until_id_IN != "" ) ):
                    
                        # is current ID the until ID?
                        if ( current_post_reddit_id == until_id_IN ):
                        
                            # it is.  stop.
                            continue_collecting = False
                            print( "In " + me + ": reddit post " + current_post_reddit_id + " is our until post ( " + until_id_IN + " ).  Stopping collection." )
                            
                        #-- END check to see if current post is post at which we are to stop. --#
                    
                    #-- END check for until ID. --#
                    
                    # do we have an until date?
                    if ( ( until_date_IN ) and ( until_date_IN != None ) ):
                    
                        #-- we have an until date...  is current date less than until date?
                        if ( current_post_created_dt < until_date_IN ):
                        
                            # it is.  stop.
                            continue_collecting = False
                            print( "In " + me + ": reddit post " + current_post_reddit_id + " has date " + str( current_post_created_dt ) + " that is past our until date.  Stopping collection." )
                        
                        #-- END check to see if post's date is past the cutoff. --#
                    
                    #-- END check to see if we have an until date --#
    
                    #----------------------------------------------------------------
                    # collection logic
                    #----------------------------------------------------------------
                    
                    # do we continue collecting?
                    if ( continue_collecting == True ):
    
                        # Only process if either there is no subreddit list, or the
                        #    subreddit is in the list.
                        if ( ( len( subreddit_in_list_IN ) <= 0 ) or ( current_post_subreddit_id in subreddit_in_list_IN ) ):
                        
                            # ==> post already in database?
                            try:
                        
                                # lookup post.
                                django_post = reddit_collect.models.Post.objects.get( reddit_id = current_post_reddit_id )
    
                                # post is in database
                                is_post_in_database = True
                                # print( "In " + me + ": reddit post " + current_post_reddit_id + " is already in database." )
                                
                            except:
                            
                                # Not found.  Create new instance, set flag.
                                django_post = reddit_collect.models.Post()
                                is_post_in_database = False
                            
                            #-- END - check for post in database --#
                            
                            # ==> Got existing?  (Could put this in except, still not
                            #    sure how I feel about using exceptions for program
                            #    flow)
                            # OLD - allowing for update now.
                            #if ( django_post == None ):
    
                            # ==> Do we process this post?  We do if:
                            # - post is not in database. - OR -
                            # - post is in database, but update flag is true.
                            if ( ( is_post_in_database == False ) or ( ( is_post_in_database == True ) and ( do_update_existing == True ) ) ):
                            
                                # Update appropriate counter
                                if ( is_post_in_database == True ):
    
                                    # in database - increment update count.
                                    update_count += 1
    
                                else:
                                
                                    # not in database.  Increment new post count.
                                    new_posts_processed += 1
                                
                                #-- END counter increment. --#
    
                                # set fields from reddiwrap post instance.
                                django_post.set_fields_from_reddiwrap( current_rw_post, self.convert_4_byte_unicode_to_entity )
                                
                                # sanity check - are django_do_bulk_create and
                                #    do_update_existing both true?
                                if ( ( django_do_bulk_create == True ) and ( do_update_existing == True ) ):
                                
                                    print( "==> In " + me + "(): ERROR - django_do_bulk_create and do_update_existing are both True.  Should never happen." )
                                
                                #-- END sanity check. --#
    
                                # bulk create?
                                # - Never bulk create if do_update_existing is True.
                                if ( ( django_do_bulk_create == True ) and ( do_update_existing == False ) ):
                
                                    # add post to bulk create list.
                                    django_post_create_list.append( django_post )
                    
                                else: #-- not bulk create --#
    
                                    # exception handling around save, to deal with encoding (!).
                                    try:
                                    
                                        # save to database.
                                        django_post.save()
                                        
                                    except Exception as e:
                                    
                                        # error saving.  Probably encoding error.
        
                                        # process exception.
                                        error_email_subject = "Problem saving post."
                                        exception_message = "In " + me + ": reddit post " + current_post_reddit_id + " threw exception on save()."
                                        self.process_exception( e, exception_message, True, error_email_subject )
                                                
                                        # throw exception?
                                        raise( e )
                                        
                                    #-- END try-except around save() --#
                                    
                                #-- END if...else check to see if doing bulk create. --#
                                    
                            #-- END check to see if already in database --#
                            
                        #-- END check to see if subreddit list indicates we should process this post. --#
                        
                    #-- END check to see if we continue collecting --#
                
                #-- END loop over current set of posts. --#
                
                #--------------------------------------------------------------------
                # bulk create?
                #--------------------------------------------------------------------
    
                if ( django_do_bulk_create == True ):
                
                    # yes, bulk create.  Anything in the create list?
                    django_current_create_count = len( django_post_create_list )
                    if ( django_current_create_count > 0 ):
                    
                        # yes.  Bulk create, then update count.
                        # exception handling around save, to deal with encoding (!).
                        try:
                        
                            # save to database using bulk_create().
                            reddit_collect.models.Post.objects.bulk_create( django_post_create_list )
                            
                        except Exception as e:
                        
                            # error saving.  Probably encoding error.
    
                            # process exception.
                            error_email_subject = "Problem bulk-saving posts."
                            exception_message = "In " + me + ": bulk_create() threw exception.  Last reddit post ID processed: " + current_post_reddit_id + "; count of posts being bulk created = " + str( django_current_create_count )
                            self.process_exception( e, exception_message, True, error_email_subject )
    
                            # throw exception?
                            raise( e )
                            
                        #-- END try-except around bulk_create() --#
                        
                        # increment the total posts created counter
                        django_bulk_create_count += django_current_create_count
                        
                        # could empty create list here, but doing it at top of loop,
                        #    so no need to do it twice.
                    
                    #-- END check to see if posts to create --#
                
                #-- END check to see if bulk create --#
    
                #--------------------------------------------------------------------
                # if we haven't already decided to stop, check if we can continue.
                #--------------------------------------------------------------------
    
                if ( continue_collecting == True ):
                
                    # no reason to stop yet...  Do we have more posts?                
                    if ( reddiwrap.has_next() == False ):
                
                        # no - do not continue.
                        continue_collecting = False
                    
                    else:
                
                        # see if we are allowed to continue.
                        continue_collecting = self.may_i_continue()
                        
                    #-- END checks to see if we continue collecting. --#
    
                #-- END check to see if we continue collecting. --#
                
            #-- END outer reddit collection loop --#
            
        except Exception as e:
        
            # yes - send email about problems
            error_email_subject = "Unexpected problem with post collector."
            exception_message = "Unexpected problem with post collector.  Details:\n"
            self.process_exception( e, exception_message, True, error_email_subject )
            
            # throw exception?
            #raise( e )

        #-- END super try/except around entire loop.
        
        # output overall summary
        summary_string = ""
        
        temp_string = "==> Posts processed: " + str( post_count )
        print( temp_string )
        summary_string += temp_string
        
        temp_string = "==> New posts: " + str( new_posts_processed )
        print( temp_string )
        summary_string += "\n" + temp_string

        if ( do_update_existing == True ):
        
            temp_string = "==> Updated posts: " + str( update_count )
            print( temp_string )
            summary_string += "\n" + temp_string
        
        #-- END check to see if we are updating. --#
        
        if ( django_do_bulk_create == True ):
        
            temp_string = "==> Posts bulk_create()'ed: " + str( django_bulk_create_count )
            print( temp_string )
            summary_string += "\n" + temp_string
        
        #-- END check to see if bulk create --#
        
        temp_string = "==> First reddit ID processed: " + first_reddit_id_processed
        print( temp_string )
        summary_string += "\n" + temp_string

        temp_string = "==> Last reddit ID processed: " + current_post_reddit_id
        print( temp_string )
        summary_string += "\n" + temp_string

        temp_string = "==> Collection started: " + str( start_dt )
        print( temp_string )
        summary_string += "\n" + temp_string

        end_dt = datetime.datetime.now()
        temp_string = "==> Collection ended: " + str( end_dt )
        print( temp_string )
        summary_string += "\n" + temp_string
        
        duration_td = end_dt - start_dt
        temp_string = "==> Duration: " + str( duration_td )
        print( temp_string )
        summary_string += "\n" + temp_string
        
        # email summary
        summary_email_subject = "Post collection complete - " + str( datetime.datetime.now() )
        summary_email_message = "Post collection summary:\n"
        summary_email_message += summary_string
        summary_email_status = self.email_send_status( summary_email_message, summary_email_subject )
        print( "==> Summary email status: " + summary_email_status )

        return status_OUT
    
    #-- END method collect_posts() --#


    def create_reddiwrap_instance( self, *args, **kwargs ):
    
        '''
        Creates and returns ReddiWrap instance for User Agent in this
           instance, and if there is both a username and a password, also logs it
           in using those credentials.  If error, returns None.
        ''' 
        
        # return reference
        instance_OUT = None
        
        # declare variables
        my_user_agent = ""
        my_cookie_file_path = ""
        my_username = ""
        my_password = ""
        do_login = False
        login_result = -1
        
        # create new instance.
        my_user_agent = self.user_agent
        instance_OUT = ReddiWrap( user_agent = my_user_agent )
        
        # do we have a cookie file path?  If so, try to load cookies.
        my_cookie_file_path = self.cookie_file_path
        if ( ( my_cookie_file_path ) and ( my_cookie_file_path != "" ) ):
        
            instance_OUT.load_cookies( my_cookie_file_path )
        
        #-- END check to see if cookie file path --#
        
        # got username and password?
        my_username = self.username
        my_password = self.password
        
        if ( ( ( my_username ) and ( my_username != "" ) ) and ( ( my_password ) and ( my_password != "" ) ) ):
        
            # from cookie file, is this user already authenticated?
            if ( instance_OUT.logged_in == False ):
            
                # log in.
                do_login = True
                
            # logged in - same username?  If not, log in again.
            elif ( reddit.user.lower() != my_username.lower() ):
            
                # log in.
                do_login = True
                
            else:
            
                # logged_in is True and it is the same user name.  No need to
                #    log in again.
                do_login = False
                
            #-- END check to see if we need to log in. --#
            
            # Do we need to log in?
            if ( do_login == True ):
            
                # yes, we need to login.  Try it.
                print('logging into %s' % my_username)
                login_result = instance_OUT.login( user = my_username, password = my_password )
                
                # success?
                if ( login_result != 0 ):
                
                    # fail.  Output message.
                    print( 'ERROR - unable to log in with username: %s; password: %s (error code %d where 1 = invalid password, 2 = over rate limit, -1 = unexpected error)' % ( my_username, my_password, login_result ) )
                    
                    # return None?
                    # instance_OUT = None
                
                else:
                
                    # success!  If cookie path, update cookies.
                    if ( ( my_cookie_file_path ) and ( my_cookie_file_path != "" ) ):
                    
                        # save cookies.
                        instance_OUT.save_cookies( my_cookie_file_path )
                    
                    #-- END check to see if we have a cookie file path. --#
                
                #-- END check to see if success --#
            
            #-- END check to see if we need to log in. --#
        
        #-- END check to see if we have a username and a password. --#
            
        return instance_OUT
    
    #-- END create_reddiwrap_instance() --#


    def email_initialize( self, smtp_host_IN = "localhost", smtp_port_IN = -1, smtp_use_ssl_IN = False, smtp_username_IN = "", smtp_password_IN = "", *args, **kwargs ):
    
        '''
        Accepts properties that can be used to initialize an email helper
           instance.  Initializes object, stores it in instance variable.
        '''
    
        # declare variables
        my_email_helper = None
        my_exception_helper = None
        
        # create email helper
        my_email_helper = EmailHelper()
        
        # set host.
        my_email_helper.set_smtp_server_host( smtp_host_IN )

        # set port?
        if ( ( smtp_port_IN ) and ( smtp_port_IN != None ) and ( smtp_port_IN > 0 ) ):
        
            my_email_helper.set_smtp_server_port( smtp_port_IN )
        
        #-- END check to see if port passed in. --#
        
        # use ssl?
        my_email_helper.set_smtp_server_use_SSL( smtp_use_ssl_IN )
        
        # set username?
        if ( ( smtp_username_IN ) and ( smtp_username_IN != None ) and ( smtp_username_IN != "" ) ):
        
            my_email_helper.set_smtp_server_username( smtp_username_IN )
        
        #-- END check to see if username passed in --#

        # set password?
        if ( ( smtp_password_IN ) and ( smtp_password_IN != None ) and ( smtp_password_IN != "" ) ):
        
            my_email_helper.set_smtp_server_password( smtp_password_IN )
        
        #-- END check to see if password passed in --#
        
        # store in instance variable.
        self.email_helper = my_email_helper
        
        # Do we have an Exception Helper?
        my_exception_helper = self.exception_helper
        if ( ( my_exception_helper ) and ( my_exception_helper ) ):
        
            # we do.  Add the email_helper to the exception helper, also.
            my_exception_helper.email_helper = my_email_helper
        
        #-- END check to see if exception helper --#
        
    #-- END method email_initialize() --#    
    
    
    def email_send( self, message_IN = None, subject_IN = None, from_address_IN = None, to_address_IN = None, *args, **kwargs ):

        '''
        Uses nested email_helper instance to send email.  Returns status message.
           If status returned is email_helper.STATUS_SUCCESS, then success, if
           anything else, it is an error message explaining why the email was not
           sent.
        '''
    
        # return reference
        status_OUT = ""
    
        # declare variables
        my_email_helper = None
        
        # get email helper
        my_email_helper = self.email_helper
        
        # got a helper?
        if ( ( my_email_helper ) and ( my_email_helper != None ) ):

            # yes - send email
            status_OUT = my_email_helper.send_email( message_IN, subject_IN, from_address_IN, to_address_IN )
            
        else:
        
            # no - error.
            status_OUT = "ERROR - no email helper present, so can't send email."
        
        #-- END check to see if we have an email helper. --#
        
        return status_OUT
    
    #-- END method email_send() --#
    
    
    def email_send_status( self, message_IN = None, subject_IN = None, *args, **kwargs ):

        '''
        If email helper and status email are set, uses nested email_helper
           instance to send email to status email.  Returns status message.
           If status returned is email_helper.STATUS_SUCCESS, then success, if
           anything else, it is an error message explaining why the email was not
           sent.
        '''
    
        # return reference
        status_OUT = ""
    
        # declare variables
        my_email_helper = None
        my_status_email = ""
        
        # get email helper and status address
        my_email_helper = self.email_helper
        my_status_email = self.email_status_address
        
        # got a helper?
        if ( ( my_email_helper ) and ( my_email_helper != None ) ):

            # yes.  Got a status email address?
            if ( ( my_status_email ) and ( my_status_email != None ) and ( my_status_email != "" ) ):

                # yes - send email
                status_OUT = my_email_helper.send_email( message_IN, subject_IN, my_status_email, my_status_email )
                
            else:
            
                # no status email address set.
                status_OUT = "ERROR - no email address set for sending status messages.  Can't send email status."
            
            #-- END check to see if status email present --#
            
        else:
        
            # no - error.
            status_OUT = "ERROR - no email helper present, so can't send email."
        
        #-- END check to see if we have a mail helper. --#
        
        return status_OUT
    
    #-- END method email_send_status() --#
    
    
    def get_reddiwrap_instance( self, *args, **kwargs ):
    
        '''
        If there is a reddiwrap instance already in this instance, returns it.
           If not, creates and returns ReddiWrap instance for User Agent in this
           instance, and if there is both a username and a password, also logs it
           in using those credentials.  Stores a newly created instance in this
           object, so it can be re-used.  If error, returns None.
        ''' 
        
        # return reference
        instance_OUT = None
        
        # declare variables
        
        instance_OUT = self.reddiwrap_instance
        
        if ( ( not instance_OUT ) or ( instance_OUT == None ) ):
            
            # create new instance.
            instance_OUT = self.create_reddiwrap_instance()
            
            # store it.
            self.reddiwrap_instance = instance_OUT
            
            # retrieve from that variable, just so we make sure it got stored.
            instance_OUT = self.reddiwrap_instance
            
        #-- END check to see if there is anything in m_e2user_node_type.
        
        return instance_OUT
    
    #-- END get_reddiwrap_instance() --#


    def process_comments( self,
                          post_IN = None,
                          comment_list_IN = [],
                          parent_comment_IN = None,
                          do_update_existing_IN = False,
                          *args,
                          **kwargs ):
        
        '''
        Accepts django reddit_collect.models.Post instance, list of reddiwrap
           comment instances.  Loops over all comments in the list, processing
           each, then checking for child comments.  If child(ren) found, calls
           this routine again, also passing parent comment, so they reference
           both root parent post and parent comment.  Returns count of comments
           created.  This method creates all django relations as well as storing
           IDs from reddit.  The process_comments_bulk() method stores reddit IDs
           so comment relations can be pieced together, but doesn't create django
           relations, as well.
                   
        Parameters:
        - post_IN - reddit_collect.models.Post instance, so we can relate comments to their post.
        - comment_list_IN - list of reddiwrap Comment instances we are to store in the database.
        - parent_comment_IN - reddit_collect.models.Comment instance of parent comment, so we can relate the child comment back to it.
        - do_update_existing_IN - Boolean, True if we want to update existing comments that are already in the database, false if not.  Defaults to False.
        '''
    
        # return reference
        comment_count_OUT = 0
        
        # declare variables
        me = "process_comments"
        do_update_existing = False
        comment_count = -1
        update_count = -1
        new_comment_count = -1
        current_rw_comment = None
        comment_reddit_full_id = ""
        django_comment = None
        is_comment_in_database = False
        django_do_bulk_create = False
        comment_children = None
        child_count = -1
        
        # initialize variables
        comment_count = 0
        
        # updating existing?
        do_update_existing = do_update_existing_IN
        
        # do we have a comment list
        if ( ( comment_list_IN ) and ( len( comment_list_IN ) > 0 ) ):
        
            # we have comments.  Loop over them.
            for current_rw_comment in comment_list_IN:
            
                # increment count
                comment_count += 1
                
                # get the full ID
                comment_reddit_full_id = current_rw_comment.name
            
                # ==> comment already in database?
                try:
            
                    # lookup comment.
                    django_comment = reddit_collect.models.Comment.objects.get( reddit_full_id = comment_reddit_full_id )
                    
                    # post is in database
                    is_comment_in_database = True

                    print( "In " + me + ": reddit comment " + comment_reddit_full_id + " is already in database - moving on." )
                
                except:
                
                    # Not found.   Create new instance, set flag.
                    django_comment = reddit_collect.models.Comment()
                    is_comment_in_database = False
                
                #-- END - check for comment in database --#
                
                # ==> Got existing?  (Could put this in except, still not
                #    sure how I feel about using exceptions for program
                #    flow)
                # OLD - allowing for update now.
                #if ( django_comment == None ):

                # ==> Do we process this comment?  We do if:
                # - comment is not in database. - OR -
                # - comment is in database, but update flag is true.
                if ( ( is_comment_in_database == False ) or ( ( is_comment_in_database == True ) and ( do_update_existing == True ) ) ):

                    # Update appropriate counter
                    if ( is_comment_in_database == True ):

                        # in database - increment update count.
                        update_count += 1

                    else:
                    
                        # not in database.  Increment new post count.
                        new_comment_count += 1
                    
                    #-- END counter increment. --#

                    # create model instance.
                    # OLD - already have instance now.
                    #django_comment = reddit_collect.models.Comment()
                    
                    # set fields from reddiwrap instance.
                    django_comment.set_fields_from_reddiwrap( current_rw_comment, self.convert_4_byte_unicode_to_entity )
                    
                    # if post, set post (better be a post).
                    if ( ( post_IN ) and ( post_IN != None ) ):

                        django_comment.post = post_IN
                        
                    #-- END check to see if related post passed in. --#
                    
                    # if parent comment, set it.
                    if ( ( parent_comment_IN ) and ( parent_comment_IN != None ) ):
                    
                        django_comment.parent = parent_comment_IN
                    
                    #-  END check to see if parent_comment_IN --#
                    
                    # exception handling around save, to deal with encoding (!).
                    try:
                    
                        # save to database.
                        django_comment.save()
                        
                    except Exception as e:
                    
                        # error saving.  Probably encoding error.

                        # process exception.
                        error_email_subject = "Problem saving comment."
                        exception_message = "In " + me + ": reddit comment " + comment_reddit_full_id + " threw exception on save()."
                        self.process_exception( e, exception_message, True, error_email_subject )

                        # throw exception?
                        raise( e )
                        
                    #-- END try-except around save() --#
                        
                #-- END check to see if already in database --#

                # does current comment have children?
                comment_children = current_rw_comment.children
                if ( ( comment_children ) and ( len( comment_children ) > 0 ) ):
                
                    # yes.  Recurse!
                    child_count = self.process_comments( post_IN, comment_children, django_comment, do_update_existing_IN )
                    
                    # add child count to comment_count
                    comment_count += child_count
                
                #-- END check to see if there are comments --#
            
            #-- END loop over comments. --#
        
        #-- END check to see if comments. --#
        
        # return comment_count
        comment_count_OUT = comment_count
        
        return comment_count_OUT
    
    #-- END method process_comments --#
    
    
    def process_comments_bulk( self, post_IN = None, comment_list_IN = [], *args, **kwargs ):
        
        '''
        Accepts django reddit_collect.models.Post instance, list of reddiwrap
           comment instances.  Loops over all comments in the list, processing
           each, then checking for child comments.  If child(ren) found, calls
           this routine again, passing post and list of children, so they
           reference root parent post.  Returns list of comments
           that need to be bulk saved.  This method stores reddit IDs so comment
           relations can be pieced together, but doesn't create django relations,
           as well.  The process_comments_bulk() method creates all django
           relations as well as storing IDs from reddit.  Lots more queries,
           though.
                   
        Parameters:
        - post_IN - reddit_collect.models.Post instance, so we can relate comments to their post.
        - comment_list_IN - list of reddiwrap Comment instances we are to store in the database.
        '''
    
        # return reference
        comment_list_OUT = []
        
        # declare variables
        me = "process_comments"
        comment_count = -1
        new_comment_count = -1
        current_rw_comment = None
        comment_reddit_full_id = ""
        django_comment = None
        django_do_bulk_create = False
        comment_children = None
        child_comment_list = []
        
        # initialize variables
        comment_count = 0
        
        # do we have a comment list
        if ( ( comment_list_IN ) and ( len( comment_list_IN ) > 0 ) ):
        
            # we have comments.  Loop over them.
            for current_rw_comment in comment_list_IN:
            
                # increment count
                comment_count += 1
                
                # get the full ID
                comment_reddit_full_id = current_rw_comment.name
            
                # ==> comment already in database?
                try:
            
                    # lookup comment.
                    django_comment = reddit_collect.models.Comment.objects.get( reddit_full_id = comment_reddit_full_id )

                    print( "In " + me + ": reddit comment " + comment_reddit_full_id + " is already in database - moving on." )
                
                except:
                
                    # Not found.  Set to None.
                    django_comment = None
                
                #-- END - check for comment in database --#
                
                # !TODO - update as well as create?
                
                # ==> Got existing?  (Could put this in except, still not
                #    sure how I feel about using exceptions for program
                #    flow)
                if ( django_comment == None ):

                    # not in database.  Add it.
                    new_comment_count += 1
                    
                    # create model instance.
                    django_comment = reddit_collect.models.Comment()
                    
                    # set fields from reddiwrap instance.
                    django_comment.set_fields_from_reddiwrap( current_rw_comment, self.convert_4_byte_unicode_to_entity )
                    
                    # if post, set post (better be a post).
                    if ( ( post_IN ) and ( post_IN != None ) ):

                        django_comment.post = post_IN
                        
                    #-- END check to see if related post passed in. --#
                    
                    # append instance to list
                    comment_list_OUT.append( django_comment )
                    
                #-- END check to see if already in database --#

                # does current comment have children?
                comment_children = current_rw_comment.children
                if ( ( comment_children ) and ( len( comment_children ) > 0 ) ):
                
                    # yes.  Recurse!
                    child_comment_list = self.process_comments_bulk( post_IN, comment_children )
                    
                    # add instances in child list to the return list.
                    comment_list_OUT.extend( child_comment_list )
                
                #-- END check to see if there are child comments --#
            
            #-- END loop over comments. --#
        
        #-- END check to see if comments. --#
        
        return comment_list_OUT
    
    #-- END method process_comments_bulk --#
    
    
    def process_exception( self, exception_IN = None, message_IN = "", send_email_IN = False, email_subject_IN = "", *args, **kwargs ):
    
        # return reference
        status_OUT = self.STATUS_SUCCESS
        
        # declare variables
        my_exception_helper = ""
        
        # get exception helper
        my_exception_helper = self.exception_helper
        if ( ( my_exception_helper ) and ( my_exception_helper != None ) ):

            # process using exception_helper.
            status_OUT = my_exception_helper.process_exception( exception_IN, message_IN, send_email_IN, email_subject_IN )
            
        #-- END check to see if we have a helper --#
        
        return status_OUT
    
    #-- END method process_exception() --#
    
    
    def set_email_status_address( self, value_IN, *args, **kwargs ):
    
        '''
        Accepts an email address, stores it internally, and in the nested
           exception helper, so it can be used to email exception messages.
        '''
        
        # declare variables
        my_exception_helper = None
        
        # store the value
        self.email_status_address = value_IN
        
        # see if we have an exception helper.
        my_exception_helper = self.exception_helper
        if ( ( my_exception_helper ) and ( my_exception_helper != None ) ):
        
            # we do.  Set it there, too.
            my_exception_helper.email_status_address = value_IN
        
        #-- END check to see if we have an exception helper --#
        
    #-- END method set_email_status_address() --#


#-- END class RedditCollector. --#

'''
#================================================================================
# Original Code
#================================================================================

reddit = ReddiWrap(user_agent='ReddiWrap')

USERNAME = 'Mr_Boy'
PASSWORD = 'Iman1234'
SUBREDDIT_NAMES = ['POLITICS', 'FUNNY', 'PICS' , 'todayilearned'];

while True:
	for MOD_SUB in SUBREDDIT_NAMES:
		print "#########  " + MOD_SUB + "  ###########";
		# Load cookies from local file and verify cookies are valid
		reddit.load_cookies('cookies.txt')

		# If we had no cookies, or cookies were invalid, 
		# or the user we are logging into wasn't in the cookie file:
		if not reddit.logged_in or reddit.user.lower() != USERNAME.lower():
			print('logging into %s' % USERNAME)
			login = reddit.login(user=USERNAME, password=PASSWORD)
			if login != 0:
				# 1 means invalid password, 2 means rate limited, -1 means unexpected error
				print('unable to log in: %d' % login)
				print('remember to change USERNAME and PASSWORD')
				exit(1)
			# Save cookies so we won't have to log in again later
			reddit.save_cookies('cookies.txt')

		print('logged in as %s' % reddit.user)

		# uinfo = reddit.user_info()
		# print('\nlink karma:    %d' % uinfo.link_karma)
		# print('comment karma: %d' % uinfo.comment_karma)
		# created = int(uinfo.created)
		# print('account created on:  %s' % reddit.time_to_date(created))
		# print('time since creation: %s\n' % reddit.time_since(created))


		# # # # # # # # Finding Subreddit
		print "Finding Subreddit ..."
		subreddit = "";
		flag = False; # if we find the subreddit, this flag is going to be Ture
		while True:
			subreddits = reddit.get('/reddits');
			for subred in subreddits:
				if subred.display_name == MOD_SUB.lower():
					subreddit = subred;
					flag = True;
					break
			if (not reddit.has_next()) or flag:
				break;
			time.sleep(2);
			subreddits = reddit.get_next()
			


		# # # # # # # # saving subreddit in subreddit table
		print "Saving Subreddit ... ";
		over18 = 0;
		if subreddit.over18 :
			over18 = 1;
		if not myLib.exsits_row(subreddit.id, "Subreddit"):
			myLib.insert_row([subreddit.id, subreddit.name, subreddit.display_name, subreddit.title, subreddit.url, subreddit.description,
		 subreddit.created, over18, int(subreddit.subscribers), subreddit.header_title] , "Subreddit");

		
		# # # # # # # # Saving Posts
		print "saving Posts ... "
		posts = reddit.get('/r/%s' % MOD_SUB)
		while True:
			for post in posts:
				if not myLib.exsits_row(post.id, "Post"):
					# add the post to the Post table
					myLib.insert_row(myLib.retrieve_post_traits(post), 'Post');
			if not reddit.has_next():
				break
			time.sleep(2);
			posts = reddit.get_next()

		 
		# subreddit = myLib.retreive_subreddit(MOD_SUB.lower());
		posts =  myLib.posts_of_reddit(subreddit.name); # corrent

		print "saving Comments ... ";
		i = 0;
		for post in posts:
			pst = myLib.make_post_obj(post);
			reddit.fetch_comments(pst);
			myLib.iterate_comments(pst.comments); # iterates and save comments
			time.sleep(1);
			i = i + 1;
			print i;

'''