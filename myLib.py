import sqlite3 as lite
import reddiwrap.ReddiWrap as rdd

###########################################################
########################################################### General
###########################################################


def insert_row(values, table):
#	Insert values in table
	conn = lite.connect('reddit.sqlite')
	c = conn.cursor();		

	# making Question mark part
	qmark_str = "";
	for i in range(0, len(values)-1): qmark_str = qmark_str + "?,";
	qmark_str = qmark_str + "?";
	
	# Insert a row of data
	c.execute("INSERT INTO "+ table +" VALUES ("+ qmark_str +")", values)
	conn.commit()
	# We can also close the connection if we are done with it.
	# Just be sure any changes have been committed or they will be lost.
	conn.close()

def exsits_row(rowID, table):
#	checks if this row.id exists in the table or not
	conn = lite.connect('reddit.sqlite');
	c = conn.cursor();
	
	# c.execute('SELECT 1 FROM Post WHERE name=?', [post.id]); # it should be faster
	c.execute('SELECT * FROM '+ table +' WHERE id=?', [rowID]);
	
	if c.fetchone() == None:
		return False;
	return True;

def bool_to_int(boolvar):
	if str(boolvar) == "True":
		return 1;
	return 0;

def int_to_bool(intvar):
	if str(intvar) == "1":
		return True;
	return False;

###########################################################
########################################################### Subreddit
###########################################################
	

def retreive_subreddit(display_name):
	conn = lite.connect('reddit.sqlite');
	c = conn.cursor();
	c.execute('SELECT * FROM Subreddit WHERE display_name=?', [display_name]);
	# print c.fetchone()
	temp = c.fetchone();
	if temp == None:
		print "There is not any subreddit named "+ display_name + " in out database"	
	return temp;
	

############################################################
############################################################ Post
############################################################


def retrieve_post_traits(post):
#	return the list of traits of the given post. The list is in the order of the Post table
	over_18 = 0;
	if post.over_18:
		over_18 = 1;
	is_self = 0;
	if post.is_self:
		is_self = 1;
	
	# author_id is author_name right now.
	return [post.id, post.name, post.title, post.url, post.author, post.author, post.domain, post.subreddit, 
		post.subreddit_id, post.permalink, is_self,	post.selftext, post.num_comments, post.score, post.upvotes,
		post.downvotes, over_18, post.created, post.num_reports ]

def retrieve_post_traits2(post):
#	return the list of traits of the given post. The list is in the order of the Post table
	over_18 = 0;
	if post[16]:
		over_18 = 1;
	is_self = 0;
	if post[10]:
		is_self = 1;
	
	# author_id is author_name right now.
	return {'id' : post[0], 'name' : post[1], 'title': post[2], 'url' : post[3], 'author' : post[4], 'author' : post[5], 
			'domain' : post[6], 'subreddit' : post[7], 'subreddit_id' : post[8], 'permlink' : post[9], 
			'is_self' : is_self, 'selftext' : post[11], 'num_comments' : post[12], 'score' : post[13], 'upvotes' : post[14],
			'downvotes' : post[15], 'over_18' : over_18, 'created' : post[17], 'num_reports' : post[18] }



def posts_of_reddit(subreddit_id):
	conn = lite.connect('reddit.sqlite');
	c = conn.cursor();
	c.execute('SELECT * FROM Post WHERE subreddit_id=?', [subreddit_id]);
	return c.fetchall();

def make_post_obj(post):
	pstObj = rdd.Post();
	postDict = retrieve_post_traits2(post);
	
	pstObj.id = postDict['id'];
	pstObj.name = postDict['name'];
	pstObj.title = postDict['title'];
	pstObj.url = postDict['url'];
	pstObj.author = postDict['author'];
	pstObj.domain = postDict['domain'];
	pstObj.subreddit = postDict['subreddit'];
	pstObj.subreddit_id = postDict['subreddit_id'];
	pstObj.permalink = postDict['permlink'];	
	pstObj.is_self = int_to_bool(postDict['is_self']);
	pstObj.selftext = postDict['selftext'];
	pstObj.num_comments = postDict['num_comments'];
	pstObj.score = postDict['score'];
	pstObj.upvotes = postDict['upvotes'];
	pstObj.downvotes = postDict['downvotes'];
	pstObj.over_18 = int_to_bool(postDict['over_18']);
	pstObj.created =  postDict['created']; 
	pstObj.num_reports = postDict['num_reports'];
	
	return pstObj;
	
	
	
###########################################################
########################################################### Comments
###########################################################

def retrieve_comment_traits(comment):
#	return the list of traits of the given post. The list is in the order of the Post table
	editted = 0;
	if comment.edited:
		editted = 1;
	
	# author_id is author_name right now.
	return [comment.id, comment.name, comment.link_id, comment.parent_id, comment.author, comment.author, comment.link_id, comment.body, comment.subreddit, 
		comment.upvotes, comment.downvotes, comment.score, comment.created, editted, comment.num_reports ]
				

		
def iterate_comments(comment, depth=0):
	# Recursively iterate and 'pretty print' comments. 
	if isinstance(comment, list):
		to_it = comment
	else:
		to_it = comment.children;
		if not exsits_row(comment.id, "Comment"):
			insert_row(retrieve_comment_traits(comment), "Comment");
	for comm in to_it:
		iterate_comments(comm, depth + 1)
