# This is based on an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

# reddiwrap reddit API library
# import reddiwrap.ReddiWrap

# python_utilities
from python_utilities.booleans.boolean_helper import BooleanHelper

# python libraries
import datetime

class Subreddit(models.Model):

    #============================================================================
    # Django model fields.
    #============================================================================

    reddit_id = models.CharField( max_length = 255)
    name = models.TextField( null = True, blank = True )
    display_name = models.TextField( null = True, blank = True )
    title = models.TextField( null = True, blank = True )
    url = models.TextField( null = True, blank = True )
    description = models.TextField( null = True, blank = True )
    created = models.IntegerField( blank=True)
    created_dt = models.DateTimeField( null = True, blank = True )
    created_utc = models.TextField( null = True, blank = True )
    created_utc_dt = models.DateTimeField( null = True, blank = True )
    over_18 = models.BooleanField( blank = True, default = False )
    subscribers = models.IntegerField( null = True, blank = True )
    public_desc = models.TextField( null = True, blank = True )
    header_title = models.TextField( null = True, blank = True )
    create_date = models.DateTimeField( auto_now_add = True )
    last_update = models.DateTimeField( auto_now = True )

    #============================================================================
    # meta class
    #============================================================================

    # class Meta:

    #    db_table = 'Subreddit'

    #-- END Meta class --#
    

    #============================================================================
    # instance methods
    #============================================================================


    def set_fields_from_reddiwrap( self, instance_IN, *args, **kwargs ):
    
        '''
        Accepts a reddiwrap Comment instance.  Uses it to populate this instance.
        '''
    
        # declare variables
        
        # got an instance passed in?
        if ( ( instance_IN ) and ( instance_IN != None ) ):
    
            self.reddit_id = instance_IN.id              # 2qh0u
            self.name = instance_IN.name                 # t5_2qh0u
            self.display_name = instance_IN.display_name # pics
            self.title = instance_IN.title               # /r/Pics
            self.url = instance_IN.url                   # /r/pics/
            self.description = instance_IN.description   # <text description>
            self.created = instance_IN.created           # time since 1/1/1970, local
            self.created_utc = instance_IN.created_utc   # time since 1/1/1970, UTC
            self.over_18 = instance_IN.over18            # false
            self.subscribers = instance_IN.subscribers   # 1979507
            self.public_desc = instance_IN.public_desc   # <brief summary>
            self.header_title = instance_IN.header_title # "Pictures and Images"

            # what to do about these?
            '''
            self.header_img   = json_data['header_img']   # .png
            '''

        #-- END check to make sure instance passed in. --#
    
    #-- END method import_from_reddiwrap --#


#-- END Subreddit model --#


class User(models.Model):

    #============================================================================
    # Django model fields.
    #============================================================================

    reddit_id = models.CharField( max_length = 255)
    created = models.TextField( null = True, blank = True )
    created_dt = models.DateTimeField( null = True, blank = True )
    created_utc = models.TextField( null = True, blank = True )
    created_utc_dt = models.DateTimeField( null = True, blank = True )
    link_karma = models.IntegerField( null = True, blank = True )
    comment_karma = models.IntegerField( null = True, blank = True )
    create_date = models.DateTimeField( auto_now_add = True )
    last_update = models.DateTimeField( auto_now = True )

    #============================================================================
    # meta class
    #============================================================================

    # class Meta:

    #    db_table = 'User'

    #-- END Meta class --#
    

    #============================================================================
    # instance methods
    #============================================================================


    def set_fields_from_reddiwrap( self, instance_IN, *args, **kwargs ):
    
        '''
        Accepts a reddiwrap UserInfo instance.  Uses it to populate this instance.
        '''
    
        # declare variables
        
        # got an instance passed in?
        if ( ( instance_IN ) and ( instance_IN != None ) ):
    
            self.reddit_id = instance_IN.id
            self.created = instance_IN.created             # Time since 1/1/1970 when acct was created
            self.created_utc = instance_IN.created_utc     # Same as 'created', but in UTC
            self.link_karma = instance_IN.link_karma       # Integer, total score of submissions
            self.comment_karma = instance_IN.comment_karma # Integer, total score of comments

            # what to do about these?
            '''
            self.has_mail      = json_data['has_mail']      # Boolean, True if user has unread mail.
            self.name          = json_data['name']          # String, username
            if json_data.get('modhash') != None:
                self.modhash       = json_data['modhash']     # Unique hash for interacting with account
            self.is_gold       = json_data['is_gold']      # Boolean
            self.has_mod_mail  = json_data['has_mod_mail']  # Boolean
            self.is_mod        = json_data['is_mod']        # Boolean
            '''			

        #-- END check to make sure instance passed in. --#
    
    #-- END method import_from_reddiwrap --#


#-- END User model --#


class Post(models.Model):

    #============================================================================
    # Django model fields.
    #============================================================================

    reddit_id = models.CharField( max_length = 255)
    name = models.TextField( null = True, blank = True )
    title = models.TextField( null = True, blank = True )
    url = models.TextField( null = True, blank = True )
    author = models.ForeignKey( User, null = True, blank = True )
    author_name = models.TextField( null = True, blank = True )
    author_reddit_id = models.CharField( max_length = 255, null = True, blank = True )
    domain = models.TextField( null = True, blank = True )
    subreddit = models.ForeignKey( Subreddit, null = True, blank = True )
    subreddit_name = models.TextField( null = True, blank = True )
    subreddit_reddit_id = models.CharField( max_length = 255, null = True, blank = True )
    permalink = models.TextField( null = True, blank = True )
    is_self = models.BooleanField( blank = True, default = False )
    clicked = models.BooleanField( blank = True, default = False )
    hidden = models.BooleanField( blank = True, default = False )
    edited = models.BooleanField( blank = True, default = False )
    saved = models.BooleanField( blank = True, default = False )
    selftext = models.TextField( null = True, blank = True )
    selftext_html = models.TextField( null = True, blank = True )
    num_comments = models.IntegerField( null = True, blank = True )
    score = models.IntegerField( null = True, blank = True )
    upvotes = models.IntegerField( null = True, blank = True )
    downvotes = models.IntegerField( null = True, blank = True )
    over_18 = models.BooleanField( blank = True, default = False )
    created = models.TextField( null = True, blank = True )
    created_dt = models.DateTimeField( null = True, blank = True )
    created_utc = models.TextField( null = True, blank = True )
    created_utc_dt = models.DateTimeField( null = True, blank = True )
    num_reports = models.IntegerField( null = True, blank = True )
    modhash = models.TextField( null = True, blank = True )
    banned_by = models.TextField( null = True, blank = True )
    approved_by = models.TextField( null = True, blank = True )
    link_flair_class = models.TextField( null = True, blank = True )
    link_flair_text = models.TextField( null = True, blank = True )
    author_flair_class = models.TextField( null = True, blank = True )
    author_flair_text = models.TextField( null = True, blank = True )
    create_date = models.DateTimeField( auto_now_add = True )
    last_update = models.DateTimeField( auto_now = True )

    #============================================================================
    # meta class
    #============================================================================

    #class Meta:
    
    #    db_table = 'Post'

    #-- END Meta class --#


    #============================================================================
    # instance methods
    #============================================================================


    def set_fields_from_reddiwrap( self, instance_IN, *args, **kwargs ):
    
        '''
        Accepts a reddiwrap Comment instance.  Uses it to populate this instance.
        '''
    
        # declare variables
        test = False
        
        # got an instance passed in?
        if ( ( instance_IN ) and ( instance_IN != None ) ):
    
            self.modhash = instance_IN.modhash             # base36 string for communicating with account
            self.reddit_id = instance_IN.id                # base36 id for a post (usually 5 characters)
            self.name = instance_IN.name                   # example: t1_czwe3. t# is content type, the rest is the ID
            self.title = instance_IN.title                 # Title of post
            self.url = instance_IN.url                     # URL to post
            self.author_name = instance_IN.author          # Username of author
            self.domain = instance_IN.domain               # Domain posted ot
            self.subreddit = instance_IN.subreddit         # Subreddit posted to
            self.subreddit_reddit_id = instance_IN.subreddit_id
            self.permalink = instance_IN.permalink         # Link to the post (including comments)
            self.is_self = BooleanHelper.convert_value_to_boolean( instance_IN.is_self ) # Self-post?
            self.selftext = instance_IN.selftext           # Self-post text
            self.selftext_html = instance_IN.selftext_html # HTML for self-post text
            self.num_comments = instance_IN.num_comments   # Number of comments
            self.score = instance_IN.score                 # upvotes - downvotes * crazy reddit vote fuzzing constant
            self.upvotes = instance_IN.upvotes
            self.downvotes = instance_IN.downvotes
            self.over_18 = BooleanHelper.convert_value_to_boolean( instance_IN.over_18 ) # NSFW post
            self.created = instance_IN.created
            self.created_dt = datetime.datetime.fromtimestamp( int( self.created ) )
            self.created_utc = instance_IN.created_utc
            self.created_utc_dt = datetime.datetime.fromtimestamp( int( self.created_utc ) )
            self.num_reports = instance_IN.num_reports
            self.banned_by = instance_IN.banned_by
            self.approved_by = instance_IN.approved_by
            self.link_flair_text = instance_IN.link_flair_text
            self.link_flair_class = instance_IN.link_flair_class # link_flair_css_class": null,
            self.author_flair_text = instance_IN.author_flair_text # "author_flair_css_class": null,
            self.author_flair_class = instance_IN.author_flair_class
            self.clicked = BooleanHelper.convert_value_to_boolean( instance_IN.clicked ) # If logged-in user has clicked link yet
            self.hidden = BooleanHelper.convert_value_to_boolean( instance_IN.hidden )
            self.saved = BooleanHelper.convert_value_to_boolean( instance_IN.saved )
            self.edited = BooleanHelper.convert_value_to_boolean( instance_IN.edited )

            # what to do with these?
            '''
            self.comments      = [] # List of Comment objects that are replies to the Post
            self.has_more_comments = False # Contains comments that have not been loaded
            self.more_comments     = ''    # JSON data containing information about comments to load
            self.media_embed   = {}
            self.media         = None
            self.thumbnail     = ''
            '''

        #-- END check to make sure instance passed in. --#
    
    #-- END method import_from_reddiwrap --#

    
#-- END Post model --#


class Comment( models.Model ):

    #============================================================================
    # Django model fields.
    #============================================================================

    reddit_id = models.TextField()
    name = models.TextField( null = True, blank = True )
    link_id = models.TextField( null = True, blank = True )
    parent = models.ForeignKey( 'self', null = True, blank = True )
    parent_reddit_id = models.CharField( max_length = 255, null = True, blank = True )
    author = models.ForeignKey( User, null = True, blank = True )
    author_name = models.TextField( null = True, blank = True )
    author_reddit_id = models.CharField( max_length = 255, null = True, blank = True )
    post = models.ForeignKey( Post, null = True, blank = True )
    post_reddit_id = models.CharField( max_length = 255, null = True, blank = True )
    body = models.TextField( null = True, blank = True )
    body_html = models.TextField( null = True, blank = True )
    subreddit = models.TextField( null = True, blank = True )
    upvotes = models.IntegerField( null = True, blank = True )
    downvotes = models.IntegerField( null = True, blank = True )
    score = models.IntegerField( null = True, blank = True )
    created = models.TextField( null = True, blank = True )
    created_dt = models.DateTimeField( null = True, blank = True )
    created_utc = models.TextField( null = True, blank = True )
    created_utc_dt = models.DateTimeField( null = True, blank = True )
    edited = models.BooleanField( blank = True, default = False )
    edited_dt = models.DateTimeField( null = True, blank = True )
    num_reports = models.IntegerField( null = True, blank = True )
    modhash = models.TextField( null = True, blank = True )
    banned_by = models.TextField( null = True, blank = True )
    approved_by = models.TextField( null = True, blank = True )
    flair_class = models.TextField( null = True, blank = True )
    flair_text = models.TextField( null = True, blank = True )
    create_date = models.DateTimeField( auto_now_add = True )
    last_update = models.DateTimeField( auto_now = True )

    #============================================================================
    # meta class
    #============================================================================

    # class Meta:

    #    db_table = 'Comment'

    #-- END Meta class --#
    

    #============================================================================
    # instance methods
    #============================================================================


    def set_fields_from_reddiwrap( self, instance_IN, *args, **kwargs ):
    
        '''
        Accepts a reddiwrap Comment instance.  Uses it to populate this instance.
        '''
    
        # declare variables
        
        # got an instance passed in?
        if ( ( instance_IN ) and ( instance_IN != None ) ):
    
            self.modhash = instance_IN.modhash
            self.reddit_id = instance_IN.id
            self.name = instance_IN.name
            self.link_id = instance_IN.link_id
            self.parent_id = instance_IN.parent_id
            self.author_name = instance_IN.author
            self.body = instance_IN.body
            self.body_html = instance_IN.body_html
            self.subreddit = instance_IN.subreddit
            self.upvotes = instance_IN.upvotes
            self.downvotes = instance_IN.downvotes
            self.score = instance_IN.score
            self.created = instance_IN.created
            self.created_dt = datetime.datetime.fromtimestamp( int( self.created ) )
            self.created_utc = instance_IN.created_utc
            self.created_utc_dt = datetime.datetime.fromtimestamp( int( self.created_utc ) )
            self.edited = instance_IN.edited
            self.num_reports = instance_IN.num_reports
            self.banned_by = instance_IN.banned_by
            self.approved_by = instance_IN.approved_by
            self.flair_class = instance_IN.flair_class
            self.flair_text = instance_IN.flair_text
            
            # what to do about these?
            # self.children    = []
            # self.has_more_comments = False
            # self.more_comments = ''

        #-- END check to make sure instance passed in. --#
    
    #-- END method import_from_reddiwrap --#


#-- END Comment model --#