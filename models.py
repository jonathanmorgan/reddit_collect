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
import django.utils.encoding
from django.utils.encoding import python_2_unicode_compatible

# reddiwrap reddit API library
import reddiwrap.ReddiWrap

# python_utilities
from python_utilities.booleans.boolean_helper import BooleanHelper
from python_utilities.strings.string_helper import StringHelper

# python libraries
import datetime


#================================================================================
# functions
#================================================================================


def safe_string( string_IN = None ):

    # return reference
    string_OUT = None

    # store what was passed in in output reference.
    string_OUT = string_IN

    # make sure it is not None or empty string    
    if ( ( string_OUT ) and ( string_OUT != None ) and ( string_OUT != "" ) ):

        string_OUT = django.utils.encoding.smart_text( string_OUT ).encode( 'ascii', 'xmlcharrefreplace' )
        
    #-- END check to see if any flair text - don't want "None". --#

    return string_OUT

#-- END function clean_string() --#


#================================================================================
# django models
#================================================================================


@python_2_unicode_compatible
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
        Accepts a reddiwrap Subreddit instance.  Uses it to populate this instance.
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
    
    #-- END method set_fields_from_reddiwrap --#


    def __str__(self):
        
        # return reference
        string_OUT = ""
        
        # id?
        if ( ( self.id ) and ( self.id != None ) and ( self.id > 0 ) ):
        
            string_OUT += "Subreddit " + str( self.id ) + " - "
        
        #-- END check to see if id --#
        
        # name = type + reddit ID (t5_2qh0u)
        if( self.name ):
        
            string_OUT += self.name + " - "
        
        #-- END check to see if reddit_id --#
        
        # URL - includes the subreddit name.
        if ( self.url ):
        
            string_OUT += self.url
        
        #-- END check to see if URL --#

        return string_OUT

    #-- END __str__() method --#


#-- END Subreddit model --#


@python_2_unicode_compatible
class User(models.Model):

    #============================================================================
    # Django model fields.
    #============================================================================

    reddit_id = models.CharField( max_length = 255)
    name = models.TextField( null = True, blank = True )
    is_gold = models.BooleanField( blank = True, default = False )
    is_mod = models.BooleanField( blank = True, default = False )
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
            self.name = instance_IN.name                   # String, username
            self.is_gold = BooleanHelper.convert_value_to_boolean( instance_IN.is_gold ) # Boolean
            self.is_mod = BooleanHelper.convert_value_to_boolean( instance_IN.is_mod ) # Boolean
            self.created = instance_IN.created             # Time since 1/1/1970 when acct was created
            self.created_utc = instance_IN.created_utc     # Same as 'created', but in UTC
            self.link_karma = instance_IN.link_karma       # Integer, total score of submissions
            self.comment_karma = instance_IN.comment_karma # Integer, total score of comments

            # what to do about these?
            '''
            self.has_mail      = json_data['has_mail']      # Boolean, True if user has unread mail.
            if json_data.get('modhash') != None:
                self.modhash       = json_data['modhash']       # Unique hash for interacting with account
            self.has_mod_mail  = json_data['has_mod_mail']  # Boolean
            '''			

        #-- END check to make sure instance passed in. --#
    
    #-- END method set_fields_from_reddiwrap --#


    def __str__(self):
        
        # return reference
        string_OUT = ""
        
        # id?
        if ( ( self.id ) and ( self.id != None ) and ( self.id > 0 ) ):
        
            string_OUT += "User " + str( self.id )
        
        #-- END check to see if id --#
        
        # reddit ID
        if( self.reddit_id ):
        
            string_OUT += " - " + self.reddit_id
        
        #-- END check to see if reddit_id --#
        
        # name
        if( self.name ):
        
            string_OUT += " - " + self.name
        
        #-- END check to see if name --#
        
        return string_OUT

    #-- END __str__() method --#


#-- END User model --#


@python_2_unicode_compatible
class Post(models.Model):


    #----------------------------------------------------------------------
    # constants-ish
    #----------------------------------------------------------------------


    # comment collection statuses, for ongoing comment collection.
    COMMENT_COLLECTION_STATUS_NEW = "new"
    COMMENT_COLLECTION_STATUS_ONGOING = "ongoing"
    COMMENT_COLLECTION_STATUS_DONE = "done"

    COMMENT_COLLECTION_STATUS_CHOICES = (
        ( COMMENT_COLLECTION_STATUS_NEW, 'New' ),
        ( COMMENT_COLLECTION_STATUS_ONGOING, 'Ongoing' ),
        ( COMMENT_COLLECTION_STATUS_DONE, 'Done' ),
    )
    

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
    
    # comment collection
    comment_collection_status = models.CharField( max_length = 255, choices = COMMENT_COLLECTION_STATUS_CHOICES, default = COMMENT_COLLECTION_STATUS_NEW )
    comments_last_collected = models.DateTimeField( null = True, blank = True )
    
    # timestamps
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
        Accepts a reddiwrap Post instance.  Uses it to populate this instance.
        '''
    
        # declare variables
        text_value = ""
        
        # got an instance passed in?
        if ( ( instance_IN ) and ( instance_IN != None ) ):
    
            self.modhash = instance_IN.modhash             # base36 string for communicating with account
            self.reddit_id = instance_IN.id                # base36 id for a post (usually 5 characters)
            self.name = instance_IN.name                   # example: t1_czwe3. t# is content type, the rest is the ID
            self.title = django.utils.encoding.smart_text( instance_IN.title ).encode( 'ascii', 'xmlcharrefreplace' )                 # Title of post
            self.url = instance_IN.url                     # URL to post
            self.author_name = instance_IN.author          # Username of author
            self.domain = instance_IN.domain               # Domain posted ot
            self.subreddit_name = instance_IN.subreddit         # Subreddit posted to
            self.subreddit_reddit_id = instance_IN.subreddit_id
            self.permalink = instance_IN.permalink         # Link to the post (including comments)
            self.is_self = BooleanHelper.convert_value_to_boolean( instance_IN.is_self ) # Self-post?
            self.selftext = safe_string( instance_IN.selftext )           # Self-post text
            self.selftext_html = safe_string( instance_IN.selftext_html ) # HTML for self-post text
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
            self.author_flair_text = safe_string( instance_IN.author_flair_text )
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
    
    #-- END method set_fields_from_reddiwrap --#

    
    def create_reddiwrap_post( self, *args, **kwargs ):
    
        '''
        Creates a reddiwrap Post instance, populates it from this instance,
           returns the result.
        '''
    
        # return reference
        instance_OUT = None
    
        # declare variables
        
        # create instance
        instance_OUT = reddiwrap.ReddiWrap.Post()

        # populate instance.        
        instance_OUT.modhash = self.modhash             # base36 string for communicating with account
        instance_OUT.id = self.reddit_id                # base36 id for a post (usually 5 characters)
        instance_OUT.name = self.name                   # example: t1_czwe3. t# is content type, the rest is the ID
        instance_OUT.title = self.title                 # Title of post
        instance_OUT.url = self.url                     # URL to post
        instance_OUT.author = self.author_name          # Username of author
        instance_OUT.domain = self.domain               # Domain posted ot
        instance_OUT.subreddit = self.subreddit_name    # Subreddit posted to
        instance_OUT.subreddit_id = self.subreddit_reddit_id
        instance_OUT.permalink = self.permalink         # Link to the post (including comments)
        instance_OUT.is_self = self.is_self             # Self-post?
        instance_OUT.selftext = self.selftext           # Self-post text
        instance_OUT.selftext_html = self.selftext_html # HTML for self-post text
        instance_OUT.num_comments = self.num_comments   # Number of comments
        instance_OUT.score = self.score                 # upvotes - downvotes * crazy reddit vote fuzzing constant
        instance_OUT.upvotes = self.upvotes
        instance_OUT.downvotes = self.downvotes
        instance_OUT.over_18 = self.over_18 # NSFW post
        instance_OUT.created = self.created
        instance_OUT.created_utc = self.created_utc
        instance_OUT.num_reports = self.num_reports
        instance_OUT.banned_by = self.banned_by
        instance_OUT.approved_by = self.approved_by
        instance_OUT.link_flair_text = self.link_flair_text
        instance_OUT.link_flair_class = self.link_flair_class # link_flair_css_class": null,
        instance_OUT.author_flair_text = self.author_flair_text
        instance_OUT.author_flair_class = self.author_flair_class
        instance_OUT.clicked = self.clicked # If logged-in user has clicked link yet
        instance_OUT.hidden = self.hidden
        instance_OUT.saved = self.saved
        instance_OUT.edited = self.edited

        # what to do with these?
        '''
        self.comments      = [] # List of Comment objects that are replies to the Post
        self.has_more_comments = False # Contains comments that have not been loaded
        self.more_comments     = ''    # JSON data containing information about comments to load
        self.media_embed   = {}
        self.media         = None
        self.thumbnail     = ''
        '''

        return instance_OUT
    
    #-- END method create_reddiwrap_post --#


    def __str__(self):
        
        # return reference
        string_OUT = ""
        
        # id?
        if ( ( self.id ) and ( self.id != None ) and ( self.id > 0 ) ):
        
            string_OUT += "Post " + str( self.id )
        
        #-- END check to see if id --#
        
        # name
        if( self.name ):
        
            string_OUT += " - " + self.name
        
        #-- END check to see if name --#
        
        # title
        if( self.title ):
        
            string_OUT += " - " + self.title
        
        #-- END check to see if title --#
        
        # author_name
        if ( self.author_name ):
        
            string_OUT += " - by " + self.author_name
        
        #-- END cehcek for author_name --#
        
        return string_OUT

    #-- END __str__() method --#


#-- END Post model --#


@python_2_unicode_compatible
class Comment( models.Model ):

    #============================================================================
    # Django model fields.
    #============================================================================

    reddit_id = models.CharField( max_length = 255 )
    reddit_full_id = models.CharField( max_length = 255, null = True, blank = True )
    name = models.TextField( null = True, blank = True )
    link_id = models.CharField( max_length = 255 )
    parent = models.ForeignKey( 'self', null = True, blank = True )
    parent_reddit_id = models.CharField( max_length = 255, null = True, blank = True )
    author = models.ForeignKey( User, null = True, blank = True )
    author_name = models.TextField( null = True, blank = True )
    author_reddit_id = models.CharField( max_length = 255, null = True, blank = True )
    post = models.ForeignKey( Post, null = True, blank = True )
    post_reddit_id = models.CharField( max_length = 255, null = True, blank = True )
    body = models.TextField( null = True, blank = True )
    body_html = models.TextField( null = True, blank = True )
    subreddit = models.ForeignKey( Subreddit, null = True, blank = True )
    subreddit_name = models.TextField( null = True, blank = True )
    subreddit_reddit_id = models.CharField( max_length = 255, null = True, blank = True )
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
            self.reddit_id = instance_IN.id # reddit id (c9irgqx)
            self.reddit_full_id = instance_IN.name # type + reddit id (t1_c9irgqx)
            self.reddit_name = instance_IN.name # type + reddit id (t1_c9irgqx)
            self.link_id = instance_IN.link_id # type + reddit ID of parent post (t3_1cp0i3).
            self.parent_reddit_id = instance_IN.parent_id # reddit full ID of parent comment, if there is a parent.
            self.post_reddit_id = instance_IN.link_id # strip type?
            self.author_name = instance_IN.author # username of poster (UnixCurious)
            self.body = django.utils.encoding.smart_text( instance_IN.body  ).encode( 'ascii', 'xmlcharrefreplace' )
            self.body_html = django.utils.encoding.smart_text( instance_IN.body_html ).encode( 'ascii', 'xmlcharrefreplace' )
            self.subreddit_name = instance_IN.subreddit # name of subreddit
            self.subreddit_reddit_id = instance_IN.subreddit_id # type + reddit ID of subreddit.
            self.upvotes = instance_IN.upvotes
            self.downvotes = instance_IN.downvotes
            self.score = instance_IN.score
            self.created = instance_IN.created
            self.created_dt = datetime.datetime.fromtimestamp( int( self.created ) )
            self.created_utc = instance_IN.created_utc
            self.created_utc_dt = datetime.datetime.fromtimestamp( int( self.created_utc ) )
            self.edited = BooleanHelper.convert_value_to_boolean( instance_IN.edited )
            self.num_reports = instance_IN.num_reports
            self.banned_by = instance_IN.banned_by
            self.approved_by = instance_IN.approved_by
            self.flair_class = instance_IN.flair_class
            self.flair_text = safe_string( instance_IN.flair_text )
            
            # what to do about these?
            # self.children    = []
            # self.has_more_comments = False
            # self.more_comments = ''

        #-- END check to make sure instance passed in. --#
    
    #-- END method set_fields_from_reddiwrap --#


    def __str__(self):
        
        # return reference
        string_OUT = ""
        
        # id?
        if ( ( self.id ) and ( self.id != None ) and ( self.id > 0 ) ):
        
            string_OUT += "Comment " + str( self.id )
        
        #-- END check to see if id --#
        
        # name
        if( self.name ):
        
            string_OUT += " - " + self.name
        
        #-- END check to see if name --#
        
        # author_name
        if( self.author_name ):
        
            string_OUT += " - by " + self.author_name
        
        #-- END check to see if author_name --#
        
        # subreddit
        if( self.subreddit ):
        
            string_OUT += " - in /r/" + self.subreddit
        
        #-- END check to see if subreddit --#
        
        return string_OUT

    #-- END __str__() method --#


#-- END Comment model --#