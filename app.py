import ollama
for part in ollama.chat(model='mistral', messages=[{'role': 'user', 'content': 'Write me a Haiku about your favorite programming language'}], stream=True):
        print(part['message']['content'], end='', flush=True)
