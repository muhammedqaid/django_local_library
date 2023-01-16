# django_local_library
Local Library website written in Django. Primarily following the online tutorial from mdn web docs: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/ 

This branch is to continue with the tutorial through deployment using Railway. 

It includes: 
    - Procfile - As the web application "entry point" - listing commands to be executed by Railway to start the site
    - Setting up gunicorn (a pure-Python HTTP server). Don't need to for development, but install locally so it becomes part of requirements. !!NOTE< Gunicorn doesn't work on windows! Linux package>
    - Database configuration -using a database that runs its own process somewhere on the internet, accessed by application using an address passed as an environment variable (Doesn't have to be done this way, but can be). In this case using a postgres DB, also hosted on Railway. 
        Supplying database connection information to Django as environment variable "DATABASE_URL" 
        Also need to install: 
            dj-database-url for parsing this variable and automatically converting to correct configuration
            psycopg2 for django to interact with postgres
    - Run collectstatic to collect all static files into folder defined by static root. This is because it is inefficient to one webserver to serve both static and dynamic HTML. So we typically separate the static files from the django web application, making it easier to directly server from the web server or a content delivery network (CDN). 
        Important setings: 
            STATIC URL - base url location from which static fileswill be served
            STATIC ROOT - Absolute path to a directory where Django's collect static tool will gather any static files referenced in templates. 
            STATICFILES_DIRS - Lists additional directories that Django's collectstatic tool should search for static files
        collectstatic is run automatically by railway. Then WhiteNoise finds the files in the STATIC-ROOT and serves them
    - Set up WhiteNoise ^, to serve static files 
    - Set up requirements
        pip3 freeze > requirements.txt