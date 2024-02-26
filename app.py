
from flask import render_template, request, redirect, url_for
import os
import csv
from openai import OpenAI
import json
import subprocess


from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'json', 'csv'}
IMAGES_DIR = "/Users/timzav/Desktop/prak/static/images"
json_f_path = 'uploads/output.json'


@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/test')
def test():
    return render_template('test.html')

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

    
        dir_path = "/Users/timzav/Desktop/prak/static/images"   # Directory containing the images
        img_filenames = []                  # List to store image filenames
        for _, __, fnames in os.walk(dir_path):
            for f in fnames:                # Iterate over every file found in the directory
                if f.lower().endswith(".jpg") or f.lower().endswith(".png"):      # Checking whether the file has .jpg/.png extension
                    img_filenames.append(f)         # Adding the valid image filenames to our list
        return render_template("upload.html", img_data=img_filenames)

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


if __name__ == '__main__':
    app.run()