### Description

This is a security camera which can be installed on any raspberry Pi which has a RGB camera attached to it
It is a motion sensing camera built using python, it captures photo when detects any motion ( Well tuned and can be used in farely dark places, like as a garage, parking lot or in front of the house camera)

## Photo

![Camera + Raspberry Pi module setup](camera_pi1.jpg)

### Requirements 

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

### Setup Instructions 



### Tasks

-   Implement a terraform configuration to create the required infrastructure on AWS.
-   Use terraform to 'deploy' the index.html ( application ) on the AWS infrastructure.
-   Ensure that the application can only be accessed from: 3.121.56.176

### Deliverables

Make sure to include all source code in this repository.

Please provide brief documentation as to why you chose a particular stack/setup.

Ensure that your terraform code can be executed and create the infrastructure
required and 'deploy' the single-page application.

You may use local state or remote state if you so choose.

### Evaluation Criteria

-   Terraform best practices.
-   Choice of infrastructure
-   Completeness: did you complete the features?
-   Correctness: does the functionality act in sensible, thought-out ways?
-   Maintainability: is it written in a clean, maintainable way?

### CodeSubmit

Please organize, design, test, and document your code as if it were
going into production - then push your changes to the master branch. After you have pushed your code, you may submit the assignment on the assignment page.

All the best and happy coding,

The ClearEstate Team

### Documentation 

-   Application is deployed using docker runtime. Dockerfile for the game app can be found under scripts/Dockerfile.game
-   Application is deployed on GCP using terraform. A virtual machine is spin up on GCP with a static IP address of 34.133.97.202 .
-   To publish to public a firewall policy is setup using terraform and attached to this VM 
-   Terraform installs docker runtime, git clones the game app and runs a bash script which runs the game application in container
-   Application running inside the container is maped to port 8000 of this VM
-   NOTE - Some things are done just for the sake of simplicity for example 
          - credentials folders contains ssh keys and gcp service account key for terraform to successfully run ( but those are temporary I will delete them in 2 days)
          - In production they can be extracted either from a vault server or Actions secrets
          - currently terraform state files are pushed in github, but in real production environment they can be maintained either on AWS s3 or GCP blob buckets or on a separate machine or NFS storage pool (path mounted onto the runners to access them)
### How to Run 

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
