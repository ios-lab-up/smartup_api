#!/bin/bash
URL="http://api:5555/FetchGroupDataUPSite"

max_retries=3
retries=0
delay=10

echo "Sending GET request to scrapper endpoint..."

while [ $retries -lt $max_retries ]
do
  response=$(curl -s -o /dev/null -w "%{http_code}" -X GET $URL)
  if [ "$response" -eq 200 ]
  then
    echo "Scrapper script completed."
    break
  else
    echo "Request failed with status code $response. Retrying in $delay seconds..."
    retries=$((retries+1))
    sleep $delay
  fi
done

if [ $retries -eq $max_retries ]
then
  echo "Maximum number of retries reached. Scrapper script failed."
fi
