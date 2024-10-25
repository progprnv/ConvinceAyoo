from flask import Flask, render_template, request
import google.generativeai as genai

# Initialize the Flask application
app = Flask("ConvinceAyoo")

# Configure the Gemini API with your API key
genai.configure(api_key="AIzaSyDpujbyrAZ1I_hniPtJNZwnMClGSjfLj-A")
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to connect to the Gemini API
def get_opposing_reasons(user_query):
    try:
        # Generate content using the Gemini model
        response = model.generate_content(user_query)
        return response.text  # Return the generated response text
    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Retrieve the user query from the form
        user_query = request.form.get("query")
        if user_query:
            # Get opposing arguments from the Gemini API
            opposing_reasons = get_opposing_reasons(user_query)
            return render_template("index.html", opposing_reasons=opposing_reasons)
        else:
            return render_template("index.html", error="Please enter a valid query.")
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
