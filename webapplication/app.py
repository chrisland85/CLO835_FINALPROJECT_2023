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

imageurl = "https://clo835-finalproject-group1buckett.s3.us-east-1.amazonaws.com/ilovecats.jpeg?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEGsaCXVzLWVhc3QtMiJIMEYCIQDdDg3w9rWNNywXyw5l5zHcqkBp%2BsIlsMil4g3w61ilKQIhAIb6Vom0bT%2Bimz8yXjEpgUuQG7IaKq2A5ZDWPwdfY49LKvcCCGQQABoMNDQ4ODcwNzIxMjMwIgwiivhWtB8q8BBf88oq1AL8AEcX6PIEA4hNpYyH1uZCY3aJmuhzCzuoKK71ryNBCs5uTzGqBmBJjezOuEht5HbZy1bp1ayRZ0mSeoRxnarLwtcMKTUCoqvUdXWRQQjFJbgixRdwo5Mp%2FnY0bNhKy4SwrzvNeYezHv%2Bvrg3BJcRejggVA9AUBfJ%2FHsbrhUxtFknK8zsTNgQCn91nQqufv04y26T4ILLhniqVG30XwKJQ7QZ%2F%2B0F8FnXrdpEK2tAH2yPB6%2F4YI8F57x%2BJYVmb89rYsn3qAOXWWNOZrGm7GkkXwFAmagUCCBx4q%2FeNs5UvQqCb%2FhzjTF1cjUdVRWIuKdVrX2uE8AojM4Aw%2F31JBlIuqVl8PhzAKj%2BekzPqnvRM0sY%2FUOm0Iv8foF2PAo0lX7%2BjvkZ%2FfExT4rmwgKZ8MisLJl0%2BuFm79aKENZAHyk6pzwxgb0%2FNWXnRTf6IEGxYk1R3WxzuMPLG%2B6EGOoYCgMK0CjBJ6KWDtLRK%2BbjXRquFqPSy96sr4W%2BuQ1opZurdC4pQ%2Bk6VPa8a4RT3CYgVKHYihuBG5fkP4lD9mw7Q1fvYBuOtVcdpj0pgUYe%2FgcNKKEDo0H2XiJvaLaH6hPcUYQqXqXYJvA9Y5z2CgQ4cMN2wTNUOm7%2B0EEJfrDon5ZRRMqejrGifJeOpJ8on29lBPsck3aoQhG8DZe2zrx30iUOuc%2FnqdoO%2BPtZZFt7F5WHQL3zNBQOIh7pN%2FlowEtP%2BuKb3%2Fsnm3cdNAZ6VsLfXlhwTm1pvwyJWnafIuKwOrxIzx1yLJaSoy2xYq3Bs%2FVp9%2FLK0QfW%2BdGZHyQE%2Bcj4CmKoogyblyw%3D%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20230418T210530Z&X-Amz-SignedHeaders=host&X-Amz-Expires=720&X-Amz-Credential=ASIAWRAWHU3HCCHQROU7%2F20230418%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=fb729d26550ed16207fbf9e0d06518ce454e81dd0eece53e2f6e98787b7b9404";

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
