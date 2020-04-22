# auto email
30 7 * * * python run.py >> /dev/null

# stop now docker
20 7 * * * ./scripts/service_start.sh >> /dev/null

# start stopped docker
40 7 * * * ./scripts/service_start.sh >> /dev/null
