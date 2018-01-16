

#    TrapHuman - Phishing OSINT MODULE    


# Authors 
(@networkseg1) - (@forges82) - traphuman[at]gmail.com

Version 1.0.0


# DESCRIPTION


Collection of python  and bash scripts which permit to feed a Database with information related to
phishing. 

The Drupal module will interact with the TrapHuman OSINT module.


** osint-tw.py: Python script to connect to Twitter Streamming API, downloading english or spanish phishing tweets and store them into 
a MariaDB in real time.

** database_osint.py: module to setup your Database parameters. This module is used in
osint-tw.py.

** DBosint_tw.sql: a sql file to create the OSINT database and all the tables needs.

** traphuman-twd.sh: Bash script to run osint-tw.py as a daemon. This script calls start_traphumna-tw.sh script.



# REQUIREMENTS


Debian -> Tested on Debian 9 64bits and python 3.4+


# INSTALLATION

<h3>Step 0: Choose a user/pass in order to your application is able to connect to OSINT database</h3>

--> Edit: DBosint_tw.sql

GRANT USAGE ON *.* TO 'myownuser'@localhost IDENTIFIED BY 'herethepassword';



<h3>Step 1: Run the script: setup.sh    (Installation Path: /opt/traphuman/osint/)</h3>

Set permissions: chmod +x setup.sh

This script installs and sets up:

--> All the needs debian and python packages.

--> A virtual version 3 python environment under /opt/traphuman/osint folder.

--> The MariaDB Database and create the osint DB and its tables. 

--> A crontab to improve our phishing collecting.

--> Copy all python scripts  under the /opt/traphuman/osint folder.

--> Copy the traphuman-twd.sh daemon to /usr/sbin/



<h3>Step 2: SETUP YOUR OWN TWITTER API</h3>


GET your token Tweeter API keys from: https://apps.twitter.com/ - Create New App and fill the
information.

Open the App page and click in Keys and Access Token. You will need:

consumer_key

consumer_secret

access_token

access_secret

-->  Edit /opt/traphuman/osint/osint-tw.py and set your own API Keys parameters.



<h3>Step 3: Setup your own Database application parameters</h3>


--> Edit /opt/traphuman/osint/lib/python/site-package/database_osint.py and set you own Database information. 




<h3>Step 4: START osint-tw</h3>

 
/usr/sbin/traphuman-twd.sh start

The script will start to collecting phishing tweets.

During the installation a crontab is setup. Review the crontab if you wish adjust it.



<h3>Step 5: Check the Logfile</h3>


/var/log/traphuman.log

Now, you could check your logfile: /var/log/traphuman.log for some issue, if everything is ok, you will see a line like this one:

     https://stream.twitter.com:443 "POST /1.1/statuses/filter.json?delimited=length HTTP/1.1" 200 None


# OTHER INFORMATION


<h3>Module installation path</h3>


/opt/traphuman/osint/


<h3>Crontab installed</h3>


5 2 * * * /usr/sbin/traphuman-twd.sh stop

5 7 * * * /usr/sbin/traphuman-twd.sh start


