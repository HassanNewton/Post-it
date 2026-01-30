#!/bin/bash

if [ $# -ne 3 ]; then
    echo "Usage: $0 <URL> <RATE> <DURATION_SECONDS>"
    exit 1
fi

URL=$1
RATE=$2
DURATION=$3

echo "Starting workload generator..."
echo "URL: $URL"
echo "Rate: $RATE requests per iteration"
echo "Duration: $DURATION seconds"

END=$((SECONDS + DURATION))

while [ $SECONDS -lt $END ]; do
    echo "Sending $RATE requests..."
    for i in $(seq 1 $RATE); do
        curl -s -o /dev/null -w "%{http_code} " -X POST $URL \
             -H "Content-Type: application/json" \
             -d "{\"author\":\"user$i\",\"message\":\"test message $i\"}" &
    done
    wait
    echo ""
done

echo "Workload generator finished."
