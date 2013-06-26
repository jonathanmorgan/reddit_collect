# import praw - install: pip install praw
# Praw doc: https://praw.readthedocs.org/en/latest/index.html
import praw

# set user agent.
r = praw.Reddit( user_agent = 'reddit comment collector v0.1 by /u/jonathan_morgan' )

# retrieve a post with lots of comments - has over 22,000
post = r.get_submission( submission_id = "1bvkol" )

# use the replace_more_comments() method to pull in as many comments as possible.
post.replace_more_comments( limit = None, threshold = 0 )

# get the comments
comments = post.comments

# print out number of comments
print( len( comments ) ) # 3,915 and counting

# these are objects where parent comments reference children.  flatten...
flat_comments = praw.helpers.flatten_tree( post.comments )

# how many now?
print( len( flat_comments ) ) # 13364 - closer to 22000, but still not all of them.

# get a comment
test_comment = flat_comments[ 0 ]

# what is in it?
print( str( test_comment ) ) # outputs the text of comment, nothing more.

# reddit ID of comment:
print( test_comment.id )

# body of comment
print( test_comment.body )

# what other properties are there?
from python_utilities.objects.object_helper import ObjectHelper
test_attrs = ObjectHelper.get_user_attributes( test_comment.__class__, exclude_boring_IN = False )

# stunning - not storing things like votes for comments.

'''
{'__class__': <attribute '__class__' of 'object' objects>,
 '__delattr__': <slot wrapper '__delattr__' of 'object' objects>,
 '__dict__': <attribute '__dict__' of 'RedditContentObject' objects>,
 '__doc__': 'A class that represents a reddit comments.',
 '__eq__': <function praw.objects.__eq__>,
 '__format__': <method '__format__' of 'object' objects>,
 '__getattr__': <function praw.objects.__getattr__>,
 '__getattribute__': <slot wrapper '__getattribute__' of 'object' objects>,
 '__hash__': <slot wrapper '__hash__' of 'object' objects>,
 '__init__': <function praw.objects.__init__>,  
 '__module__': 'praw.objects',
 '__ne__': <function praw.objects.__ne__>,
 '__new__': <function __new__>,
 '__reduce__': <method '__reduce__' of 'object' objects>,
 '__reduce_ex__': <method '__reduce_ex__' of 'object' objects>,
 '__repr__': <slot wrapper '__repr__' of 'object' objects>,
 '__setattr__': <function praw.objects.__setattr__>,
 '__sizeof__': <method '__sizeof__' of 'object' objects>,
 '__str__': <function praw.objects.__str__>,
 '__subclasshook__': <method '__subclasshook__' of 'object' objects>,
 '__unicode__': <function praw.objects.__unicode__>,
 '__weakref__': <attribute '__weakref__' of 'RedditContentObject' objects>,
 '_get_json_dict': <function praw.objects._get_json_dict>,
 '_populate': <function praw.objects._populate>,
 '_update_submission': <function praw.objects._update_submission>,
 'approve': <function praw.objects.approve>,
 'clear_vote': <function praw.objects.clear_vote>,
 'delete': <function praw.objects.delete>,
 'distinguish': <function praw.objects.distinguish>,
 'downvote': <function praw.objects.downvote>,
 'edit': <function praw.objects.edit>,
 'from_api_response': <classmethod at 0x5319600>,
 'fullname': <property at 0x535c1b0>,
 'is_root': <property at 0x535c578>,
 'mark_as_nsfw': <function praw.objects.mark_as_nsfw>,
 'mark_as_read': <function praw.objects.mark_as_read>,
 'mark_as_unread': <function praw.objects.mark_as_unread>,
 'permalink': <property at 0x535c5d0>,
 'remove': <function praw.objects.remove>,
 'replies': <property at 0x535c628>,
 'reply': <function praw.objects.reply>,
 'report': <function praw.objects.report>,
 'score': <property at 0x535c680>,
 'submission': <property at 0x535c6d8>,
 'undistinguish': <function praw.objects.undistinguish>,
 'unmark_as_nsfw': <function praw.objects.unmark_as_nsfw>,
 'upvote': <function praw.objects.upvote>,
 'vote': <function praw.objects.vote>}
'''