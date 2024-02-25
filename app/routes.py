from app import app
from flask import render_template, request, redirect, url_for
import os
import json
import csv


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



        text1 = request.form['text1']
        text2 = request.form['text2']

        html_table = csv_to_html_table(f'{os.path.join(UPLOAD_FOLDER, filename)}')
        # Process the file and texts here
        return f'File "{filename}" uploaded successfully. Text 1: {text1}, Text 2: {text2}\n{html_table}'
    return 'Invalid file'


def csv_to_json(csv_file, json_file):
    with open(csv_file, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        data = list(csvreader)
    with open(json_file, 'w') as jsonfile:
        json.dump(data, jsonfile, indent=4)



def csv_to_html_table(csv_file):
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