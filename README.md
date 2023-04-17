# CLO835_FINALPROJECT_2023
Group final project for winter 2023 graduating class.

Tasks
EKS Cluster with 2 Worker Nodes is Deployed (eks cluster manifest (eks_config) is also in the repository)

# Install the required MySQL package

sudo apt-get update -y
sudo apt-get install mysql-client -y

# Running application locally
pip3 install -r requirements.txt
sudo python3 app.py
# Building and running 2 tier web application locally
### Building mysql docker image 
```docker build -t my_db -f Dockerfile . ```

### Building application docker image 
```docker build -t my_app -f Dockerfile . ```

### Building the bridge network
```docker network create -d bridge --subnet 182.18.0.1/24 --gateway 182.18.0.1 grp1-network ```

### Running mysql
```docker run -d -e MYSQL_ROOT_PASSWORD=pw  --network grp1-network my_db```


### Get the IP of the database and export it as DBHOST variable
```docker inspect <container_id>```


### Example when running DB runs as a docker container and app is running locally
```
export DBHOST=182.18.0.2
export DBPORT=3306
```
### Example when running DB runs as a docker container and app is running locally
```
export DBHOST=182.18.0.2
export DBPORT=3306
```
```
export DBUSER=root
export DATABASE=employees
export DBPWD=pw
```
### Running the application, make sure it is visible in the browser
```docker run -p 8080:81  -e DBHOST=$DBHOST -e DBPORT=$DBPORT -e  DBUSER=$DBUSER -e DBPWD=$DBPWD --network grp1-network  my_app```

________________________________________________________________________________________________________________________________________________________________

# Main Tasks Overview
Deploy Python Application with Persistent MySql Database on EKS (using Storage Class (SC), Persistent Volume (PV) and Persistent Volume Claim (PVC))

Steps:
# Using Storage class and PVC

#To Confirm that the cluster with 2 worker nodes is running
k get nodes
#Create base64 encoded password
echo -n 'admin' | base64
#Create storage class
k apply -f storage_class.yaml -n grp1
#create namespace
k create ns grp1
#Create the secrets
k apply -f secret.yaml -n grp1                                                                                                                                                                                   
#Create configmap
k apply -f config-map.yaml -n grp1                                                                                                                                                                                
#Create PVC
k apply -f pvc.yaml -n grp1                                                                                                                                                                                       
#Create the deployment of the Database
k apply -f db-deployment.yaml -n grp1
#Create deployment of the cluster IP service for the Database
k apply -f db-service.yaml -n grp1
#Verify that the database and service has been created
k get all -n grp1
#Create the app deployment
k apply -f webapp-deployment.yaml -n grp1++++++++
#Create Service type Load Balancer for the application
k create -f webapp-service.yaml -n grp1
#Verify the app and its service has been deployed
k get all -n grp1
#get the external IP (URL) of the load balancer.
#Paste the url in a browser and the exposed port.
#Add some data into the database
#verify the data is in the mysql database
k exec -it pod/db-deployment-49bccdz45de-vd675 -n grp1 -- /bin/bash
mysql -p
admin
use employees;
select * from employee;
#Delete the running database pod
k delete <name of running database pod> -n grp1
#Verify that another db pod has been created to replace the deleted one
k get all -n grp1
#Delete the app pods as well so that the app deployemnt can replace with new pods
k delete <name of app pod1> <name of app pod2> -n grp1
#Verify new app pods were created
k get all -n grp1
#Navigate back to the browser, refresh the url and try to retrieve the data that was stored.
k exec -it pod/db-deployment-49bccdz45de-vd675 -n grp1 -- /bin/bash
mysql -p
admin
use employees;
select * from employee;
