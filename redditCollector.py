#!/usr/bin/python

import time
import sys

path = '/home/socs/socs_reddit/'
if path not in sys.path:
        sys.path.append(path)

import myLib
from reddiwrap.ReddiWrap import ReddiWrap

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


