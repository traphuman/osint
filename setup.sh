#!/bin/bash

debian_initialize() {
sc=$(readlink -f "$0")
scriptpath=$(dirname "$sc")
apt-get -qq update 
}

install_packages() {
echo "****************************************************"
echo "Installing packages................................."
echo "****************************************************"
apt-get update
apt-get -y install mariadb-server 
apt-get -y install build-essential libssl-dev libffi-dev python-dev
apt-get -y install python3
apt-get -y install python3-pip
apt-get -y install python3-venv
echo "   "
}

hardening_mysql_DB_system() {
echo "****************************************************"
echo "MySQL Secure Installation .........................."
echo "****************************************************"
mysql_secure_installation
echo "     "
echo "setting up mysql directory permissions:"
chown -R root:root /etc/mysql/
chmod 0644 /etc/mysql/my.cnf
echo "     "
echo "setting up mysql DB storage directory permissions:"
echo "     "
echo "setup mysql user shell:"
usermod -s /bin/false mysql > /dev/null 2>&1
}

run_sql_script() {
echo "***********************************"
echo "Creating OSINT DB...............   "
echo "***********************************"
echo "running DBosint-tw.sql script....... Intro your root DB password"
mysql -h "localhost" -u "root" "-p" < "./DBosint_tw.sql"
}


create_python_env() {
echo "**********************************************"
echo "Creating python3 virtual environment.......   "
echo "**********************************************"
mkdir -p /opt/traphuman/osint
python3 -m venv /opt/traphuman/osint
}

setup_osint_module() {
echo "**********************************************"
echo "Installing application and dependencies......."
echo "**********************************************"
chmod +x $scriptpath/start_traphuman-tw.sh
chmod +x $scriptpath/traphuman-twd.sh
cp $scriptpath/requirements.txt /opt/traphuman/osint/
cp $scriptpath/osint-tw.py /opt/traphuman/osint/
cp $scriptpath/start_traphuman-tw.sh /opt/traphuman/osint/
cp $scriptpath/traphuman-twd.sh /usr/sbin/
cp $scriptpath/README.md /opt/traphuman/osint/
cp $scriptpath/database_osint.py /opt/traphuman/osint/lib/python*/site-packages/

cd /opt/traphuman/osint
./bin/pip3 install -r ./requirements.txt > /dev/null 2>&1
}

activate_crontab() {
echo "*******************************************"
echo "Installing crontab........................."
echo "*******************************************"
#m h  dom mon dow   command
(crontab -l 2>/dev/null; echo "5 2 * * * /usr/sbin/traphuman-twd.sh stop") | crontab -
(crontab -l 2>/dev/null; echo "5 7 * * * /usr/sbin/traphuman-twd.sh start") | crontab -
}

debian_initialize;
install_packages;
hardening_mysql_DB_system;
run_sql_script;
create_python_env;
setup_osint_module;
activate_crontab;

