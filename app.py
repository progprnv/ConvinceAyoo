from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Placeholder function for connecting to Ollama API
def get_opposing_reasons(user_query):
    # Sample payload to send to Ollama (replace with actual API structure)
    payload = {
        "model": "convince_ayo_model",
        "input": user_query
    }
    # Simulating Ollama API call
    url = "https://api.ollama.ai/generate"
    headers = {"Authorization": "Bearer YOUR_OLLAMA_API_KEY"}

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        # Extracting the response text from Ollama
        result = response.json().get("choices")[0].get("text", "Could not generate response.")
        return result
    except Exception as e:
        return str(e)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Retrieve the user query from the form
        user_query = request.form.get("query")
        if user_query:
            # Get opposing arguments from Ollama
            opposing_reasons = get_opposing_reasons(user_query)
            return render_template("index.html", opposing_reasons=opposing_reasons)
        else:
            return render_template("index.html", error="Please enter a valid query.")
    return render_template("index.html")

if _name_ == "_main_":
    app.run(debug=True)
