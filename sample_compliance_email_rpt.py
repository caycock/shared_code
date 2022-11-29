import pymongo
import matplotlib.pyplot as plt
import sys
import os
from datetime import datetime
from datetime import datetime
import pyodbc
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from os.path import exists
import numpy as np
from cryptography.fernet import Fernet


#GLOBALS
node_path_array = []
my_date_array = []
my_comp_data_array = []
dateTimeObj = datetime.now()
timestampStr = dateTimeObj.strftime("%m-%d-%Y %H:%M")
datestampStr = dateTimeObj.strftime("%Y-%m-%d")
eng_datestampStr = dateTimeObj.strftime("%m-%d-%Y")
print("date:", datestampStr)
print("time/date:", timestampStr)
client = pymongo.MongoClient("mongodb://some_ip/")  
mydb = client["some"]
mycol = mydb["some"]


def get_comp_data_sql(sql_in):
    global my_date_array, my_comp_data_array
    server = 'tcp:some_server'
    database = 'some'
    username = 'some'
    password = 'some'
    node_path = ""
    compliance_percent = ""
    date_of_compliance_check = ""
    cnxn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    cursor = cnxn.cursor()
    number_of_rows = cursor.execute(sql_in);
    result = cursor.fetchall()
    for row in result:
        node_path = row.node_path
        compliance_percent = row.compliance_percent
        date_of_compliance_check = str(row.date_of_compliance_check)
        print("node_path" + "---" + node_path )
        print("compliance_percent" + "---" + compliance_percent)
        print("date_of_compliance_check" + "---" + date_of_compliance_check)
        print("\n")
        my_date_array.append(date_of_compliance_check)
        my_comp_data_array.append(float(compliance_percent))


def cm_to_inch(value):
    return value/2.5


def create_graph_for_node_path(node_path_in):
    global my_date_array, my_comp_data_array
    my_date_array.clear()
    my_comp_data_array.clear()

    # At the top of create_graph_for_node_path
    mysql = "some"
    get_comp_data_sql(mysql)
    x = my_date_array
    y = my_comp_data_array
    labels = x
    men_means = y
    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, men_means, width, color='green')
    ax.set_ylim(0, 105)
    ax.set_ylabel('Compliance Percentage')
    ax.set_title(node_path_in )
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    file_exists = exists(node_path_in.replace("/", "_") + ".png")
    if file_exists:
        os.remove(node_path_in.replace("/", "_") + ".png")
    ax.figure.set_size_inches(cm_to_inch(15), cm_to_inch(9))
    ax.bar_label(rects1, padding=1)
    fig.tight_layout()
    ax.figure.savefig(node_path_in.replace("/", "_") + ".png")
 

def get_distinct_node_paths_sql():
    global node_path_array
    server = 'tcp:some'
    database = 'some'
    username = 'some'
    password = 'some'
    sql_in = "some"
    cnxn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    cursor = cnxn.cursor()
    number_of_rows = cursor.execute(sql_in);
    result = cursor.fetchall()
    for row in result:
        node_path = row.node_path
        print("node_path" + "---" + node_path )
        node_path_array.append(node_path)


def enter_table_data(node_path_in, compliance_percent, device_count, passes, warnings, errors):
    html = '<table class="GeneratedTable" width=800>' + \
    '<thead>' + \
    '<tr>' + \
    '<th bgcolor="#01b9ff">' + \
    node_path_in + \
    '</th>' + \
    '<th colspan="4"><img src="cid:' + node_path_in.replace("/", "_") + '" ></th>' + \
    '</tr>' + \
    '</thead>' + \
    '<tbody>' + \
    '<tr>' + \
    '<td><b><u><center>Compliance Percentage</center><b><u></td>' + \
    '<td><b><u><center>Device Count</center><b><u></td>' + \
    '<td><b><u><center>Passes</center><b><u></td>' + \
    '<td><b><u><center>Warnings</center><b><u></td>' + \
    '<td><b><u><center>Errors</center><b><u></td>' + \
    '</tr>' + \
    '<tr>' + \
    '<td><center>' + compliance_percent + '</center></td>' + \
    '<td><center>' + device_count + '</center></td>' + \
    '<td><center>' + passes + '</center></td>' + \
    '<td><center>' + warnings + '</center></td>' + \
    '<td><center>' + errors + '</center></td>' + \
    '</tr>' + \
    '</tbody>' + \
    '</table>'
    return html


def gen_compliance_email(html_in):
    global node_path_array
    # Define these once; use them twice!
    strFrom = 'some'
    strTo = 'some'

    # Create the root message and fill in the from, to, and subject headers
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = 'Device Compliance Report - ' + eng_datestampStr
    msgRoot['From'] = strFrom
    msgRoot['To'] = strTo
    msgRoot.preamble = 'This is a multi-part message in MIME format.'

    # Encapsulate the plain and HTML versions of the message body in an
    # 'alternative' part, so message agents can decide which they want to display.
    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    msgText = MIMEText('This is the alternative plain text message.')
    msgAlternative.attach(msgText)

    # Reference the image in the IMG SRC attribute by the ID we give it below
    html_text = '<style>' + \
                'table.GeneratedTable {' + \
                'width: width=1050;' + \
                'background-color: #ffffff;' + \
                'border-collapse: collapse;' + \
                'border-width: 2px;' + \
                'border-color: #0a0a0a;' + \
                'border-style: solid;' + \
                'color: #000000;' + \
                '}' + \
                'table.GeneratedTable td, table.GeneratedTable th {' + \
                'border-width: 2px;' + \
                'border-color: #0a0a0a;' + \
                'border-style: solid;' + \
                'padding: 3px;' + \
                '}' + \
                'table.GeneratedTable thead {' + \
                'background-color: #FFFFFF;' + \
                '}' + \
                '</style> ' + \
                html_in
    msgText = MIMEText(html_text, 'html')
    msgAlternative.attach(msgText)

    for x in node_path_array:
        print("some nodes:" + x)
        file_exists = exists(x.replace("/", "_") + ".png")
        if file_exists:
            # This example assumes the image is in the current directory
            fp = open(x.replace("/", "_") + ".png", 'rb')
            msgImage = MIMEImage(fp.read())
            fp.close()

            # Define the image's ID as referenced above
            msgImage.add_header('Content-ID', '<' + x.replace("/", "_") + '>')
            msgRoot.attach(msgImage)

    print("Sending Email....")
    # Send the email (this example assumes SMTP authentication is required)
    import smtplib
    smtp = smtplib.SMTP()
    strFrom = "some"
    strTo = "some"

    connection = smtplib.SMTP(host='some', port=some)
    connection.starttls()
    connection.login("some", decrypt_string("some"))
    connection.send_message(msgRoot)
    connection.quit()


def execute_sql_string(sql_in):
    server = 'tcp:some'
    database = 'some'
    username = 'some'
    password = 'some'
    ret_device_group_id = ""
    cnxn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    cursor = cnxn.cursor()
    cursor.execute(sql_in)
    cnxn.commit()


def remove_todays_data():
    sql_stmt = "delete from some " + \
                "where FORMAT (date_of_compliance_check, 'dd-MM-yy') = FORMAT (CURRENT_TIMESTAMP, 'dd-MM-yy')"
    execute_sql_string(sql_stmt)


def get_key():
    file = open('some.txt', 'rb')
    key = file.read()  # The key will be type bytes
    file.close()
    return key


def decrypt_string(string_in):
    key_in = get_key()
    encoded = string_in.encode()
    f = Fernet(key_in)
    decrypted = f.decrypt(encoded)
    cln_encrypted = str(decrypted)[2:-1]
    return cln_encrypted


def calc_compliance(cursor_in, node_path_in, date_of_compliance_check):
    init_sql_stmt = "insert into some " + \
                    "some"
    sql2 = ""
    all_sql = ""
    passes = 0
    warnings = 0
    errors = 0
    compliance_percent1 = 0
    compliance_percent2 = 0
    device_count = 0
    tst_pass = 0
    device_name_list = []
    bad_device_count = 0
    for doc in cursor_in:
        tst_pass = doc["totals"]["passes"]
        if tst_pass > 0:
            device_name = doc["deviceName"]
            exist_count = device_name_list.count(device_name)
            if exist_count < 1:
                device_count = device_count + 1
                device_name_list.append(device_name)
                errors = errors + doc["totals"]["errors"]
                warnings = warnings + doc["totals"]["warnings"]
                passes = passes + doc["totals"]["passes"]
                compliance_percent1 = (((passes) / (errors + warnings + passes)))
        else:
            bad_device_count = bad_device_count + 1
    print("\nnodepath:", nodepath)
    print("errors:", errors)
    print("warnings:", warnings)
    print("passes:", passes)
    print("device_count:", device_count)
    print("BAD_device_count:", bad_device_count)
    compliance_percent2 = str(round(compliance_percent1 * 100, 2))
    print("compliance_percentage2:", compliance_percent2)
    sql2 = "'" + node_path_in + "', " + \
           "'" + str(errors) + "', " + \
           "'" + str(warnings) + "', " + \
           "'" + str(passes) + "', " + \
           "'" + str(device_count) + "', " + \
           "'" + str(compliance_percent2) + "', " + \
           "'" + date_of_compliance_check + "', " + \
           "CURRENT_TIMESTAMP)"
    all_sql = init_sql_stmt + sql2
    print("sql stmt:" + all_sql)
    execute_sql_string(all_sql)
    ret_html = enter_table_data(node_path_in, str(compliance_percent2), str(device_count), str(passes), str(warnings), str(errors))
    return ret_html


#**** MAIN ****
remove_todays_data()
start = datetime.fromisoformat(datestampStr)
device_groups_to_calculate = ["some", "some", "some",
                              "some", "some", "some", "some",
                              "some", "some", "some"]

entire_html = ""
for x in device_groups_to_calculate:
    device_group = x.split("_", 1)
    nodepath = device_group[0]
    myquery = {"nodePath": nodepath, "timestamp": {"$gt": start}}
    fields = {"deviceName": 1, "totals": 1, "timestamp": 1}
    mydoc = mycol.find(myquery, fields)
    inc_counter = 0
    spacer = '<br><br><br>'
    entire_html = entire_html + spacer + calc_compliance(mydoc, nodepath, timestampStr)
    create_graph_for_node_path(nodepath)

get_distinct_node_paths_sql()

for x in node_path_array:
    print("nodes:" + x)

# Generate Email
gen_compliance_email(entire_html)