from flask import Flask, request
import psycopg2
from flask_cors import CORS  # Import CORS from flask_cors module


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

connection = psycopg2.connect(
            dbname="Project",
            user="postgres",
            # password="your_password",
            host="localhost",
            port="5432"
        )
cursor = connection.cursor()

@app.route('/login', methods=['POST'])
def login():
    try:
         # Retrieve data from the request body
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        query = "SELECT * FROM login WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        rows = cursor.fetchall()

        if rows:
            return {'data': "Logged In successfull"}, 200
        else: 
            return {'message': 'Incorrect username or password'}, 200
        
        connection.close()
        return {'data': rows}, 200
    except psycopg2.Error as e:
        return {'error': str(e)}, 500





@app.route('/register', methods=['POST'])
def register():
    try:
         # Retrieve data from the request body
        data = request.get_json()

        # Extract data from the validated request
        username = data.get('username')
        password = data.get('password')
        firstname= data.get('firstname')
        middlename= data.get('middleName')
        lastname= data.get('lastname')
        age= data.get('age')
        gender= data.get('gender')
        dob= data.get('DOB')
        mobileno= data.get('mobileNo')
        state= data.get('state')
        district= data.get('district')
        village= data.get('village')
        pincode= data.get('pinCode')

        query = "INSERT INTO login (username, password, firstname, middlename, lastname, age, gender, dob, mobileno, state, district, village, pincode) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (username, password, firstname, middlename, lastname, age, gender, dob, mobileno, state, district, village, pincode))

        if cursor.rowcount > 0:
            connection.commit()
            return {'data': "User registration successfull"}, 200
        else:
            print("We are facing issues while registration. Please try again")
        
        connection.close()
    except psycopg2.Error as e:
        return {'error': str(e)}, 500

@app.route('/my-profile', methods=['GET'])
def fetch_my_profile():
    try:
        username = request.args.get('username')
        print("username", username)
        query = "SELECT * FROM login WHERE username = %s"
        cursor.execute(query, (username, ))
        rows = cursor.fetchall()

        # Fetch column names from cursor description
        column_names = [desc[0] for desc in cursor.description]

        # Convert rows to dictionaries with column names as keys
        data = []
        for row in rows:
            row_dict = {}
            for i in range(len(column_names)):
                row_dict[column_names[i]] = row[i]
            data.append(row_dict)
        if data:
            return {'data': data}, 200
        else: 
            return {'message': 'No Data found'}, 200
        connection.close()
    except psycopg2.Error as e:
        return {'error': str(e)}, 500

@app.route('/edit-my-profile', methods=['POST'])
def editMyProfile():
    try:
         # Retrieve data from the request body
        data = request.get_json()
        username= data.get('username')

        firstname= data.get('firstname')
        middlename= data.get('middleName')
        lastname= data.get('lastname')
        age= data.get('age')
        gender= data.get('gender')
        dob= data.get('DOB')
        mobileno= data.get('mobileNo')
        state= data.get('state')
        district= data.get('district')
        village= data.get('village')
        pincode= data.get('pinCode')
        address= data.get('address')

        query =  "UPDATE login SET firstname = %s, middlename = %s, lastname = %s, age = %s, gender = %s, dob = %s, mobileno = %s, state = %s, district = %s, village = %s, pincode = %s, address = %s WHERE username = %s"
        cursor.execute(query, (firstname, middlename, lastname, age, gender, dob, mobileno, state, district, village, pincode, address, username))

        if cursor.rowcount > 0:
            connection.commit()
            return {'data': "User registration update successfull"}, 200
        else:
            print("We are facing issues while registration. Please try again")
        
        connection.close()
    except psycopg2.Error as e:
        return {'error': str(e)}, 500
    
  

if __name__ == '__main__':
    app.run(debug=True)
