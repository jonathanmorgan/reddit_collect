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

- pull in our python code

        git clone ssh://<username>@data.jrn.cas.msu.edu/home/socs/git/reddit_collect.git
    
- cd back to the site's root directory

        cd ..
    
- cd into the reddit_socs directory.

        cd socs_reddit
    
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

    - For sqlite3:

        - figure out what file you want to hold the database.  For the initial implementation, we used reddit.sqlite in same directory as code (/home/socs/socs_reddit/reddit_collect/reddit.sqlite).
        - In settings.py, in the DATABASES structure:
            - set the ENGINE to "django.db.backends.sqlite3"
            - set the database NAME (path to file), USER and PASSWORD if you set one on the database.
            - If the database is not on localhost, enter a HOST.
            - If the database is listening on a non-standard port, enter a PORT.
        - Example:

## Notes

- Always have an integer primary key separate from the application-specific key, for troubleshooting your program.
- don't use breaks.  Single points of entry and exit, structure conditionals, loops so no breaks.
- for "main" programs, build them as class or static methods on a class, so they can be invoked in a script, but also easily invoked as part of a program, as well.
- sqlite database files are generally named *.sqlite

## TODO

- really look over and understand code.
- built models.  Update sqlite database, code so it has a separate unique ID, then reddit_id.
- Q - change names of tables to what django would make, or leave them as iman named them?  And in general, how to migrate this to mysql?  Need to change table names, switch to django models for queries, inserts, etc.