# CLO835_FINALPROJECT_2023
Group final project for winter 2023 graduating class.

# Tasks Overview
Deploy Python Application with Persistent MySql Database on EKS (using Storage Class (SC), Persistent Volume (PV) and Persistent Volume Claim (PVC))

Prequisites: 
Docker Images are pushed to the ecr repository
EKS Cluster with 2 Worker Nodes is Deployed (eks cluster manifest (eks_config) is also in the repository)
Steps:
# Using Storage class and PVC

#Confirm that the cluster with 2 worker nodes is running
k get nodes
#Create base64 encoded password
echo -n 'admin' | base64
#Create storage class
k create -f storage_class.yaml -n grp1
#Create the Namspace
k create ns grp1
#Create the secrets
k create -f secret.yaml -n grp1                                                                                                                                                                                   
#Create configmap
k create -f config-map.yaml -n grp1                                                                                                                                                                                
#Create PVC
k create -f pvc.yaml -n grp1                                                                                                                                                                                       
#Create the deployment of the Database
k apply -f db-deployment.yaml -n grp1
#Create deployment of the cluster IP service for the Database
k create -f db-service.yaml -n grp1
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
#verify the data is in the mysql data base
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
