from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import traceback  # Added for detailed error logging

app = Flask(__name__)
CORS(app)

# Groq AI API Configuration
GROQ_API_URL = "https://console.groq.com/keys"
GROQ_API_KEY = ""  # Replace with your actual Groq API key

headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

@app.errorhandler(Exception)
def handle_exception(e):
    traceback.print_exc()  # This prints the full error traceback in the terminal
    return jsonify({"error": str(e)}), 500

@app.route('/api/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get('question', '')

    if not question:
        return jsonify({"error": "Question is required"}), 400

    try:
        # Debugging: Print incoming data
        print("Received Data:", data)

        # Call Groq AI API
        response = requests.post(
            GROQ_API_URL,
            headers=headers,
           json={
    "model": "llama3-8b-8192",  # Use a valid model name
    "messages": [{"role": "user", "content": question}]
}
        )

        # Debugging: Print API response
        print("API Response:", response.status_code, response.text)

        if response.status_code != 200:
            return jsonify({"error": "Failed to get response from AI model"}), 500

        # Extract AI response
        ai_response = response.json().get("choices", [{}])[0].get("message", {}).get("content", "No response")
        return jsonify({"response": ai_response})

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "An error occurred while processing your request"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
