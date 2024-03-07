from openai import OpenAI
import json
import re
import subprocess
import sys
import os
import glob
import time
#import tiktoken
from ollama import Client
import requests
import ollama
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import anthropic
from anthropic import Anthropic
#api
with open('/Users/timzav/Desktop/DataWizard/config.json') as f:
    config = json.load(f)
    kljuc = config['API_KEY']
    client = OpenAI(api_key=kljuc)

counter = 0#za napake stet, kasnej break


#file names list
def files_list(folder_path):
    file_names = []
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            if os.path.isfile(os.path.join(folder_path, filename)):
                file_names.append(filename)
    return file_names

p_file_Path = "/Users/timzav/Desktop/prak/tplot.py"

def skupek_imen():
    file_names_list = files_list(folder_path)#iz funkcije
    file_names_string = ' '.join(file_names_list)
    return file_names_string
description = os.environ.get('DESCRIPTION')
Task = os.environ.get('TASK')
JsonfPath = os.environ.get('JSONFPATH')
jsonString = os.environ.get('DATABLOCKEXAMPLE')
choice = os.environ.get('CHOICE')
graphic = os.environ.get('GRAPHIC')
st = os.environ.get('ST')

Hand = '''
Hand-drawn/Sketch: These charts mimic the appearance of hand-drawn illustrations, with imperfect lines, doodles, and handwritten labels. They have a playful and informal feel.
'''
Classic = '''
normal chart style.
'''
Modern = '''
Modern: Modern chart styles often feature sleek designs, minimalist layouts, and vibrant color palettes. They may incorporate gradients, shadows, and other contemporary design elements.
'''
Retro = '''
Retro/Vintage: Retro-style charts evoke a nostalgic aesthetic, often featuring faded colors, textured backgrounds, and retro typography. They may incorporate design elements reminiscent of a specific time period.
'''


inputs = f"EXAMPLE OF DATA FROM JSON FILE:'{jsonString}', DESCRIPTION:'{description}', JSON FILE PATH (file is HERE):'{JsonfPath}'"

if graphic == 'option1':
    style = Classic
elif graphic == 'option2':
    style = Modern
elif graphic == 'option3':
    style = Hand
elif graphic == 'option4':
    style = Retro


folder_path = '/Users/timzav/Desktop/prak/static/images'
context = f'''Respond with python code ONLY inside ```python ```, no comments/explanations. Write code that will create PNG image showing chart based on data and task provided. Here is some additional information to help you get started:
  {inputs}, COLLOR STYLE:[{style}], RESOLUTION of chart(png image) must be HD (very high resolution), adjusted to each chart ratio of image resolution, only requirement is good resolution and readability of whole chart.
  Code should save image(s) here '{folder_path}'.
  '''

Context = f'''
Based on this: {inputs} create python code that will generate png charts based on this task: {Task}. Code can find data in this file: {JsonfPath} and should save image(s) here: {folder_path}.
'''
if st == 'option2':
    context = f'''Your task is to create this chart:[{Task}] with this js library:"https://cdn.jsdelivr.net/npm/chart.js, to create chart here is structure of data so you understand your task better:{jsonString} and description of data:{description}'. Your response must only be pure js script (withouth additional explenation or any html). Chart will be shown with canvas that has 'odCharta' id.
    You need to fetch data from async function with /get_csv, like so: const response = await fetch('/get_csv');
            const data = await response.json();
            return data;'''


while True:
    if counter <= 4:
        if choice == 'option1':
            response = client.chat.completions.create(
                model="gpt-4-1106-preview", 
                messages=[
                    {"role": "system", "content": context},
                    {"role": "user", "content": Task}
                ]
            )
            response = response.choices[0].message.content
        elif choice == 'option2':
            client = Client(host='https://b410-35-187-243-128.ngrok-free.app')
            response = client.chat(model='mixtral', messages=[
              {
                'role': 'user',
                'content': f'{context}, \n Your task is to:{Task}, for this create simple code with simple library usage.',
              },
            ])
            response = response['message']['content']
        elif choice == 'option3':
            client = Client(host='https://adc3-34-125-246-255.ngrok-free.app')#vedno popravi link
            response = client.chat(model='sammcj/smaug:72b-q4_k_m', messages=[
              {
                'role': 'user',
                'content': f'{Context}',
              },
            ])
            response = response['message']['content']
        elif choice == 'option4':
            client = Anthropic(
            api_key='',
            )
            message = client.messages.create(
            max_tokens=1024,
            messages=[
            {
            "role": "user",
            "content": f"Context: {Context} Task: {Task}",
            }
            ],
            model="claude-3-opus-20240229",
            )
            response = message.content
            response_text = [block.text for block in response]

            response_text = ''.join(response_text)
            response = response_text

        if st == 'option2':
            match = re.search(r"```(?:\bjavascript\b)?(.*?)```", response, re.DOTALL)
            if match:
                code_snippet = match.group(1)
            else:
                raise ValueError(f"No JavaScript code found in the input string {response}")

            json_file_path = "/Users/timzav/Desktop/prak/static/js/chart.js"

            with open(json_file_path, "w") as js_file:
                js_file.write(code_snippet)
            break

        
        match = re.search(r"```(?:\bpython\b)?(.*?)```", response, re.DOTALL)

        #pattern in string? #0
        if match:
            r_code = match.group(1)
        else:
            raise ValueError(f"No python code found in the input string{response}")
        
        #zapis kode
        
        with open(p_file_Path, "w") as r_file:
            r_file.write(r_code)
        
        # Check za ERROR
        try:
            result = subprocess.run(['/Users/timzav/miniconda3/bin/python', p_file_Path], stderr=subprocess.PIPE, text=True)
            #r1
            if result.returncode != 0:
                e = str(result.stderr)
                task = f'''This code:'{response}, gave this error when run:\n {str(e)}. Rewrite whole code again to fix this error.'''
                counter = counter + 1 
            else:
                print(f"Python script executed successfully in {counter} attempt")
                break
            #R2  
        except subprocess.CalledProcessError as e:
            task = f'''This code:'{response}, gave this error when run:\n {str(e)}. Rewrite whole code again to fix this error.'''
            counter = counter + 1
            #R3
        except Exception as e:
            task = f'''This code:'{response}, gave this error when run:\n {str(e)}. Rewrite whole code again to fix this error.'''
            counter = counter + 1

    else:
        #zdej ko je fl ne pise vec ker je drugac laufana..mogu bi posilat nazaj appu napako - zaenkrat nepotrebno
        print(f"Attempts:'{counter}'. Gave up at 4rd. imena\n:{skupek_imen()}")
        break
     
#upload ciscenje-folder 
    #safety
'''
folder_path = '/Users/timzav/Desktop/prak/uploads'
if os.path.exists(folder_path):
    file_paths = glob.glob(os.path.join(folder_path, '*'))
    for file_path in file_paths:
        if os.path.isfile(file_path):
            os.remove(file_path)
#varnostno
#tplot ciscenje-datoteka

#code that delets all data from this file p_file_Path
with open(p_file_Path, "w") as r_file:
    r_file.write("")
    '''