from flask import Flask, render_template, request 
import requests

app = Flask("ConvinceAyoo")

# Function to connect to the Ollama API
def get_opposing_reasons(user_query):
    # Sample payload to send to Ollama
    payload = {
        "model": "convince_ayo_model",  # Replace with your actual model name
        "input": user_query
    }
    
    # Ollama API URL
    url = "http://127.0.0.1:11434/generate"  # Ensure this matches the server URL

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise an error for bad responses
        
        # Extracting the response text from Ollama
        result = response.json().get("choices")[0].get("text", "Could not generate response.")
        return result
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

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

if __name__ == "__main__":
    app.run(debug=True)
