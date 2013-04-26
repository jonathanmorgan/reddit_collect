#!/usr/bin/python

#================================================================================
# imports
#================================================================================

# base python libraries
import time
import sys
import datetime

# site-specific imports.
site_path = '/home/socs/socs_reddit/'
if site_path not in sys.path:
    sys.path.append( site_path )

import myLib
from reddiwrap.ReddiWrap import ReddiWrap


class RedditCollector( object ):


    #============================================================================
    # instance variables
    #============================================================================


    reddiwrap_instance = None
    user_agent = ""
    username = ""
    password = ""
    cookie_file_path = ""
    do_manage_time = True
    
    
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
        do_manage_time = True

    #-- END constructor --#


    #============================================================================
    # instance methods
    #============================================================================
    

    def collect_from_all_subreddit(  self, *args, **kwargs ):
    
        '''
        This method collects posts from the /r/all subreddit, which allows access
           to the entire history of reddit.  Eventually, we will add parameters
           to let you collect from or to a certain date, collect until you find a
           certain post ID, etc.  For now, iteratively building up to that so we
           can get our data.
           
        Postconditions: Stores each matching post to the database using django
           model classes.  Returns a status message.
        '''

        # return reference
        status_OUT = self.STATUS_SUCCESS
        
        # declare variables
        me = "collect_from_all_subreddit"
        reddiwrap = None
        post_list = None
        continue_collecting = True

        # first, get reddiwrap instance
        reddiwrap = self.get_reddiwrap_instance()
        
        # get first set of results for /r/all
        post_list = reddiwrap.get( "/r/all/new?limit=100" )

        # loop until flag is false
        while continue_collecting == True:
        
            # for now, just fall out of loop.
            continue_collecting = False
            
        #-- END loop --#
        
        return status_OUT
    
    #-- END method collect_from_all_subreddit() --#


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
    
    
    def may_i_continue( self, last_transaction_dt_IN = None, *args, **kwargs ):
    
        '''
        Accepts the last datetime.datetime of a transaction to reddit.  Compares
           that to datetime.datetime.now().  If the difference is greater than
           2 seconds, then returns True.  If not, waits the time between the
           difference and 2 seconds and returns True.  Can't think of a reason to
           return False at the moment, but perhaps, in the future, this could be
           a semaphore, and so processes could loop waiting for True.
           
        Eventually, will change processing based on the value in do_manage_time -
           if True, assume we are the only process.  If False, check a separate
           ok_to_proceed flag, set by external manager, and only return True when
           that flag has been set on this instance.
           
        Note: this will fail if interval between request and now() is exactly 24
           hours (not checking day at the moment, just seconds and microseconds).
        ''' 
        
        # return reference
        value_OUT = False
        
        # declare variables
        me = "may_i_continue"
        last_request_dt = None
        current_dt = None
        difference_td = None
        difference_seconds = -1
        difference_microseconds = -1
        sleep_seconds = -1.0
        
        # do we have a datetime passed in.
        if ( ( last_transaction_dt_IN ) and ( last_transaction_dt_IN != None ) ):
        
            # yes.  Use it.
            last_request_dt = last_transaction_dt_IN
            
        else:
        
            # no - just grab now().
            last_request_dt = datetime.datetime.now()
            
        #-- END check to see if we have a datetime passed in. --#
            
        # get current date time.
        current_dt = datetime.datetime.now()
        
        # date math - substract current from last_request.
        difference_td = current_dt - last_request_dt
        
        # get difference in seconds
        difference_seconds = difference_td.seconds
        difference_microseconds = difference_td.microseconds
        
        # convert microseconds to seconds (divide by 1,000,000), add to
        #    difference_seconds.
        difference_seconds = difference_seconds + ( difference_microseconds / 1000000.0 )
        
        print( "In " + me + ": difference = " + str( difference_seconds ) )

        # is difference greater than or equal to 2 seconds?
        if ( difference_seconds >= 2 ):
        
            # yes - return True.
            value_OUT = True
            print( "In " + me + ": greater than 2 seconds - OK to continue." )
            
        else:
            
            # no - subtract difference from 2.
            sleep_seconds = 2 - difference_seconds
            
            print( "In " + me + ": less than 2 seconds - sleep for " + str( sleep_seconds ) + " seconds." )

            # sleep.
            time.sleep( sleep_seconds )
            
            # set value_OUT
            value_OUT = True
            
        #-- END check to see if we need to sleep. --#
        
        return value_OUT
    
    #-- END may_i_continue() --#
    
    
#-- END class RedditCollector. --#

'''

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