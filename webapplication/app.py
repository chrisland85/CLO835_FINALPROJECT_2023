import os
from flask import Flask, render_template, request
from pymysql import connections
import boto3
import random
import argparse


app = Flask(__name__)

DBHOST = os.environ.get("DBHOST") or "localhost"
DBUSER = os.environ.get("DBUSER") or "root"
DBPWD = os.environ.get("DBPWD") or "pw"
DATABASE = os.environ.get("DATABASE") or "employees"
COLOR_FROM_ENV = os.environ.get('APP_COLOR') or "lime"
#DBPORT = int(os.environ.get("DBPORT"))
DBPORT = 3306 


# Connect to the S3 bucket
s3 = boto3.resource('s3')
bucket_name = 'clo835-finalproject-2023'
bucket = s3.Bucket(bucket_name)
image_key = 'ilovecats.jpg'
s3_url = f'https://{bucket_name}.s3.amazonaws.com/{image_key}'
imageurl = f'https://{bucket_name}.s3.amazonaws.com/{image_key}'


# Create a connection to the MySQL database
db_conn = connections.Connection(
    host= DBHOST,
    port=DBPORT,
    user= DBUSER,
    password= DBPWD, 
    db= DATABASE
    
)
output = {}
table = 'employee';

imageurl = "https://clo835-finalproject-winter2023.s3.us-east-1.amazonaws.com/ilovedogs.jpeg?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEEIaCXVzLWVhc3QtMiJGMEQCIB0Y%2BPI0roCY6ENhavN1RC8DSawZdIjVp83dq36611QYAiALbmQvcWjJh3MjYW7xr44yt8MdMgXUSkKvZwM9QC1YNCr3Agg7EAAaDDQ0ODg3MDcyMTIzMCIMXUgFItwTL5NeJfwZKtQCx%2BbYAFBBsKYocCMxtH4MI1zmmmaeLwt55Oot01SaxNZBzGJjSlOLYYVJDHMh6tPMPyws9mbbWMu5TKpiOqGEa0W52U6h7waWhuCzz2p7O7AVg4JVEZmc0V40C68zTUxxDM5ohZxJwd8DUdlNehqbDkUvN72ubRdeF8yU6lHOsRxw7qveQVSJP6Hg361IOInXztDpKsNrYS1Uk9IZiZ51703YRlasE5yinO9%2BZY84eirOzQAouhQrbWzU5PeYHwFXj16F7kY5LHyQLhMsD2ywpFYCkXRVV5l4lrpbGwBg%2FaN%2BirIl2%2Fgi1%2FSGDk4L87oS%2FAlWfMfVfSq0UkqTl4PZ0ttMTzISRL7B9IX3pz1D56QqmgSwH2i%2BRFdTyCfS4le8JtzgjYC5yd%2BS1VYaLcJcywO0Z6kqw1tTfOJrqmJ3qJBPMDvd8K1XPrIuoaE0%2BD0FkoFj2jCYnvKhBjqIAkLTAtqXNfEeLxCIv27mWuplKOau8IrJCvgB%2BfHM%2BWV9hJjLcXRHWPGHMFb3EuO1dRL1koSNJEE%2FgNuQN%2BkP4FQhnXE%2Bbt%2BtOvkvfkUtoXVvDORMxIlvQL00wKpZhCbWV4uB0HAS2T8NYYXLbN0ZX6%2B7hFPBFxpwx2PU%2BZ8R9EuXpQsaj3ZOh2ZJcKhiI8kZmqTUOiV1oewA7h9ldpe7qrUHoCZxouAf9SGX3KtzZXfJpatTvt0xNwiMDZWJDW%2FVFZFsOfMaO758%2B1yjPE3ll%2BJ%2F%2Fzr9o9BYGcX1osMauXVgHr%2B0GgLS1LDwVbwRjkR6vinroNL9fbyiC%2B0dBNNlsfsmbWgQkG7D%2FQ%3D%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20230417T020223Z&X-Amz-SignedHeaders=host&X-Amz-Expires=720&X-Amz-Credential=ASIAWRAWHU3HHKN5D7FD%2F20230417%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=e8dbf90edea71d3ffd0e02633b79995079d7fc5c5a55f64b70d3610e51e987c8";

# Define the supported color codes
color_codes = {
    "red": "#e74c3c",
    "green": "#16a085",
    "blue": "#89CFF0",
    "blue2": "#30336b",
    "pink": "#f4c2c2",
    "darkblue": "#130f40",
    "lime": "#C1FF9C",
}


# Create a string of supported colors
SUPPORTED_COLORS = ",".join(color_codes.keys())

# Generate a random color
COLOR = random.choice(["red", "green", "blue", "blue2", "darkblue", "pink", "lime"])


@app.route("/", methods=['GET', 'POST'])
def home():
    imageurl = "https://clo835-finalproject-2023.s3.amazonaws.com/ilovecats.jpg";
    s3_url = "s3://clo835-finalproject-2023/ilovecats.jpg"
    return render_template('addemp.html', imageurl=imageurl)

@app.route("/about", methods=['GET','POST'])
def about():
    imageurl = "https://clo835-finalproject-2023.s3.amazonaws.com/ilovecats.jpg";
    return render_template('about.html', imageurl=imageurl)
    
@app.route("/addemp", methods=['POST'])
def AddEmp():
    emp_id = request.form['emp_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    primary_skill = request.form['primary_skill']
    location = request.form['location']

  
    insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()

    try:
        
        cursor.execute(insert_sql,(emp_id, first_name, last_name, primary_skill, location))
        db_conn.commit()
        emp_name = "" + first_name + " " + last_name

    finally:
        cursor.close()

    print("all modification done...")
    return render_template('addempoutput.html', name=emp_name, imageurl=imageurl)

@app.route("/getemp", methods=['GET', 'POST'])
def GetEmp():
    return render_template("getemp.html",imageurl=imageurl)


@app.route("/fetchdata", methods=['GET','POST'])
def FetchData():
    emp_id = request.form['emp_id']

    output = {}
    select_sql = "SELECT emp_id, first_name, last_name, primary_skill, location from employee where emp_id=%s"
    cursor = db_conn.cursor()

    try:
        cursor.execute(select_sql,(emp_id))
        result = cursor.fetchone()
        
        # Add No Employee found form
        output["emp_id"] = result[0]
        output["first_name"] = result[1]
        output["last_name"] = result[2]
        output["primary_skills"] = result[3]
        output["location"] = result[4]
        
    except Exception as e:
        print(e)

    finally:
        cursor.close()

    return render_template("getempoutput.html", id=output["emp_id"], fname=output["first_name"],
                           lname=output["last_name"], interest=output["primary_skills"], location=output["location"], imageurl=imageurl)

if __name__ == '__main__':
    
    # Check for Command Line Parameters for color
    parser = argparse.ArgumentParser()
    parser.add_argument('--color', required=False)
    args = parser.parse_args()

    if args.color:
        print("Color from command line argument =" + args.color)
        COLOR = args.color
        if COLOR_FROM_ENV:
            print("A color was set through environment variable -" + COLOR_FROM_ENV + ". However, color from command line argument takes precendence.")
    elif COLOR_FROM_ENV:
        print("No Command line argument. Color from environment variable =" + COLOR_FROM_ENV)
        COLOR = COLOR_FROM_ENV
    else:
        print("No command line argument or environment variable. Picking a Random Color =" + COLOR)

    # Check if input color is a supported one
    if COLOR not in color_codes:
        print("Color not supported. Received '" + COLOR + "' expected one of " + SUPPORTED_COLORS)
        exit(1)

    app.run(host='0.0.0.0',port=81,debug=True)
