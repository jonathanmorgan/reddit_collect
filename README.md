# reddit_collect = data collector for reddit data.

This code collects and stores data from reddit in a database, using django ORM models to interact with database.

## Installation

- install pip

        (sudo) easy_install pip

- install django

        (sudo) pip install django

- in your work directory, create a django site.

        django-admin.py startproject socs_reddit
    
- cd into the reddit directory

        cd socs_reddit
    
- pull in reddiwrap

        git clone https://github.com/derv82/reddiwrap.git

- pull in Jon's python_utilities

        git clone https://github.com/jonathanmorgan/python_utilities.git

- pull in our python code

        git clone ssh://<username>@data.jrn.cas.msu.edu/home/socs/git/reddit_collect.git
    
- cd back to the site's root directory

        cd ..
    
- cd into the reddit_socs directory.

        cd socs_reddit

### Configure settings.py

- set USE_TZ to false to turn off time zone support:

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
    
    # optional, if you need to log in:
    reddit_collector.username = "<reddit_username>"
    reddit_collector.password = "<reddit_password>"
    
    # optional - also can set path to store cookies, if you want to persist them.
    reddit_collector.cookie_file_path = "cookies.txt"
    
    # just want a ReddiWrap instance?
    reddiwrap = reddit_collector.create_reddiwrap_instance()
    
### Reddiwrap Usage

    # search /r/all for posts from a specific sub-reddit
    reddiwrap.search( query = "subreddit:boston&limit=100", subreddit = "all", sort = "new" )
    
    # step through... Only gets 1000 - no more.  Have to pull all?
    while ( reddiwrap.has_next() == True ):
    
        # make sure you don't go over 2 transactions per second.
        reddiwrap.get_next()
    
    #-- END iteration over search results --#
    
    # try getting all from /r/all - see if we can step past 1000 results.
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

## Notes

- Always have an integer primary key separate from the application-specific key, for troubleshooting your program.
- don't use breaks.  Single points of entry and exit, structure conditionals, loops so no breaks.
- for "main" programs, build them as class or static methods on a class, so they can be invoked in a script, but also easily invoked as part of a program, as well.
- sqlite database files are generally named *.sqlite
- want created and updated timestamps on each table.
- place to store dates converted to datetime in database.

## TODO

- continue to look over and understand code.
- built models.  Update sqlite database, code so it has a separate unique ID, then reddit_id.
- Change table names, switch to django models for queries, inserts, etc.
- Q - do we need to keep checking in on posts, comments until they reach a certain stability criteria?  Or just for a certain time period?
- Q - Do we want time series on votes, voting, scores?
- // need mysql so we can have concurrency (scanning for and categorizing URLs, for example, while reddit collection is still ongoing).
- // need to work on the code for collection - gather user info?  check back in on posts, comments?
- Q - need a way to load JSON directly into django model instance, or is it OK to just load from ReddiWrapper objects?  For now, just using RediWrapper.