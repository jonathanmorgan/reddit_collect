# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class Comment( models.Model ):

    #============================================================================
    # Django model fields.
    #============================================================================

    reddit_id = models.TextField(unique=True, blank=True)
    name = models.TextField(blank=True)
    link_id = models.TextField(blank=True)
    parent_id = models.TextField(blank=True)
    author_name = models.TextField(blank=True)
    author_id = models.TextField(blank=True)
    post_id = models.TextField(blank=True)
    body = models.TextField(blank=True)
    subreddit = models.TextField(blank=True)
    upvotes = models.IntegerField(null=True, blank=True)
    downvotes = models.IntegerField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)
    created = models.TextField(blank=True)
    edited = models.IntegerField(null=True, blank=True)
    num_reports = models.IntegerField(null=True, blank=True)

    #============================================================================
    # meta class
    #============================================================================

    class Meta:

        db_table = 'Comment'

    #-- END Meta class --#
    
#-- END Comment model --#


class Post(models.Model):

    reddit_id = models.TextField(unique=True, blank=True)
    name = models.TextField(blank=True)
    title = models.TextField(blank=True)
    url = models.TextField(blank=True)
    author_name = models.TextField(blank=True)
    author_id = models.TextField(blank=True)
    domain = models.TextField(blank=True)
    subreddit = models.TextField(blank=True)
    subreddit_id = models.TextField(blank=True)
    permalink = models.TextField(blank=True)
    is_self = models.IntegerField(null=True, blank=True)
    selftext = models.TextField(blank=True)
    num_comments = models.IntegerField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)
    upvotes = models.IntegerField(null=True, blank=True)
    downvotes = models.IntegerField(null=True, blank=True)
    over_18 = models.IntegerField(null=True, blank=True)
    created = models.TextField(blank=True)
    num_reports = models.IntegerField(null=True, blank=True)

    #============================================================================
    # meta class
    #============================================================================

    class Meta:
        db_table = 'Post'

    #-- END Meta class --#
    
#-- END Post model --#


class Subreddit(models.Model):

    #============================================================================
    # Django model fields.
    #============================================================================

    reddit_id = models.TextField(unique=True, blank=True)
    name = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    title = models.TextField(blank=True)
    url = models.TextField(blank=True)
    description = models.TextField(blank=True)
    created = models.TextField(blank=True)
    over_18 = models.IntegerField(null=True, blank=True)
    subscribers = models.IntegerField(null=True, blank=True)
    header_title = models.TextField(blank=True)

    #============================================================================
    # meta class
    #============================================================================

    class Meta:

        db_table = 'Subreddit'

    #-- END Meta class --#
    
#-- END Subreddit model --#


class User(models.Model):

    #============================================================================
    # Django model fields.
    #============================================================================

    reddit_id = models.TextField(unique=True, blank=True)
    created = models.TextField(blank=True)
    link_karma = models.IntegerField(null=True, blank=True)
    comment_karma = models.IntegerField(null=True, blank=True)

    #============================================================================
    # meta class
    #============================================================================

    class Meta:

        db_table = 'User'

    #-- END Meta class --#
    
#-- END User model --#