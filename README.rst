IGReport
==========
The anonymous corruption reporting hotline for the Inspectorate of Government, code-named 'IGReport,' is built based on previous work by UNICEF for their anonymous hotline for reporting quality of health services.  It uses the RapidSMS core, as well as a number of community apps (rapidsms-httprouter, rapidsms-polls, and rapidsms-script).

Installation
==============
An example is deployed to an IG laptop, which has been configured following the directions described here.  These directions are also available at http://github.com/daveycrockett/rapidsms-training.

Basic Tools
-----------------

Most linux distributions come with python and git, but instructions for installing both can be found at http://git-scm.com/downloads  and http://www.python.org/getit/releases/2.7.3/.

Additional Python Tools
--------------------------
Once you have python and git, there are a few additional tools that make development and deployment easier.  These are easy_install, virtualenv, and virtualenvwrapper.

To install easy install, try::

    wget “http://peak.telecommunity.com/dist/ez_setup.py” 
    python ez_setup.py

Then, installing Virtual Environment (and making it usable) is easy::

    easy_install virtualenv
    easy_install virtualenvwrapper
    sudo mkdir /opt/env/
    
For now, change /opt/env to be world readable, we'll lock it down later (see the section titled 'Security')::

    sudo chown -R your_username:your_username /opt/env

Now, edit the global /etc/bash.bashrc file and add the following lines::

    export WORKON_HOME=/opt/env
    source /usr/local/bin/virtualenvwrapper.sh

Your path to virtualenvwrapper.sh may vary, be sure to verify it's in /usr/local/bin or /usr/bin.  You're now ready to begin installing IGReport itself!

Initial Deployment
---------------------
The paths described above (/opt/env/) and also the ones described here are important: the fabric deployment file at http://github.com/daveycrockett/fabulous assumes that you use the same folders to ensure a smooth, easy update process whenever the code changes.  Be sure to follow the instructions here carefully.

Install the Repo
``````````````````

First, create a virtual environment for the deployment, clone it into its production folder, and install its dependencies::

    mkvirtualenv igreport
    sudo mkdir -p /var/www/prod/igreport
    sudo chown -R your_username:your_username /var/www
    git clone git://github.com/daveycrockett/igreport /var/www/prod/igreport
    cd /var/www/prod/igreport
    git submodule init
    git submodule update
    pip install -r pip-requirements.txt

Some distros of linux may have issues installing psycopg2 directly, if you get an error message try running::

    sudo apt-get install libpq-dev

Configure the Database
`````````````````````````

IGReport requires Postgresql to be installed, as it uses some database-specific SQL.  Most distributions of linux come with postgres installed, but if not you should be able to install it via the package manager::

    sudo apt-get install postgresql

From there, configure the database user to have a password::

    sudo passwd postgres
    sudo -u postgres psql
   
From the psql prompt, run::

    \password postgres

Now, you should be ready to create a localsettings.py file in /var/www/prod/igreport/igreport_project::

    DATABASES = {
        'default': {
            'ENGINE' : 'django.db.backends.postgresql_psycopg2',
            'NAME': 'igreport',
            'HOST': 'localhost',
            'USER': 'postgres',
            'PASSWORD': 'YOUR PASSWORD',
            'ROUTER_URL': 'http://smgw1.yo.co.ug:9100/sendsms?ybsacctno=YBS_ACCOUNT_NUMBER&password=YBS_ACCOUNT_PASSWORD&origin=7008&sms_content=%(text)s&destionation=%(recipients)s',
        }
    }

    # Yo! wants only 100 recipients at a time
    MESSAGE_CHUNK_SIZE=100

Now that the database (and also the Yo! integration, as a bonus) are configured, you can execute all the sql needed to prepare the application::

    python manage.py syncdb
    python manage.py loaddata locations
    python manage.py create_script

You should now be able to verify that the app is ready to go by running `python manage.py runserver` and browsing to http://your.server.ip:8000/

Install and Configure Web Server Tools
``````````````````````````````````````````

That said, runserver was never intended to be a production server!  For a production server, a few additional tools will be required to ensure a quality, stable web application.  First, install and configure nginx, the web server that will dispatch requests to the python app::

    sudo apt-get install nginx

Nginx will install itself to the system startup, however the RapidSMS app itself and the messenger management command will not.  In order to make sure that those two processes stay up, you'll need to install supervisor through the package manager::

    easy_install supervisor

The configuration files for both of these are fairly well-documented, but it'll be much easier just to look at the configuration files for each that are already installed on the laptop, and tweak them as necessary::

    /etc/supervisor/supervisor.conf
    /etc/nginx/conf.d/igreport.conf

Security
````````````

Now that you're ready to get everything running, you'll need to add the www-data (although on most systems, it already exists), and then add yourself to the www-data group::

    cat /etc/passwd | grep www-data

If that doesn't return any lines, go ahead and add www-data::

    useradd -M -U www-data

Now, add yourself to the www-data group::

    groups
    usermod -g your-user-name -G comma,separated,list,of,results,of,groups,command,plus,www-data

Note that we're adding www-data to the comma-separated list of your existing groups (be sure to include sudo in the -G argument, or you'll lose your sudoers rights on the next login).

Finally, change all the working directories to the appropriate permissions::

    sudo chown -R www-data:www-data /opt/env
    sudo chown -R www-data:www-data /var/www
    sudo chmod -R ug+rwx /opt/env
    sudo chmod -R ug+rwx /var/www

Startup
````````

Now power cycle supervisord,  nginx and the supervised apps::

    $ sudo /etc/init.d/supervisord restart
    $ supervisorctl (you'll be prompted for a login and password)
    reread
    update
    quit
    $ sudo /etc/init.d/nginx restart

Script Scheduling
`````````````````````

RapidSMS-script relies on a cron to check for updates in script progress::

    sudo cp /var/www/prod/igreport/cron_igreport /etc/cron.d

Deploying Updates
--------------------

If you've installed fabric on your local machine::

    easy_install fabric

and cloned the fabfile repo::

    git clone git://github.com/daveycrockett/fabulous

Deploying is as easy as running::

    fab deploy igreport dest=prod

Test and Production Environments
----------------------------------

Ultimately, you'll want parallel running versions of the igreport code on the servers, for production and testing environments.

Simply duplicate the steps above for creating a database, cloning the repo, running the various management commands, and installing a supervisor process for a uwsgi socket for /var/www/test/igreport.  You can then update this with `fab deploy igreport`.

 
