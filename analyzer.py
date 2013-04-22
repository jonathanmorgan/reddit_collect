#!/usr/bin/python

from reddiwrap.ReddiWrap import ReddiWrap
import myLib
import time
import sys
import Tree
import sqlite3 as lite
import pickle




def main():
	# # step one: making graph based on a reddit
	# sebreddit_name  = 'FUNNY' 
	# graph_maker(sebreddit_name);

	


	fp = open("data/FUNNY", 'r');
	funny = pickle.load(fp);
	print "funny_max_width"
	fp = open("data/funny_max_width", 'w');
	for f in funny:
		res = f.get_max_width();
		fp.write(str(res[0]) + ',' + str(res[1]) + "\n")
	print "funny_leaves_hgh1"
	fp = open("data/funny_leaves_hgh1", 'w');
	for f in funny:
		fp.write(str(f.get_leaves_of_height(1)) + "\n");
	print "funny_unique_users"
	fp = open("data/funny_unique_users", 'w');
	for f in funny:
		fp.write(str(f.get_number_of_unique_users()) + "\n");
	
	
	
	fp = open("data/POLITICS", 'r');
	politics = pickle.load(fp);
	print "politics_max_width"
	fp = open("data/politics_max_width", 'w');
	for p in politics:
		res = p.get_max_width();
		fp.write(str(res[0]) + ',' + str(res[1]) + "\n")
	print "politics_leaves_hgh1"
	fp = open("data/politics_leaves_hgh1", 'w');
	for p in politics:
		fp.write(str(p.get_leaves_of_height(1)) + "\n");
	print "politics_unique_users"
	fp = open("data/politics_unique_users", 'w');
	for p in politics:
		fp.write(str(p.get_number_of_unique_users()) + "\n");
	
	
	
def graph_maker(sebreddit_name):
	conn = lite.connect('reddit.sqlite');
	c = conn.cursor();
	c.execute('SELECT * FROM Subreddit WHERE display_name=?', [sebreddit_name.lower()]);
	subreddit = c.fetchone();
	# # # # # # # # Saving Posts
	c.execute('SELECT * FROM Post WHERE subreddit_id=?', [subreddit[1]]);
	posts = c.fetchall();
	ROOTS = [];


	for post in posts:
		post_id = post[0];
		post_name = post[1];
		c.execute('SELECT * FROM Comment WHERE link_id=?', [post_name]);
		comments = c.fetchall();
	# if 2 == 2:	
		# comments = [
			# ['1' , '1', 'aaa', 'aaa', 'iman'],
			# ['2' , '2', 'aaa', '1' , 'nazie'],
			# ['3' , '3', 'aaa', '1' , 'sajjad'],
			# ['4' , '4', 'aaa', '3' , 'mehrdad'],
			# ['5' , '5', 'aaa', '3' , 'iman'],
			# ['6' , '6', 'aaa', '3', 'sahar'],
			# ['7' , '7', 'aaa', '2', 'sajjad'],
			# ['8' , '8', 'aaa', '2', 'nazie'],
			# ['9' , '9', 'aaa', '8', 'sajjad'],
			# ['10' , '10', 'aaa', 'aaa', 'fariborz'],
			# ['11' , '11', 'aaa', '10', 'iman'],
			# ['12' , '12', 'aaa', '11', 'mehrdad'],
			# ['13' , '13', 'aaa', '11', 'mitra'],		
			# ['14' , '14', 'aaa', 'aaa', 'nazie']
			# ];
		# root = Tree.CommentTree('aaa', 'aaa', 'aaa', True);
		
		
		root = Tree.CommentTree(post_name, post_name, post_name, True);
		ROOTS.append(root);
		tempParents = [root];
		
		while True:	
			futureParents = [];
			for prnt in tempParents:
				i = 0;
				indexes =[];
				for comment in comments:
					if comment[3] == prnt.name:
						# node = Tree.CommentTree(comment[1], comment[2], comment[3], comment[4], False);
						node = Tree.CommentTree(comment[1], comment[2], comment[3], False);
						node.set_attributes(comment);
						node.parent_node = prnt;
						prnt.children.append(node);
						futureParents.append(node);
						indexes.append(i);
					i = i + 1;
					
				for i in range(0,len(indexes)):
					j =  indexes[len(indexes) - i - 1];
					comments.pop(j);
			if futureParents == []:
				break
			tempParents = list(futureParents);
			
		

	fp = open("data/" + sebreddit_name, 'w');
	pickle.dump(ROOTS, fp);

	# fp = open("data", 'r');
	# m = pickle.load(fp);


#######################
# calling main function. This script just call this function.
main();

