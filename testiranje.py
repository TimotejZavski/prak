from ollama import Client


client = Client(host='https://b410-35-187-243-128.ngrok-free.app')
response = client.chat(model='mixtral', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
])

print(response['message']['content'])