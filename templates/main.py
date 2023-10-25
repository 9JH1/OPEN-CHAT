
from flask import Flask, jsonify, request
import firebase_admin
from firebase_admin import credentials, db
import datetime
import flask_cors
import json, os, signal
import socket
import webbrowser
import flask
import hashlib
import getpass
import subprocess
from multiprocessing import Process
import re

hostname=socket.gethostname()
IPAddr=socket.gethostbyname(hostname)
app = Flask(__name__)

def encrypt_string(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature

CORS = flask_cors.CORS(app)
creds_json = {
}

key_enc = f'{encrypt_string(IPAddr)}{encrypt_string(hostname)}'
# Initialize Firebase Admin SDK with your credentials
cred = credentials.Certificate(creds_json)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://nz-mafia-9682d-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

# Define a route to return the contents of /general
@app.route(f'/{key_enc}/general', methods=['GET'])
def get_general_data():
    try:
        # Get a reference to the /general node in your Firebase Realtime Database
        ref = db.reference('/general')

        # Fetch the data from Firebase
        data = ref.get()

        return jsonify(data)
    except Exception as e:
        return str(e), 500

def get_current_user_email():
    try:
        # Run the systeminfo command and capture its output
        systeminfo_output = subprocess.check_output(['systeminfo'], stderr=subprocess.STDOUT, text=True)

        # Use regular expressions to search for an email address pattern
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        matches = re.findall(email_pattern, systeminfo_output)

        # If matches were found, return the first one
        if matches:
            return matches[0]
        else:
            return "Email not found in systeminfo."

    except subprocess.CalledProcessError as e:
        return f"Error running systeminfo: {e}"
email_addr = get_current_user_email()


@app.route("/pr1v4t3")
def u_got_me():
    return  str(key_enc)



@app.route(f'/stopServer', methods=['GET'])
def stopServer():
    os.kill(os.getpid(), signal.SIGINT)
    return jsonify({ "success": True, "message": "Server is shutting down..." })





@app.route(f'/{key_enc}/socket')
def return_username(): 
    return str(socket.gethostbyname(socket.gethostname()))

@app.route(f"/{key_enc}/network")
def get_current_wifi_network():
    try:
        result = subprocess.check_output(["netsh", "wlan", "show", "interfaces"])
        result = result.decode("utf-8")
        lines = result.split('\n')
        for line in lines:
            if "SSID" in line:
                return line.split(":")[1].strip()
        return "404"
    except subprocess.CalledProcessError:
        return "404"

@app.route(f"/{key_enc}/send/<message>")
def log_message_to_general(message):
    if message == '': return 'message has to be !null'
    # Get the current date and time
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    print(current_datetime)
    # Get the current logged-in user for Windows
    current_user = getpass.getuser()
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(socket.gethostname())

    try:
        # Get a reference to the /general node in your Firebase Realtime Database
        ref = db.reference('/general')

        # Create a dictionary with the log entry
        log_entry = {
            'date': current_datetime,
            'user': current_user,
            'message': message,
            'ip': ip_address, 
            'hostname': hostname,
            'email': email_addr
        }

        # Push the log entry to Firebase under a new unique key
        ref.push(log_entry)

        print("Message logged to /general successfully.")
        return "Message logged to /general successfully."
    except Exception as e:
        print(f"Error: {str(e)}")
        return f"Error: {str(e)}", 500
@app.route(f"/{key_enc}/TOS_COC")
def load_tos_coc():
    return flask.render_template_string("""
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Open-Chat Terms and Conditions</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400&display=swap');

        body {
            background-color: black;
            width: 100vw;
            margin: 0;
            padding: 0;
            font-family: 'Roboto', sans-serif;
            font-weight: 500;
        }

        .til {
            width: 100%;
            height: 80px;
            color: white;
            font-size: 30px;
            display: flex;
            justify-content: center;
            align-items: center;
            font-weight: 700;
        }

        .par {
            width: 100%;
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            background-color: rgb(7, 7, 7);
            margin-bottom: 20px;
            font-size: 11px;
        }

        .pag {
            width: 90%;
            overflow-wrap: break-word;
            color: white;
        }

        .tol {
            width: 90%;
            color: rgb(30, 30, 30);
        }
    </style>
</head>

<body>
    <div class="til">
        OPen-Chat Terms and Conditions
    </div>
    <div class="par">
        <div class="tol">General</div>
        <div class="pag">
            Welcome to Open-Chat, a fully encrypted chat room created for fostering open and free speech discussions
            among
            students of Rangiora High School. This platform is designed to encourage respectful and responsible
            communication.

            By using Open-chat, you agree to abide by the following terms and conditions:
        </div>
    </div>
    <div class="par">
        <div class="tol">Terms of Service</div>
        <div class="pag">
            1. **Respectful Communication**: We encourage free speech, but it must be respectful and considerate of
            others.
            Hate speech, discrimination, or harassment of any kind is strictly prohibited.

            2. **Privacy**: Your privacy is important to us. We use encryption to protect your messages and data.
            However,
            please be cautious and do not share personal information with strangers.

            3. **Content Moderation**: We may moderate content to ensure it aligns with our community standards.
            Inappropriate
            content will be removed.

            4. **Account Responsibility**: You are responsible for your account. Do not share your login information
            with others.

            5. **Reporting**: If you encounter inappropriate behavior or content, please report it to us immediately.

            6. **No Spam**: Spamming is not allowed. Do not flood the chat with repetitive messages or advertisements.

            7. **Legal Compliance**: Use Open-Chat in compliance with all applicable laws and regulations.

            Failure to adhere to these terms may result in the suspension or termination of your account.

            We are committed to providing a safe and inclusive environment for all students. Thank you for being a part
            of our community.
        </div>
    </div>
    <div class="par">
        <div class="tol">Code of Conduct</div>
        <div class="pag">
            Our Code of Conduct is essential for maintaining a positive and respectful community:
            1. **Respect Others**: Treat all members with kindness and respect.
            2. **No Hate Speech**: Hate speech or discriminatory behavior is not tolerated.
            3. **Privacy Matters**: Protect your personal information and respect others' privacy.
            4. **Report Violations**: Report any violations of these rules to the moderators.
            5. **Be Responsible**: Use the chat service responsibly and follow the law.
        </div>
    </div>
    <div class="par">
        <div class="tol">Summary</div>
        <div class="pag">
            In conclusion, Open-Chat promotes free speech within the boundaries of respectful and responsible
            communication.
            You can freely express your thoughts and ideas in the general chat while maintaining a respectful and
            considerate attitude towards others.
        </div>
    </div>
</body>

</html>
                                        """)

@app.route(f'/{key_enc}/open_tos')
def opner_tos():
    webbrowser.open('http://127.0.0.1:5000/TOS_COC')
    return 'opening'

@app.route(f"/{key_enc}/group_ip_list/<groupname>")
def return_group_ip(groupname):
    try:
        ref = db.reference(f"/groups/{groupname}/ips")
        ip_list = ref.get()
        if ip_list is None:
            ip_list = []  # Initialize an empty list if there are no IPs
        return str(ip_list)  # Convert the list to a string for response
    except Exception as e:
        print(f"Error: {str(e)}")
        return f"Error: {str(e)}", 500

@app.route(f"/{key_enc}/check_pass_group/<group>/<password>")
def return_group_pos_state(group, password): 
    try:
        # Get the group's password from Firebase
        group_password_ref = db.reference(f'/groups/{group}/password')
        group_password = group_password_ref.get()

        if group_password == encrypt_string(password):
            return "true"
        else:
            return "false"
    except Exception as e:
        print(f"Error: {str(e)}")
        return "false"  # Return "false" in case of an error

@app.route(f"/{key_enc}/alive")
def find_status():
    return "yes"

@app.route(f"/{key_enc}/groups_list")
def get_groups():
    groups_ref = db.reference('/groups')
    groups_data = groups_ref.get()
    
    group_info = {}
    
    if groups_data:
        for group_name, group_data in groups_data.items():
            group_info[group_name] = {
                "name": group_name,
                "password": group_data.get("password", ""),
                "ips": group_data.get("ips", []),
            }
    
    return  jsonify(group_info)

@app.route(f"/{key_enc}/message_get/<group_name>")
def get_group_messages(group_name):
    group_ref = db.reference(f'/groups/{group_name}/messages')
    messages = group_ref.get()
    
    return jsonify(messages)

@app.route(f"/{key_enc}/send_group/<message>/<group>/<password>")
def log_message_to_group(message, group, password):
    if message == '': return 'message has to be !null'
    try:
        # Get the current date and time
        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        
        # Get the current logged-in user for Windows
        current_user = getpass.getuser()
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(socket.gethostname())
        # Get a reference to the group's password in Firebase
        group_password_ref = db.reference(f'/groups/{group}/password')
        group_password = group_password_ref.get()
        
        # Check if the provided password matches the group's password
        if encrypt_string(password) != group_password:
            return "Incorrect password.", 401
        
        # Get a reference to the /groups/<group>/messages node in your Firebase Realtime Database
        ref = db.reference(f'/groups/{group}/messages')
        
        # Create a dictionary with the log entry
        log_entry = {
            'date': current_datetime,
            'user': current_user,
            'message': message,
            'ip': ip_address, 
            'hostname': hostname,
        }
        
        # Push the log entry to Firebase under a new unique key
        ref.push(log_entry)
        
        print("Message logged to /group successfully.")
        return "Message logged to /group successfully."
    except Exception as e:
        print(f"Error: {str(e)}")
        return f"Error: {str(e)}", 500

@app.route(f"/{key_enc}/start_group/<group_name>/<password>")
def create_group(group_name, password):
    groups_ref = db.reference('/groups')
    
    # Get the group data from Firebase
    group_data = groups_ref.get()

    # Check if group_data is None (no groups exist yet)
    if group_data is None:
        group_data = {}  # Initialize an empty dictionary
    
    # Check if the group already exists
    if group_name in group_data:
        return "Group already exists."
    
    # Create a new group with the provided password
    new_group_data = {
        "name": group_name,
        "password": encrypt_string(password),
        "messages": {}
    }
    
    groups_ref.child(group_name).set(new_group_data)
    return f"Group '{group_name}' created successfully."










if __name__ == '__main__':
    app.run()