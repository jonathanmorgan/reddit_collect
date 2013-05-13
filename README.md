# reddit_collect = data collector for reddit data.

This code collects and stores data from reddit in a database, using django ORM models to interact with database.

## Installation

- install pip

        (sudo) easy_install pip

- install django

        (sudo) pip install django

- in your work directory, create a django site.

        django-admin.py startproject <site_directory>
    
- cd into the site\_directory

        cd <site_directory>
    
- pull in reddiwrap

        git clone https://github.com/derv82/reddiwrap.git

- pull in Jon's python\_utilities

        git clone https://github.com/jonathanmorgan/python_utilities.git

- pull in our python code

        git clone https://github.com/jonathanmorgan/reddit_collect.git
    
### Configure

- from the site\_directory, cd into the site configuration directory, where settings.py is located (it is named the same as site\_directory, but nested inside site\_directory, alongside all the other django code you pulled in from git - <site\_directory>/<same\_name\_as\_site\_directory>).

        cd <same_name_as_site_directory>

- in settings.py, set USE_TZ to false to turn off time zone support:

        USE_TZ = False

- configure the database in settings.py

    - For mysql:

        - create mysql database.
            - at the least, make your database use character set utf8 and collation utf8_unicode_ci
            - To support emoji and crazy characters, in mysql >= 5.5.2, you can try setting encoding to utf8mb4 and collation to utf8mb4\_unicode\_ci instead of utf8 and utf8\_unicode\_ci.  It didn't work for me, but I converted the database instead of starting with it like that from scratch, so your mileage may vary.  If you need to do this to an existing database:

                    ALTER DATABASE <database_name> CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

        - create user to interact with mysql database.  Set permissions so user has all permissions to your database.
        - In settings.py, in the DATABASES structure:
            - set the ENGINE to "django.db.backends.mysql"
            - set the database NAME, USER, and PASSWORD.
            - If the database is not on localhost, enter a HOST.
            - If the database is listening on a non-standard port, enter a PORT.
        - Example:

                DATABASES = {
                    'default': {
                        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
                        'NAME': 'socs_reddit',                      # Or path to database file if using sqlite3.
                        # The following settings are not used with sqlite3:
                        'USER': 'socs_reddit',
                        'PASSWORD': '<mysql_password>',
                        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
                        'PORT': '',                      # Set to empty string for default.
                    }
                }

    - For sqlite3:

        - figure out what file you want to hold the database.  For the initial implementation, we used reddit.sqlite in same directory as code (/home/socs/socs_reddit/reddit_collect/reddit.sqlite).
        - In settings.py, in the DATABASES structure:
            - set the ENGINE to "django.db.backends.sqlite3"
            - set the database NAME (path to file), USER and PASSWORD if you set one on the database.
            - If the database is not on localhost, enter a HOST.
            - If the database is listening on a non-standard port, enter a PORT.
        - Example:

                DATABASES = {
                    'default': {
                        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
                        'NAME': '/home/socs/socs_reddit/reddit_collect/reddit.sqlite',                      # Or path to database file if using sqlite3.
                        # The following settings are not used with sqlite3:
                        'USER': '',
                        'PASSWORD': '',
                        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
                        'PORT': '',                      # Set to empty string for default.
                    }
                }


- Once database is configured in settings.py, in your site directory, run "python manage.py syncdb" to create database tables.

### Set up database - MySQL < 5.5.2 (and will work for all versions):

- If MySQL, for each column that could contain crazy unicode characters, run SQL commands to explicitly set those columns to be utf8 and utf8\_unicode\_ci.  Here is SQL for the columns I've changed thus far:

    - columns on reddit\_collect\_post table:
    
            ALTER TABLE `socs_reddit`.`reddit_collect_post` CHANGE COLUMN `author_flair_text` `author_flair_text` longtext CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL;
            ALTER TABLE `socs_reddit`.`reddit_collect_post` CHANGE COLUMN `title` `title` longtext CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL;
            ALTER TABLE `socs_reddit`.`reddit_collect_post` CHANGE COLUMN `selftext` `selftext` longtext CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL;
            ALTER TABLE `socs_reddit`.`reddit_collect_post` CHANGE COLUMN `selftext_html` `selftext_html` longtext CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL;

    - columns on reddit\_collect\_comment table:
    
            ALTER TABLE `socs_reddit`.`reddit_collect_comment` CHANGE COLUMN `flair_text` `flair_text` longtext CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL;
            ALTER TABLE `socs_reddit`.`reddit_collect_comment` CHANGE COLUMN `body` `body` longtext CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL;
            ALTER TABLE `socs_reddit`.`reddit_collect_comment` CHANGE COLUMN `body_html` `body_html` longtext CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL;

### Set up database - MySQL 5.5.2 or greater:

This didn't work for me personally, but the Internet says it should work, and it could have failed for me because I didn't start out with the database and tables configured this way (I changed them as outlined below).  At any rate, if I learn more, I'll update this, but you can try it, see what your mileage is.  If you get weird errors that look like this:

    Warning: Incorrect string value: '\xF0\x9F\x98\xA0' for column 'url' at row 1

Then it isn't working (that is a 4-byte Unicode character that MySQL's 3-byte limit for utf8 is choking on).

- If for some reason they aren't already, set all tables that might have emojis or other 4-byte unicode characters to have character set of utf8mb4 and collation of utf8mb4_unicode_ci (make sure to back up your database before you do this).  Example:

        ALTER TABLE `socs_reddit`.`reddit_collect_post` CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
        ALTER TABLE `socs_reddit`.`reddit_collect_comment` CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
        ALTER TABLE `socs_reddit`.`reddit_collect_subreddit` CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
        ALTER TABLE `socs_reddit`.`reddit_collect_user` CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
    
- If MySQL, for each column that could contain crazy unicode characters, then run SQL commands to explicitly set those columns to be utf8mb4 and utf8mb4\_unicode\_ci.  Here is SQL for the columns I've changed thus far:

    - columns on reddit\_collect\_post table:
    
            ALTER TABLE `socs_reddit`.`reddit_collect_post` CHANGE COLUMN `author_flair_text` `author_flair_text` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL;
            ALTER TABLE `socs_reddit`.`reddit_collect_post` CHANGE COLUMN `title` `title` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL;
            ALTER TABLE `socs_reddit`.`reddit_collect_post` CHANGE COLUMN `selftext` `selftext` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL;
            ALTER TABLE `socs_reddit`.`reddit_collect_post` CHANGE COLUMN `selftext_html` `selftext_html` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL;

    - columns on reddit\_collect\_comment table:
    
            ALTER TABLE `socs_reddit`.`reddit_collect_comment` CHANGE COLUMN `flair_text` `flair_text` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL;
            ALTER TABLE `socs_reddit`.`reddit_collect_comment` CHANGE COLUMN `body` `body` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL;
            ALTER TABLE `socs_reddit`.`reddit_collect_comment` CHANGE COLUMN `body_html` `body_html` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL;

### Set up database - all versions:

- Create indexes on reddit IDs we use to check for duplicates/look up existing records (reddit ID, for example).  _This is really important!  As your table grows, an un-indexed lookup will slow WAY down!_

    - columns on the reddit\_collect\_post table:

            ALTER TABLE `socs_reddit`.`reddit_collect_post` ADD INDEX `reddit_id` (reddit_id);

    - columns on the reddit\_collect\_comment table:

            ALTER TABLE `socs_reddit`.`reddit_collect_comment` ADD INDEX `reddit_id` (reddit_id);
            ALTER TABLE `socs_reddit`.`reddit_collect_comment` ADD INDEX `reddit_full_id` (reddit_full_id);

- You might need to also tweak the mysql configuration.  On ubuntu, this is in /etc/mysql/my.cnf:

    - set encoding parameters - MySQL < 5.5.2:
    
            init_connect            = 'SET NAMES utf8'
            character-set-server    = utf8
            collation-server        = utf8_unicode_ci

    - (optional/might not work) set encoding parameters - MySQL >= 5.5.2:
    
            init_connect            = 'SET NAMES utf8mb4'
            character-set-server    = utf8mb4
            collation-server        = utf8mb4_unicode_ci

    - innodb\_buffer\_pool\_size - this defines how much memory the database can use as cache.  It defaults to 8 MB (to persist to disk relatively quickly).  To speed up import, you can bump it up to 50% of your total memory, or even closer to 80% if the machine is a dedicated database server.  On my box, for example, I have 20 GB of RAM, so I have it set to 8G (M = megabyte, G = gigabyte).
            
            innodb_buffer_pool_size = 8G
            
    - innodb\_flush\_log\_at\_trx\_commit - you can change this to 0 to allow the database to sync memory to disk less often (once a second, where the default of 1 forces sync after every commit).
    
            innodb_flush_log_at_trx_commit = 0
            
    - See [http://www.slideshare.net/osscube/mysql-performance-tuning-top-10-tips](http://www.slideshare.net/osscube/mysql-performance-tuning-top-10-tips) for more information.

## Usage

There are also useful example scripts (including shell\_init.py, which you can run in a shell started with "python manage.py shell" to create instances of the collector and the reddiwrap object) in reddit\_collect/examples.

### Getting started and initialization

The easiest way to run code from a shell is to go to your django sites folder and use manage.py to open a shell:

    python manage.py shell
    
If you choose, you can also just open the base python interpreter:

    python
    
Or you can install something fancier like ipython, and then run ipython:

    ipython
    
If you don't use manage.py to open a shell (or if you are making a shell script that will be run on its own), you'll have to do a little additional setup to pull in and configure django:

    # make sure the site directory is in the sys path.
    import sys
    site_path = '<site_folder_full_path>'
    if site_path not in sys.path:
        
        sys.path.append( site_path )
        
    #-- END check to see if site path is in sys.path. --#
    
    # if not running in django shell (python manage.py shell), make sure django
    #    classes have access to settings.py
    # set DJANGO_SETTINGS_MODULE environment variable = "<site_folder_name>.settings".
    import os
    os.environ[ 'DJANGO_SETTINGS_MODULE' ] = "<site_folder_name>.settings"

Then, regardless, you'll need to do the following to set up the collector:

    # import the RedditCollector class
    from reddit_collect.redditCollector import RedditCollector
    
    # make an instance
    reddit_collector = RedditCollector()
    
    # initialize bare minimum connection parameters.
    reddit_collector.user_agent = "reddit post collector v0.1 by /u/jonathan_morgan"
    
    # OR reddit_collector.user_agent = "reddit comment collector v0.1 by /u/jonathan_morgan"
    
    # optional, if you need to log in:
    reddit_collector.username = "<reddit_username>"
    reddit_collector.password = "<reddit_password>"
    
    # optional - also can set path to store cookies, if you want to persist them.
    reddit_collector.cookie_file_path = "cookies.txt"
    
    # optional - if your version of mysql doesn't support utf8mb4 (unicode
    #    characters greater than 3-bytes), set this to true and it will keep all
    #    unicode characters 3 bytes and less, turn those that are 4 bytes long
    #    into XML entities, so they are preserved, but don't break database.
    # set to escape 4-byte Unicode characters (cursed mysql).
    reddit_collector.convert_4_byte_unicode_to_entity = True

### Collect Posts

    #============================================================================
    # ==> Collect Posts    
    #============================================================================

    # collect latest 10 entries from /r/all, store them in database.
    reddit_collector.collect_posts( 10 )
    
    # collect posts until you get to ID 1d64j4
    reddit_collector.collect_posts( -1, "t3_1d64j4" )
    
    # OR, posts through ID 1d68lz
    reddit_collector.collect_posts( until_id_IN = "t3_1d68lz" )
    
    # collect posts through date - start of 2013/04/26
    boundary_date = datetime.datetime( 2013, 4, 26, 0, 0, 0, 0 )
    reddit_collector.collect_posts( until_date_IN = boundary_date )
    
    # in the event of a crash, find ID of last record retrieved, then combine
    #    arguments to pick up where you left off.
    reddit_collector.collect_posts( until_date_IN = boundary_date, after_id_IN = "t3_1d63sm" )
    
    # or combine to test - just 350 posts, no more.
    reddit_collector.collect_posts( post_count_limit_IN = 350, after_id_IN = "t3_1d4wyy" )

### Collect Comments

    #============================================================================
    # ==> Collect Comments
    #============================================================================

    # first, retrieve one or more posts from database using Django QuerySets
    # - https://docs.djangoproject.com/en/dev/ref/models/querysets/

    # for now, one post.
    import reddit_collect.models
    post_qs = reddit_collect.models.Post.objects.filter( reddit_id = '1cp0i3' )
    
    # num_comments?
    django_post = post_qs[ 0 ]
    print( django_post.num_comments ) # 115, at time of collection
    
    # pass the QuerySet to the collect_comments() method.
    reddit_collector.collect_comments( post_qs )
    
    # collect comments for all posts in /r/boston in our data set.
    comment_rs = reddit_collect.models.Post.objects.filter( subreddit_name__iexact = 'boston' ).order_by( '-created_utc_dt' )
    reddit_collector.collect_comments( comment_rs )
    
    # collect comments for only posts in /r/boston that are 'new'.
    comment_rs = reddit_collect.models.Post.objects.filter( subreddit_name__iexact = 'boston' )
    comment_rs = comment_rs.filter( comment_collection_status = 'new' )
    comment_rs = comment_rs.order_by( '-created_utc_dt' )
    reddit_collector.collect_comments( comment_rs )
    
    # collect comments for all posts in /r/news in our data set.
    comment_rs = reddit_collect.models.Post.objects.filter( subreddit_name__iexact = 'news' ).order_by( '-created_utc_dt' )
    reddit_collector.collect_comments( comment_rs )

    # collect comments for only posts in /r/news that are 'new'.
    comment_rs = reddit_collect.models.Post.objects.filter( subreddit_name__iexact = 'news' )
    comment_rs = comment_rs.filter( comment_collection_status = 'new' )
    comment_rs = comment_rs.order_by( '-created_utc_dt' )
    reddit_collector.collect_comments( comment_rs )
    
    
### RedditCollector.collect_posts() parameters:

- _subreddit\_IN_ - defaults to "all". Subreddit you want to collect from.
- _post\_count\_limit\_IN_ - number of posts we want to collect.
- _until\_id\_IN_ - value of ID we collect until we encounter in the stream (should include type - so begin with "t3_").
- _until\_date\_IN_ - datetime instance of UTC/GMT date and time we want to collect to (will stop collecting once a date after this is encountered).
- _subreddit\_in\_list\_IN_ - list of subreddits to limit our collection to (each should begin with "t5_").  If you use this, in most cases, you should leave subreddit_IN = "all".
- _after\_id\_IN_ - ID you want to get posts after.  Must include type (start with "t3_").  Use this to start at a point in time earlier than the present - to collect from a certain date, find a post around the date you want, collect from that ID on using the after_id_IN parameter.
- _before\_id\_IN_ - ID before which you want posts.  Must include type (start with "t3_").

### Reddiwrap Usage

    # just want a ReddiWrap instance?  Initialize collecter like above, then...
    reddiwrap = reddit_collector.create_reddiwrap_instance()
    
    # search /r/all for posts from a specific sub-reddit
    reddiwrap.search( query = "subreddit:boston&limit=100", subreddit = "all", sort = "new" )
    
    # step through... Only gets 1000 - no more.  Have to pull all?
    while ( reddiwrap.has_next() == True ):
    
        # make sure you don't go over 2 transactions per second.
        post_list = reddiwrap.get_next()
    
    #-- END iteration over search results --#
    
    # try getting all from /r/all
    post_list = reddiwrap.get( "/r/%s/new?limit=100" % "all" )
    
    # get first post in list.
    test_post = post_list[ 0 ]

    # create django model instance.
    import reddit_collect.models
    django_post = reddit_collect.models.Post()

    # populate from test_post
    django_post.set_fields_from_reddiwrap( test_post )
    
    # save to database.
    django_post.save()
    
    # ==> Comments
    
    # from database, find a post with lots of comments (t3_1cp0i3) and load it.
    comment_django_post = reddit_collect.models.Post.objects.get( reddit_id = '1cp0i3' )

    # create a reddiwrap Post instance from django Post.
    comment_rw_post = comment_django_post.create_reddiwrap_post()
    
    # get comments.
    reddiwrap.fetch_comments( comment_rw_post )
    
    # top-level comment list
    comment_list = comment_rw_post.comments
    
    # get 1st comment.
    test_comment = comment_list[ 0 ]
    
    # print out details
    print( test_comment.verbose() )
    
    # get children
    comment_responses = test_comment.children
    
    # get a child
    test_child = comment_responses[ 0 ]
    
    # etc.

## Notes

- Added an an integer primary key separate from the application-specific key, for troubleshooting, django support.
- added created and updated timestamps on each table.
- date columns that end in "_dt" store dates converted from unix timestamp to datetime in database.
- using bulk_create() to insert the Posts into the database instead of saving each (1 query instead of 100 for each set of 100...).
- there is some django memory management code used that you should be aware of:

        # memory management.
        gc.collect()                # force garbage collection by python.
        django.db.reset_queries()   # clear query caches (they get quite big if a program runs long enough).
        
- utf8 vs. utf8mb4 in mysql:
    - Detecting strings that have 4-byte unicode - 1: [http://stackoverflow.com/questions/3220031/how-to-filter-or-replace-unicode-characters-that-would-take-more-than-3-bytes](http://stackoverflow.com/questions/3220031/how-to-filter-or-replace-unicode-characters-that-would-take-more-than-3-bytes)
    - Detecting strings that have 4-byte unicode - 2: [http://stackoverflow.com/questions/10798605/warning-raised-by-inserting-4-byte-unicode-to-mysql](http://stackoverflow.com/questions/10798605/warning-raised-by-inserting-4-byte-unicode-to-mysql)
    - Converting mysql databases and tables from utf8 to utf8mb4 - basic: [http://dba.stackexchange.com/questions/8239/how-to-easily-convert-utf8-tables-to-utf8mb4-in-mysql-5-5](http://dba.stackexchange.com/questions/8239/how-to-easily-convert-utf8-tables-to-utf8mb4-in-mysql-5-5)
    - Converting mysql databases and tables from utf8 to utf8mb4 - detailed: [http://mathiasbynens.be/notes/mysql-utf8mb4](http://mathiasbynens.be/notes/mysql-utf8mb4)

## TODO

- implement a way to load Django models directly from JSON.
- add ability to update existing posts, comments, not just ignore if already present.
- add ability to pull in information on subreddits, users.
- improve rate-limited code so we can have multiple scrapers going at once, coordinated by central traffic cop (re-usable for other projects, as well).

## Questions

- Q - do we want ability to keep checking in on posts, comments until they reach a certain stability criteria?  Or just for a certain time period?
- Q - Do we want time series on votes, voting, scores?
- Q - praw or rediwrapper?

## License:

Copyright 2012, 2013 Jonathan Morgan

This file is part of [http://github.com/jonathanmorgan/reddit_collect](http://github.com/jonathanmorgan/reddit_collect).

reddit\_collect is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Foobar is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with [http://github.com/jonathanmorgan/reddit_collect](http://github.com/jonathanmorgan/reddit_collect).  If not, see
[http://www.gnu.org/licenses/](http://www.gnu.org/licenses/).