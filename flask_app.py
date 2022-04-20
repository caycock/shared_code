# Code by Chris Aycock 
# For ADP purposes only



from flask import Flask, jsonify
import datetime
from datetime import datetime, timedelta
from flask import Flask, request, session, redirect, url_for, render_template, send_file



app = Flask(__name__)


@app.route('/')
def index():
    return 'You are at index()'

@app.route('/report')
def report():
    match = "0"
    searched_id = ""
    searched_object_name = ""
    searched_address = ""
    searched_email = ""
    searched_date = ""
    searched_owner = ""

    args = request.args
    addr = args['addr']
    mask = args['mask']

    file = open('inventory.csv', 'r')
    file_contents = [line.rstrip('\n') for line in file]
    file.close()
    
    for c in file_contents:
        split_lines = c.split(",")  
        id = str(split_lines[0])
        dev_name = str(split_lines[1])
        ip_address = str(split_lines[2])
        email = str(split_lines[3])
        date = str(split_lines[4])
        owner = str(split_lines[5])

        if addr == ip_address:
            #match
            match = "1"
            searched_id = id
            searched_object_name = dev_name
            searched_address = ip_address
            searched_email = email
            searched_date = date
            searched_owner = owner
            break
    
    if match == "0":
        #no match
        searched_id = ""
        searched_object_name = ""
        searched_address = ""
        searched_email = ""
        searched_date = ""
        searched_owner = ""
        return jsonify(id="",searched_object_name="",searched_address="",searched_email="",searched_date="",searched_owner="")
    else:
        return jsonify(id=searched_id,searched_object_name=searched_object_name,searched_address=ip_address,searched_email=email,searched_date=date,searched_owner=owner)

@app.route('/addresses')
def addresses():
    match = "0"
    searched_id = ""
    searched_object_name = ""
    searched_address = ""
    searched_email = ""
    searched_date = ""
    searched_owner = ""

    args = request.args
    addr = args['addr']
    mask = args['mask']

    file = open('inventory.csv', 'r')
    file_contents = [line.rstrip('\n') for line in file]
    file.close()
    
    for c in file_contents:
        split_lines = c.split(",")  
        id = str(split_lines[0])
        dev_name = str(split_lines[1])
        ip_address = str(split_lines[2])
        email = str(split_lines[3])
        date = str(split_lines[4])
        owner = str(split_lines[5])

        if addr == ip_address:
            #match
            match = "1"
            searched_id = id
            searched_object_name = dev_name
            searched_address = ip_address
            searched_email = email
            searched_date = date
            searched_owner = owner
            break
    
    if match == "0":
        #no match
        searched_id = ""
        searched_object_name = ""
        searched_address = ""
        searched_email = ""
        searched_date = ""
        searched_owner = ""
        return jsonify(id="",searched_object_name="",searched_address="",searched_email="",searched_date="",searched_owner="")
    else:
        return jsonify(id=searched_id,searched_object_name=searched_object_name,searched_address=ip_address,searched_email=email,searched_date=date,searched_owner=owner)





if __name__ == '__main__':
    app.secret = 'shhhh'
    app.permanent_session_lifetime = timedelta(minutes=15)
    app.run(host='0.0.0.0', port=6543, debug=True)


