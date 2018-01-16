#! /bin/sh

PATH=/bin:/usr/bin:/sbin:/usr/sbin:/opt/traphuman/osint
DAEMON=/opt/traphuman/osint/start_traphuman-tw.sh
PIDFILE=/var/run/traphuman-tw.pid

test -x $DAEMON || exit 0

. /lib/lsb/init-functions

case "$1" in
start)
log_daemon_msg "Starting osint-tw"
start_daemon -p $PIDFILE $DAEMON
log_end_msg $?
;;
stop)
log_daemon_msg "Stopping osint-tw"
killproc -p $PIDFILE $DAEMON
PID=`ps x |grep osint-tw | head -1 | awk '{print $1}'`
kill -9 $PID       
log_end_msg $?
;;
force-reload|restart)
$0 stop
$0 start
;;
status)
status_of_proc -p $PIDFILE $DAEMON atd && exit 0 || exit $?
;;
*)
echo "Usage: /etc/init.d/osint-twd {start|stop|restart|force-reload|status}"
exit 1
;;
esac