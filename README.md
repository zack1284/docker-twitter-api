# docker-twitter-api

## Environment variables

From Twitter developmet account:

`export BEARER_TOKEN='AAAAAAAAAAAAAAAAAAAAAPYSVwEAAAAAOpAjc1LhwtsistR3%2Bta0%2FAMw3N4%3D1oTAtsKNkPEUakbi9xTznam4DBrjlZrEpqyMDNoO4fg68K8YaE'`

## Get docker images from docker hub

 ` sudo docker pull docker zack0410/docker-twitter-api:1.0`

## Run docker images

 ` sudo docker run -d zack0410/docker-twitter-api:1.0`

## Export docker container 

  `sudo docker export [container_id] > test.tar `
  
  The data will be written in test.tar > code > tweets.txt
  
## Access container

  `sudo docker exec -it [container_id] /bin/bash`
  
  
  
