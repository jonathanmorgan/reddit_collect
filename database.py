import sqlite3 as lite
conn = lite.connect('reddit.sqlite')

c = conn.cursor()



# Create table
c.execute('''CREATE TABLE User 
				(id text PRIMARY KEY,
				created text,
				link_karma integer,
				comment_karma integer)''');
				
c.execute('''CREATE TABLE Subreddit (
				id text PRIMARY KEY,
				name text,
				display_name text,
				title text, url text,
				description text,
				created text,
				over_18 integer,
				subscribers integer,
				header_title text)''');
				
c.execute('''CREATE TABLE Post (
				id text PRIMARY KEY, 
				name text, 
				title text, 
				url text, 
				author_name text, 
				author_id text, 
				domain text, 
				subreddit text,	
				subreddit_id text, 
				permalink text, 
				is_self integer, 
				selftext text, 
				num_comments integer, 
				score integer, 
				upvotes integer, 
				downvotes integer, 
				over_18 integer,
				created text, 
				num_reports integer)''')
				
c.execute('''CREATE TABLE Comment 
				(id text PRIMARY KEY, 
				name text, 
				link_id text, 
				parent_id text, 
				author_name text,
				author_id text, 
				post_id text, 
				body text, 
				subreddit text,
				upvotes integer, 
				downvotes integer,
				score integer, 
				created text, 
				edited integer, 
				num_reports integer)''')

		
# Delete Tables		
# c.execute('DROP TABLE IF EXISTS Post');
# c.execute('DROP TABLE IF EXISTS Subreddit');
# c.execute('DROP TABLE IF EXISTS User');
# c.execute('DROP TABLE IF EXISTS Comment');

		
		
# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()