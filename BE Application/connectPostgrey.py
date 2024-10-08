from flask import Flask, request, jsonify
import psycopg2
from flask_cors import CORS  # Import CORS from flask_cors module
import base64
from email.message import EmailMessage
import smtplib
sender = "pradeepkumar.sf123@gmail.com"


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
CORS(app, resources={r"/forgotPassword": {"origins": "*"}})

connection = psycopg2.connect(
            dbname="Project",
            user="postgres",
            #password="your_password",
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

        query = "INSERT INTO login (username, password, firstname, middlename, lastname, age, gender, dob, mobileno, state, district, village, pincode,admin) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"
        cursor.execute(query, (username, password, firstname, middlename, lastname, age, gender, dob, mobileno, state, district, village, pincode,False))

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
# Add admin in query
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
    
  
# Function to check if username exists in the database
def username_exists(username):
    connection.commit()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM documents WHERE username = %s", (username,))
            count = cursor.fetchone()[0]
            return count > 0
        except Exception as e:
            print("Error checking if username exists:", e)
            return False
    else:
        return False
    
@app.route('/upload-document', methods=['POST'])
def upload_document():
   
    username = request.form.get('username')
    aadhar_number = request.form.get('aadhar_number')
    bank_acc_number = request.form.get('bank_acc_number')
    aadhar_document = request.files.get('aadhar_document')
    bank_document = request.files.get('bank_document')
    seven_twelve_document = request.files.get('seven_twelve_document')
    eight_a_document = request.files.get('eight_a_document')

    # Read file data
    aadhar_document_data = aadhar_document.read()
    bank_doc_data = bank_document.read()
    seven_twelve_doc_data = seven_twelve_document.read()
    eight_a_doc_data = eight_a_document.read()
   
    # Check if all required fields are present
    if not (aadhar_document and aadhar_number and bank_acc_number and username):
        return jsonify({'error': 'Missing required fields'}), 400

 # Check if username exists in the database
    if username_exists(username):
        # Update the record
        connection.commit()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("UPDATE documents SET aadhar_number = %s, bank_acc_number = %s, aadhar_document = %s, bank_passbook_doc = %s, seven_twelve_doc = %s, eight_a_doc = %s WHERE username = %s", 
                               (aadhar_number, bank_acc_number, aadhar_document_data, bank_doc_data, seven_twelve_doc_data, eight_a_doc_data, username))
                connection.commit()
                cursor.close()
                connection.close()
                return jsonify({'message': 'Record updated successfully'}), 200
            except Exception as e:
                print("Error updating record:", e)
                return jsonify({'error': 'Failed to update record'}), 500
        else:
            return jsonify({'error': 'Failed to connect to database'}), 500
    else:
        connection.commit()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("INSERT INTO documents (username, aadhar_number, aadhar_document, bank_acc_number, bank_passbook_doc, seven_twelve_doc, eight_a_doc) VALUES (%s, %s, %s, %s, %s, %s, %s)", (username, aadhar_number, aadhar_document_data, bank_acc_number, bank_doc_data, seven_twelve_doc_data, eight_a_doc_data))
                connection.commit()
                cursor.close()
                return jsonify({'message': 'File uploaded successfully'}), 200
            except Exception as e:
                print("Error inserting file into database:", e)
                return jsonify({'error': 'Failed to upload file'}), 500
        else:
            return jsonify({'error': 'Failed to connect to database'}), 500
        

# Endpoint for admin login
@app.route('/admin/login', methods=['POST'])
def admin_login():
    try:
         # Retrieve data from the request body
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        query =  query = "SELECT * FROM login WHERE username = %s AND password = %s AND admin = TRUE"
        cursor.execute(query, (username, password))
        rows = cursor.fetchall()

        if rows:
            return {'data': "Admin Logged In successfull"}, 200
        else: 
            return {'message': 'Incorrect username or password'}, 200
        
        connection.close()
        return {'data': rows}, 200
    except psycopg2.Error as e:
        return {'error': str(e)}, 500
    

    # Route to fetch user details and uploaded documents

import base64

@app.route('/admin/dashboard', methods=['GET'])
def admin_dashboard():
    try:
        cursor.execute("""
    SELECT 
        login.username, login.firstname, login.middlename, login.lastname, login.age, login.gender, login.dob, login.mobileno, 
        documents.aadhar_number, documents.bank_acc_number, 
        encode(documents.aadhar_document, 'base64') AS aadhar_document_base64, 
        encode(documents.bank_passbook_doc, 'base64') AS bank_passbook_doc_base64, 
        encode(documents.seven_twelve_doc, 'base64') AS seven_twelve_doc_base64, 
        encode(documents.eight_a_doc, 'base64') AS eight_a_doc_base64
    FROM 
        login
    LEFT JOIN 
        documents ON login.username = documents.username
""")
        rows = cursor.fetchall()


        # Fetch column names from cursor description
        column_names = [desc[0] for desc in cursor.description]

        # Convert rows to dictionaries with column names as keys
        data = []
        for row in rows:
            row_dict = {}
            for i in range(len(column_names)):
                if column_names[i].endswith('_base64'):
                    row_dict[column_names[i]] = row[i]
                else:
                    row_dict[column_names[i]] = row[i]
            data.append(row_dict)

        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/forgotPassword', methods=['GET'])
def forgotPassword():
    try:
         # Retrieve data from the request body
        username = request.args.get('username')
      

        query = "SELECT * FROM login WHERE username = %s"
        cursor.execute(query, (username,))
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
            
            fullname = data[0]['firstname'] + " " + data[0]['middlename'] + " " + data[0]['lastname']
            mailsender(sender, username, data[0]['password'], fullname)
            return jsonify({'status': 'success', 'message': 'Email sent successfully!'})
        else: 
            return {'message': 'Incorrect username '}, 200
        
        connection.close()
       
    except psycopg2.Error as e:
        return {'error': str(e)}, 500

def send_email(sender, recipient, subject, email_message):
    try:
        # Create the email message
        email = EmailMessage()
        email['Subject'] = subject
        email['From'] = sender
        email['To'] = recipient
        email.set_content(email_message)
        # Connect to the SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender, 'sccvujqvokutqfti')

            # Send the email
            server.send_message(email)

        # Return a success indicator
        return True
    except Exception as e:
        # Print or log the exception for debugging
        print(f"An error occurred: {e}")
        # Return a failure indicator
        return False

def mailsender(sender, username, password, fullname):
    try:
        subject = "Forgot password for Upscale Sugar Factory Solutions"

        email_message = f"""
                Dear {fullname},

                    We have received a request for forgot password so we have checked that you are a authorize user. We are sharing your current password - {password}.

                    If you did not request a password request, please ignore this email. If you haven't done it please reach out to paramvirpatil278@gmail.com.

                Thank you,
                Upscale Sugar Factory Solutions
                """

        # Send the email
        result = send_email(sender, username, subject, email_message)
        
        if result:
            # Return a success response
            return jsonify({'status': 'success', 'message': 'Email sent successfully!'})
        else:
            # Return a failure response
            return jsonify({'status': 'error', 'message': 'Failed to send email.'})

    except Exception as e:
        return {"error": f"An error occurred in api mailsender: {e}"}


#Billing Route
@app.route('/my-bill', methods=['GET'])
def fetch_my_bill():
    try:
        username = request.args.get('username')
        print("username", username)
        query = "SELECT * FROM bill WHERE username = %s"
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
    

@app.route('/enterBill', methods=['POST'])
def enterBill():
    try:
         # Retrieve data from the request body
        data = request.get_json()

        # Extract data from the validated request
        username = data.get('username')
      
        ton= data.get('ton')
        rate= data.get('rate')
        waste= data.get('waste')
        totalton= data.get('totalton')
        labourid= data.get('labourid')
        date= data.get('date')
        mobileno= data.get('mobileno')
       

        query = "INSERT INTO bill (username,  ton,  rate, waste, totalton, labourid, date, mobileno) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (username,ton,  rate, waste, totalton, labourid, date, mobileno))

        if cursor.rowcount > 0:
            connection.commit()
            return {'data': "User Bill Entery successfull"}, 200
        else:
            print("We are facing issues while registration. Please try again")
        
        connection.close()
    except psycopg2.Error as e:
        return {'error': str(e)}, 500
    
if __name__ == '__main__':
    app.run(debug=True)
