# reddit_collect = data collector for reddit data.

This code collects and stores data from reddit in a database, using django ORM models to interact with database.

## Installation

- install pip

        (sudo) easy_install pip

- install django

        (sudo) pip install django

- in your work directory, create a django site.

        django-admin.py startproject <site_directory>
    
- cd into the site_directory

        cd <site_directory>
    
- pull in reddiwrap

        git clone https://github.com/derv82/reddiwrap.git

- pull in Jon's python_utilities

        git clone https://github.com/jonathanmorgan/python_utilities.git

- pull in our python code

        git clone ssh://<username>@data.jrn.cas.msu.edu/home/socs/git/reddit_collect.git
    
### Configure settings.py

- from the site_directory, cd into the site configuration directory, where settings.py is located (it is named the same as site_directory, but nested inside site_directory, alongside all the other django code you pulled in from git - <site_directory>/<same_name_as_site_directory>).

        cd <same_name_as_site_directory>

- in settings.py, set USE_TZ to false to turn off time zone support:

        USE_TZ = False

- configure the database in settings.py

    - For mysql:

        - create mysql database.
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

### Set up database

- Once database is configured in settings.py, in your site directory, run "python manage.py syncdb" to create database tables.
    
- If MySQL, for each column that could contain crazy unicode characters, then run SQL commands to explicitly set those columns to be utf8 and utf8_unicode_ci.  Here is SQL for the columns I've changed thus far:

    - columns on reddit\_collect\_post table:
    
            ALTER TABLE `socs_reddit`.`reddit_collect_post` CHANGE COLUMN `author_flair_text` `author_flair_text` longtext CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL;
            ALTER TABLE `socs_reddit`.`reddit_collect_post` CHANGE COLUMN `title` `title` longtext CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL;
            ALTER TABLE `socs_reddit`.`reddit_collect_post` CHANGE COLUMN `selftext` `selftext` longtext CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL;
            ALTER TABLE `socs_reddit`.`reddit_collect_post` CHANGE COLUMN `selftext_html` `selftext_html` longtext CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL;

    - columns on reddit\_collect\_comment table:
    
            ALTER TABLE `socs_reddit`.`reddit_collect_comment` CHANGE COLUMN `flair_text` `flair_text` longtext CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL;
            ALTER TABLE `socs_reddit`.`reddit_collect_comment` CHANGE COLUMN `body` `body` longtext CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL;
            ALTER TABLE `socs_reddit`.`reddit_collect_comment` CHANGE COLUMN `body_html` `body_html` longtext CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL;

- Create indexes on reddit IDs we use to check for duplicates/look up existing records (reddit ID, for example).  _This is really important!  As your table grows, an un-indexed lookup will slow WAY down!_

    - columns on the reddit\_collect\_post table:

            ALTER TABLE `socs_reddit`.`reddit_collect_post` ADD INDEX `reddit_id` (reddit_id);

    - columns on the reddit\_collect\_comment table:

            ALTER TABLE `socs_reddit`.`reddit_collect_comment` ADD INDEX `reddit_id` (reddit_id);
            ALTER TABLE `socs_reddit`.`reddit_collect_comment` ADD INDEX `reddit_full_id` (reddit_full_id);

- You might need to also tweak the mysql configuration.  On ubuntu, this is in /etc/mysql/my.cnf:

    - innodb\_buffer\_pool\_size - this defines how much memory the database can use as cache.  It defaults to 8 MB (to persist to disk relatively quickly).  To speed up import, you can bump it up to 50% of your total memory, or even closer to 80% if the machine is a dedicated database server.  On my box, for example, I have 20 GB of RAM, so I have it set to 8G (M = megabyte, G = gigabyte).
            
            innodb_buffer_pool_size = 8G
            
    - innodb\_flush\_log\_at\_trx\_commit - you can change this to 0 to allow the database to sync memory to disk less often (once a second, where the default of 1 forces sync after every commit).
    
            innodb_flush_log_at_trx_commit = 0
            
    - See [http://www.slideshare.net/osscube/mysql-performance-tuning-top-10-tips](http://www.slideshare.net/osscube/mysql-performance-tuning-top-10-tips) for more information.

## Usage

    # make sure the site directory is in the sys path.
    import sys
    site_path = '/home/socs/socs_reddit/'
    if site_path not in sys.path:
        
        sys.path.append( site_path )
        
    #-- END check to see if site path is in sys.path. --#
    
    # if not running in django shell (python manage.py shell), make sure django
    #    classes have access to settings.py
    # set DJANGO_SETTINGS_MODULE environment variable = "socs_reddit.settings".
    import os
    os.environ[ 'DJANGO_SETTINGS_MODULE' ] = "socs_reddit.settings"
    
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
    test_date = datetime.datetime( 2013, 4, 26, 0, 0, 0, 0 )
    reddit_collector.collect_posts( until_date_IN = test_date )
    
    # combine arguments to pick up where you left off.
    reddit_collector.collect_posts( until_date_IN = test_date, after_id_IN = "t3_1d63sm" )
    
    # or combine to test - just 350 posts, no more.
    reddit_collector.collect_posts( post_count_limit_IN = 350, after_id_IN = "t3_1d4wyy" )

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
    reddit_collector.collect_comments( comment_qs )
    
    # collect comments for all posts in /r/news in our data set.
    comment_rs = reddit_collect.models.Post.objects.filter( subreddit_name__iexact = 'news' ).order_by( '-created_utc_dt' )
    reddit_collector.collect_comments( comment_qs )
    
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

## TODO

- test code to collect comments.
- run that code on all posts in /r/boston and /r/news in our database (to start - can always grab more later as needed).

## Questions

- Q - do we need to keep checking in on posts, comments until they reach a certain stability criteria?  Or just for a certain time period?
- Q - Do we want time series on votes, voting, scores?
- Q - need to work on the code for collection - gather user info?  check back in on posts, comments?
- Q - need a way to load JSON directly into django model instance, or is it OK to just load from ReddiWrapper objects?  For now, just using RediWrapper.