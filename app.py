from flask import Flask, render_template, request 
import requests

app = Flask("ConvinceAyoo")

# Function to connect to the Gemini API
def get_opposing_reasons(user_query):
    # Sample payload to send to Gemini API
    payload = {
        "input": user_query,
        "parameters": {  # Adjust parameters based on Gemini API requirements
            "model": "gemini_model",  # Replace with your actual model name
            "max_tokens": 150  # Example parameter; adjust as needed
        }
    }
    
    # Gemini API URL (replace with the correct endpoint)
    url = "https://api.yourgeminiendpoint.com/v1/generate"  # Ensure this matches the Gemini API URL

    headers = {
        "Authorization": "Bearer AIzaSyDpujbyrAZ1I_hniPtJNZwnMClGSjfLj-A",  # Your Gemini API key
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
        
        # Extracting the response text from Gemini
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
            # Get opposing arguments from Gemini
            opposing_reasons = get_opposing_reasons(user_query)
            return render_template("index.html", opposing_reasons=opposing_reasons)
        else:
            return render_template("index.html", error="Please enter a valid query.")
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
