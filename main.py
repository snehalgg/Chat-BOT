from flask import Flask, request, render_template, jsonify
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import time
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Load pre-trained model and tokenizer
model = GPT2LMHeadModel.from_pretrained('gpt2-medium')
tokenizer = GPT2Tokenizer.from_pretrained('gpt2-medium')

# Set the model to evaluation mode
model.eval()

# Placeholder for training data
training_data = []  # This is where you'll store your training data

def collect_data():
    global training_data
    # Send a request to Google
    response = requests.get('https://www.google.com/search?q=programming+languages')
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract relevant information from the page
    search_results = soup.find_all('h3', class_='LC20lb DKV0Md')
    new_data = [result.text for result in search_results]

    # Add new data to the training set
    training_data.extend(new_data)

    # Fine-tune the model with the new data
    # Replace this with your actual fine-tuning logic

def auto_update():
    while True:
        # Placeholder for auto-update logic
        collect_data()
        # Re-train the model with the updated data
        # Replace this with your actual retraining logic

        # Sleep for a defined interval (e.g., 24 hours)
        time.sleep(86400)  # 24 hours

# Start the auto-update process in a separate thread
import threading
auto_update_thread = threading.Thread(target=auto_update)
auto_update_thread.daemon = True
auto_update_thread.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get', methods=['GET'])
def get_response():
    user_message = request.args.get('msg')

    # Tokenize and generate response
    input_ids = tokenizer.encode(user_message, return_tensors='pt')
    with torch.no_grad():
        outputs = model.generate(input_ids, max_length=50, num_return_sequences=1)

    bot_response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(debug=True)
