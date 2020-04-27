# auto email
30 7 * * * python run.py > /dev/null 2>&1 &

# stop now docker
20 7 * * * ./scripts/service_stop.sh > /dev/null 2>&1 &

# start stopped docker
5 12 * * * ./scripts/service_start.sh > /dev/null 2>&1 &
