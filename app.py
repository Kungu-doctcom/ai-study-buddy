import os
from flask import Flask, request, render_template
from openai import OpenAI

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/", methods=["GET", "POST"])
def index():
    quiz = None
    error = None

    if request.method == "POST":
        topic = request.form.get("topic", "").strip()
        if topic:
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",  # fast & cheap
                    messages=[
                        {"role": "system", "content": "You are a helpful quiz generator."},
                        {"role": "user", "content": f"Generate 3 multiple-choice questions about {topic}. Include 4 options and mark the correct one."}
                    ],
                    max_tokens=500
                )
                quiz = response.choices[0].message.content
            except Exception as e:
                error = f"OpenAI API error: {e}"

    return render_template("index.html", quiz=quiz, error=error)
