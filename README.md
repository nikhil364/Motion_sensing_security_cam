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
- Connection to wifi or internet through a LAN cable
- Screen ( OPTIONAL )  

## System Requirements 
   - run this command in raspberry pi
 ```bash
    cat /etc/os-release
 ```
   - output must look like this or you might have to tweek the Dockerfile as per your OS specs
 
  ```bash
    PRETTY_NAME="Raspbian GNU/Linux 11 (bullseye)"
	NAME="Raspbian GNU/Linux"
	VERSION_ID="11"
	VERSION="11 (bullseye)"
	VERSION_CODENAME=bullseye
	ID=raspbian
	ID_LIKE=debian
	HOME_URL="http://www.raspbian.org/"
	SUPPORT_URL="http://www.raspbian.org/RaspbianForums"
	BUG_REPORT_URL="http://www.raspbian.org/RaspbianBugs"
 ```
 

## Setup Instructions on how to setup and test the camera 

- Clone and cd in the repo
```bash
git clone https://github.com/nikhil364/Motion_sensing_security_cam.git && cd Motion_sensing_security_cam
```

- Build the camera image 
```bash
docker build -t sec99 .
```
- Create a docker bridge network
```bash
docker network create security_camera
```
- PostgresSQL database setup  
```bash
docker run --name postgres -d --restart unless-stopped  -p 5432:5432 -e POSTGRES_PASSWORD=root -e  POSTGRES_USER=root -e  POSTGRES_DB=photos --network security_camera -v ${PWD}/data:/var/lib/postgresql/data postgres:12.2
```
- Run the camera  
```bash
sudo docker run -d  --name camera --network security_camera -v $(pwd):/app --pull never  -v ./photos:/app/photos -v ./extracted_photos_for_viewing:/app/extracted_photos_for_viewing  --device=/dev/video0 --privileged --restart unless-stopped  sec99 python3 security.py
```

## How to check if its working 
- its a motion sensing camera and ones there is some object in front of it moves it captures the photo and stores it in "photos" directory
- You can use it in your room when you leave the room and it will capture the photos of anyone coming there in your absence 
