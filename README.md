## Description

This is a security camera which can be installed on any raspberry Pi which has a RGB camera attached to it
It is a motion sensing camera built using python, it captures photo when detects any motion ( Well tuned and can be used in farely dark places, like as a garage, parking lot or in front of the house camera)

## Setup Photos

### Raspberry Pi and Camera module
![Camera + Raspberry Pi module setup](camera_pi1.jpg)

### Raspberry Pi and storage (Database for photos)
![Camera + Raspberry Pi module setup](camera_pi2.jpg)

## Requirements 

Hardware Requirements 
- Raspberry Pi 
- RGB Camera 
- SSD or any storage device attached to it

Software Requirenebts insode the Raspberry Pi 
- Docker 
- Docker Compose
- Ubuntu20.04 
- Connection to wifi or internet through a LAN cable
- Screen ( OPTIONAL )  

## Download Docker image for camera 
- package_download_token=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 

## Setup Instructions on how to setup and test the camera 


## How to Run 

-   Currently this application is running and can be accessed via http://34.133.97.202:8000/ 
-   To rerun this application clone the repository and go inside the repository 
-   Run the following command to spin up the docker container with terraform setup:
```bash
sudo bash scripts/gcp_deployment.sh 
``` 
-   Exec into the docker container 
```bash
docker exec -it terraform bash
```
-   Run the following command from inside the container which has terraform setup:
```bash
sudo terraform init &&  sudo terraform destroy -auto-approve && sudo terraform apply -target google_compute_firewall.dev-dev   -auto-approve && sudo terraform apply -target google_compute_instance.dev   -auto-approve
```
-   To ssh inside the machine on which the application is hosted use following command from inside the docker container only ( ssh can only be done from inside the container ):
```bash
sudo ssh -i /home/game/credentials/sample game@34.133.97.202
```
