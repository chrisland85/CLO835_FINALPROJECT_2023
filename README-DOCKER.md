
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
```docker run -p 8080:8080  -e DBHOST=$DBHOST -e DBPORT=$DBPORT -e  DBUSER=$DBUSER -e DBPWD=$DBPWD -e APP_COLOR=red --network assignment1-network  my_app```