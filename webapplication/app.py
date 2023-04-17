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

imageurl = "https://clo835-finalproject-winterr2023.s3.us-east-1.amazonaws.com/ilovedogs.jpeg?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEFEaCXVzLWVhc3QtMiJHMEUCIEN5srvQ2d2FCMjD9yQeP6%2BdcKOZlcYDQ53q9HAuLmftAiEA0flSRlY4et4WgaDcpuwbm4k6yB15858ILbNgBCbkucMq7gIIShAAGgw3MTgyMjc5NjExNjYiDK8XGXNGyhln8mzskSrLAn7FSmHik3OXzRCAFLCILXHRSaRsc3E5KSsrTvpq3WKRmR4NPsi9f5MIE2%2FOPkwCClIGZZmwn%2FUJoOu1TsFChjIPLN%2F54pV5BOwV2TCMD4ACAmNOrQ5TR9SQ5btWWEKvc3nAfBtkIrQZlXzW7s5gMHOeRU%2BZfpsez8bwpAA1oKQ93bPGp1E2A4PdLo0loOf8c8h%2BlI8swDcmrkuTfSXudzs9nnP8G2rap8A6PuHrm42MvnL9jaIihTOI4i5EFc3JhTsKv6qWVsiuJetOSHUGEIemrLcgarL16wPaPQxEXF1mB1mzrZ%2Bl0negy0h2jrjdaFrPuClyqnWwqNqLQ99OZWHKqybPIycRbynOhlRo68CbMhqD2iJ4XEXPVDJaU5NBLy74SKq0v89Vkp%2FA%2BDTsiq32cvZ0bhDkcho5kFCOJksivxt6kYKJ3qYtRDgwifn1oQY6hwJR91i3mK5fX%2F6OC0%2BysdgxEveHAFDoTsCdJlVPXrDTR9291%2BdpM%2BKmgQ43ToCLRLQ4dkWqEatvzt5KNH5Kebjwe42ONVT9jXPj7yWKJuA6n%2BD9zND1Fd8jZvm3GYqg0PIW7pt7IBKryLzmlCMVSqO2O%2FbobNtsL0z9GbP1wvWG7WKnSeb9kx1sH38VUQM53vEcUL9uAo0YowO2WE3ysBxz09fpsoHqe2loCL6%2Bjy0%2BUDPn3harIeW%2B5Db%2BWPz%2BaE2jU2gUjnurj%2FNcIIlqrzS0CHElOrjrPrbBXqivQ7SpMwVjarAS8YYdR6s6CkpuR3yQI44bWjnqbVCIldhj4qJqML9c3HeMKw%3D%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20230417T172018Z&X-Amz-SignedHeaders=host&X-Amz-Expires=43200&X-Amz-Credential=ASIA2OONY6VHPF746HD2%2F20230417%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=ee618a1b220fa96ae61d523258a8fdb587f5e311190852b0c838e8745d28c9b0";

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
