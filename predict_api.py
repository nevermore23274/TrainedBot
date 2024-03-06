from flask import Flask, request, jsonify
import csv, os, nltk, json, torch
import torch.nn as nn
from flask_cors import CORS
from nltk.tokenize import word_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer

app = Flask(__name__)
CORS(app)

nltk.download('punkt', download_dir='/usr/src/app/nltk_data')
nltk.data.path.append('/usr/src/app/nltk_data')
feedback_file_path = '/usr/src/app/data/feedback_data.csv'

def initialize_feedback_file():
    if not os.path.exists(feedback_file_path):
        with open(feedback_file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['input_text', 'model_prediction', 'correct', 'user_correction'])

initialize_feedback_file()

@app.route('/feedback', methods=['POST'])
def feedback():
    feedback_data = request.json
    input_text = feedback_data.get('text', '')
    
    # Dummy model prediction for demonstration
    model_prediction = "Dummy model prediction based on: " + input_text

    user_correction = feedback_data.get('expected_response', '')

    with open(feedback_file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([input_text, model_prediction, 'False', user_correction])

    return jsonify({'status': 'success'})

# Define the RNNModel class
class RNNModel(nn.Module):
    def __init__(self, vocab_size, embedding_dim=64, hidden_dim=128, num_layers=2):
        super(RNNModel, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.rnn = nn.LSTM(embedding_dim, hidden_dim, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_dim, vocab_size)

    def forward(self, x):
        x = self.embedding(x)
        output, (hidden, cell) = self.rnn(x)
        logits = self.fc(output)
        return logits

# Load the configuration settings
with open('model/config.json', 'r') as f:
    config = json.load(f)

# Load the vocabulary
with open('model/vocab.json', 'r') as f:
    vocab = json.load(f)

with open('model/vocab_inv.json', 'r') as f:
    vocab_inv = json.load(f)

# Update the vocab_size in the config based on the loaded vocabulary
config['vocab_size'] = len(vocab) + 1  # Add 1 for the <UNK> token

# Instantiate the model with the configuration settings
model = RNNModel(vocab_size=len(vocab) + 1, 
                 embedding_dim=config['embedding_dim'], 
                 hidden_dim=config['hidden_dim'], 
                 num_layers=config['num_layers'])

# Load the model state dictionary
model.load_state_dict(torch.load('model/bot_rnn_model_state_dict.pth'))
model.eval()

# Define the tokenize and detokenize functions using NLTK
def tokenize(text):
    return word_tokenize(text)

def detokenize(tokens):
    return TreebankWordDetokenizer().detokenize(tokens)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    input_text = data['text']

    # Preprocess the input text
    tokens = tokenize(input_text)
    encoded_input = torch.tensor([vocab.get(token, vocab['<UNK>']) for token in tokens])

    # Feed the preprocessed input into the model
    with torch.no_grad():
        model_output = model(encoded_input.unsqueeze(0))

    # Convert the model's output to text
    output_tokens = [vocab_inv.get(str(idx), '<UNK>') for idx in model_output.argmax(dim=2).squeeze().tolist()]
    output_text = detokenize(output_tokens)

    return jsonify({'prediction': output_text})

if __name__ == '__main__':
    app.run(debug=True)
