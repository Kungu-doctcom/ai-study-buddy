from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

HF_API_KEY = os.getenv("HF_API_KEY")
API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-small"
headers = {"Authorization": f"Bearer {HF_API_KEY}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

@app.route("/", methods=["GET", "POST"])
def index():
    quiz = []
    if request.method == "POST":
        topic = request.form["topic"]
        prompt = f"Generate 3 simple quiz questions and answers about {topic} for students."
        output = query({"inputs": prompt})
        
        if isinstance(output, list) and "generated_text" in output[0]:
            quiz_text = output[0]["generated_text"].strip().split("\n")
            quiz = [q for q in quiz_text if q.strip()]
        else:
            quiz = ["Error: Could not generate quiz. Try again."]
    
    return render_template("index.html", quiz=quiz)

if __name__ == "__main__":
    app.run(debug=True)

