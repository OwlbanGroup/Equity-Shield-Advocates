from flask import Flask, jsonify
import json

app = Flask(__name__)

def load_corporate_structure():
    with open('corporate_structure.json', 'r') as f:
        data = json.load(f)
    return data

@app.route('/api/corporate-structure', methods=['GET'])
def get_corporate_structure():
    data = load_corporate_structure()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
