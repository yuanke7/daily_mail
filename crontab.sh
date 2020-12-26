# auto email
16 7 * * 1-5 path/to/run.sh >> path/to/auto-mail/var/send.log 2>&1 &

21 11 * * 6,0 path/to/run.sh >> path/to/var/send.log 2>&1 &