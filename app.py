from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import traceback  # For detailed error logging

app = Flask(__name__)
CORS(app)

# 🔴 Hardcoded Groq AI API Key (Replace with your actual key)
GROQ_API_KEY = ""  # Your Actual API Key
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"  # Correct API endpoint

# Headers for API request
headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

@app.errorhandler(Exception)
def handle_exception(e):
    """Global error handler"""
    traceback.print_exc()  # Print error details in the console
    return jsonify({"error": str(e)}), 500

@app.route('/api/ask', methods=['POST'])
def ask():
    """Handles AI query requests"""
    data = request.get_json()

    if not data or "question" not in data:
        return jsonify({"error": "Question is required"}), 400

    question = data["question"]

    try:
        # Debugging: Print incoming request
        print(f"Received Question: {question}")

        # Call Groq AI API
        payload = {
            "model": "llama3-8b-8192",  # Ensure this is a valid model
            "messages": [{"role": "user", "content": question}]
        }
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)

        # Debugging: Print API response
        print(f"API Response [{response.status_code}]: {response.text}")

        if response.status_code != 200:
            return jsonify({"error": "Failed to get response from AI model"}), 500

        # Extract AI response
        response_json = response.json()
        ai_response = response_json.get("choices", [{}])[0].get("message", {}).get("content", "No response")

        return jsonify({"response": ai_response})

    except requests.exceptions.RequestException as req_err:
        print(f"Request Error: {str(req_err)}")
        return jsonify({"error": "Failed to connect to AI API"}), 500
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "An error occurred while processing your request"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
