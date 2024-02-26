from app import app
from flask import render_template, request, redirect, url_for
import os
import json
import csv
from openai import OpenAI
import json
import re
import subprocess
import sys
import glob
import time
import subprocess
import tiktoken


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'json', 'csv'}
json_f_path = 'uploads/output.json'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(UPLOAD_FOLDER, filename))

        csv_to_json(f'{os.path.join(UPLOAD_FOLDER, filename)}', f'{json_f_path}')

        first_two_rows_json = get_first_two_rows(json_f_path)

        text1 = request.form['text1']
        text2 = request.form['text2']
        os.environ['DESCRIPTION'] = text1
        os.environ['TASK'] = text2
        os.environ['JSONFPATH'] = json_f_path
        os.environ['DATABLOCKEXAMPLE'] = first_two_rows_json

        process = subprocess.Popen(['python', '/Users/timzav/Desktop/prak/print.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Wait for the process to finish
        stdout, stderr = process.communicate()

        # Check return code to see if the script ran successfully
        if process.returncode == 0:
            print("Script execution successful.")
        else:
            print("Script execution failed.")

        image_folder = '/Users/timzav/Desktop/prak/static/images'
    
        # Get a list of all files in the folder
        image_files = os.listdir(image_folder)
        
        # Filter out non-image files
        image_files = [file for file in image_files if file.endswith(('.jpg', '.png', '.gif', '.jpeg'))]
        
        # Render the HTML template and pass the image files to it
        return render_template('upload.html', image_files=image_files)
    return 'Invalid file'

# Convert CSV to JSON
def csv_to_json(csv_file, json_file):
    with open(csv_file, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        data = list(csvreader)
    with open(json_file, 'w') as jsonfile:
        json.dump(data, jsonfile, indent=4)

    # Read CSV file
    with open(csv_file, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        # Convert CSV data to HTML table
        html_table = "<table>"
        for row in csvreader:
            html_table += "<tr>"
            for col in row:
                html_table += "<td>{}</td>".format(col)
            html_table += "</tr>"
        html_table += "</table>"
    return html_table

# first two rows of a JSON file
def get_first_two_rows(json_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)
        # Assuming data is a list of dictionaries
        first_two_rows = data[:2]
        return json.dumps(first_two_rows, indent=4) 

#ostale funkcije
with open('/Users/timzav/Desktop/DataWizard/config.json') as f:
    config = json.load(f)
    kljuc = config['API_KEY']
    client = OpenAI(api_key=kljuc)

#file names list
def files_list(folder_path):
    file_names = []
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            if os.path.isfile(os.path.join(folder_path, filename)):
                file_names.append(filename)
    return file_names

folder_path = '/images/'

