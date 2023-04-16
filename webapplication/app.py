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

imageurl = "https://clo835-finalproject-2023.s3.us-east-1.amazonaws.com/ilovedogs.jpg?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEDIaCXVzLWVhc3QtMiJHMEUCIHKJqaBFd8sRGaiiGxHPhP%2FsXbupjsA8s4A%2F13vwL9xIAiEAjqMbR8ISjzPo3YAmcKe7JSecNtB6rjE5DRYn%2ByikXYsq9AIILBAAGgw3NDA1ODA4OTQ1NDAiDNtnT1fRrPPqLZ7TIirRAjgFDpu%2FMd1%2FIcqCJ26XSzoC98urNLnpgqYay3Ldd0Refn9pq892JEiXM%2FHPQaxm%2FtjE30DxYJGg2tWjphRr1KZMZqNkKXUcpj7T91ZUOzduziRNe9G8yAWwPHXJoALlUMjayf0Mlkrj7BYwEkhDGpmEr1d8NMwfFFxbqEKqgxeebO%2BQmu%2BrCcuR4EC%2BQcPsfMQ1bwAL4yHPRaiXlBDGneUGWO5k7wACX2lyLc9x2spVStXdv0Mfh7kEbvw6JUszcOBzdteTblyjdhl%2F%2FXkLmmEygUyRSXiQ%2FmGQ%2FZxF15CUzH2%2Bt4%2Boq7qD7DGtK1s2Cvk9OHMwSdU%2FQMrmriIUiGnNs2qICayQvnOvRagZKi%2FbFIiCTMR0ZnxnyqmFcVvGup2JozUSdEpd5vo1IhdJ1we3peffPPAnm3Rm%2BKyfhrZRfnERFJ%2BGCQun4v%2BeNlLWUr0wg5vvoQY6hwJgzhlrm97PjJlwNy6FmF0djVDkyDMeBsAijErArDmvK0FZ1eaHzXdObtyWkn54iDcuAN9rw8lAogNlZyLvPEm5bAVdqje%2BqACKBItShkwZ00w4hL6tpmlTej4S8bGArQvrnzCBlDDXB7GBhvrfDBL6zUcUvT11G2%2BkoJP3N%2FywJLIuc8xEqWvhuKqQyc9F09yQk4JEtMJmpcbwcfGd9BFN1zGcD7Qn2DiSH%2BtZaR7UwYSkMf3GzqZlNqDlZRh%2BBpRn89FOHlfQjlLSauLPByENvyF%2BET3Ql2tbXMntT6e80VB99pqB3RiNMCjYrEizqgdZmez9KPqIKmYAnXuvvmKzgvlXKJMWrg%3D%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20230416T133033Z&X-Amz-SignedHeaders=host&X-Amz-Expires=43200&X-Amz-Credential=ASIA2Y3QPU5GK3G6BNHD%2F20230416%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=e759ec0eed4767e3a09d56e881e66c44bbd6fe959ac7b7970fad35b29070b7c3";

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
