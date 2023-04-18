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

imageurl = "https://clo835-finalproject-group1bucket.s3.us-east-1.amazonaws.com/ilovedogs.jpeg?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEGQaCXVzLWVhc3QtMiJHMEUCIAngvnqf7TPNQwHcBYmTXH3b0wXyEDP35GATohY0Rij9AiEAiYgIdy7R8tJIR1aWHe0p2XReSVm978ywa33N9P2sbwIq9wIIXhAAGgw0NDg4NzA3MjEyMzAiDBvR9TtjRR4JKS%2BejyrUArystIo7HdlvyTOtwVOLRuOqZVvVOHuF6J87REOJxdbB4%2BlsfKWIZ4PF82bVh%2BLoXqWezkZ7gSm1VaZmIAs%2BCIGr4JiVK%2Buv3%2F7sQ5W7sTPwCJyvJbaO7d6aA2ZKOKl4vPykAbH651cXPUT3Og87VtBCVfW6ibvsXRuYb58nD2IYLNXVIq8P9YKehksxLtjMUBCttGBucnUcYTfKBe345qRE8rp%2BfJqph9DJt%2F2vyxscSe6n8Bq8pNqmfZBwpgRMdo%2FoojWpuj%2FOoj7xlO9SoASOxumGiuMbHM2HpCwdYFOAnnOFy7Pa8rrHGmNWyjdQEU3xV%2F%2FcggP5g7RW4AasJJb6lBKxALddhLEcJSnJ2i6txlOiTIna%2FpyRquCy02rEqoB05m6lfOoYMcuHU%2BO5Ubc7HRCgJSe6fwRNqxz%2BN%2B888zrZldzm9rldfPfBFc2pzFIHu94wloj6oQY6hwJBPnTfm7nyuNo8%2BkeZyTL5nZd4JrFEe90iJP1wO2iCRlNPxVMdqESJ6D2RqtiUnkMmFAkFiUiSV%2BlYJToujaxNi9jLShuZ%2BbnNbkMV4Ck7yO1%2B0c1TQyT0cAmtOOHtqukkPYyYTMDkFEsC%2BvgLYp7ancZWOekJiiYBbt5ixlQe%2BLLjIehI8fRLrx%2Fuh2tkV3plTZCUWwTI84OAV7z2UqOcY%2Br1pe8zVhAsDpF0EQas3c7RKmaMi9Q5XFE3PUqn%2BlNzi8tACaTtKI90iLaBN1NrFaVhQ7ArSg7S1F6tC2MQyWu5BJm2kdU3PZ4tciZejhykQovhzdOXbLbx7DT9AHx%2FZJNTQETdoQ%3D%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20230418T123038Z&X-Amz-SignedHeaders=host&X-Amz-Expires=43200&X-Amz-Credential=ASIAWRAWHU3HDNFKAPX2%2F20230418%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=c99937897a58d40e83f7a7fdf56df8e4177cd5547f1454abe1b3f33e239e63fd";

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
