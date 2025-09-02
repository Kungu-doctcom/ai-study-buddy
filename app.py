import os
from flask import Flask, render_template, request, session, redirect, url_for
from openai import OpenAI

# Initialize Flask
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "supersecret")  # required for sessions

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

DEFAULT_QUESTION = "What is photosynthesis?"


def get_ai_answer(question):
    """Helper function to call OpenAI and return an answer."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful study assistant."},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content


@app.route("/", methods=["GET", "POST"])
def index():
    history = session.get("history", [])
    answer = None
    question = None
    expand_history = False
    latest_index = None  # track latest Q&A index

    if request.method == "POST":
        # Clear history
        if "clear_history" in request.form:
            session.pop("history", None)
            return redirect(url_for("index"))

        # Otherwise, process a question
        question = request.form.get("question")
        if not question:
            question = DEFAULT_QUESTION

        answer = get_ai_answer(question)

        # Save Q&A in session history
        history.append({"q": question, "a": answer})
        session["history"] = history

        expand_history = True  # auto-expand history after new question
        latest_index = len(history) - 1  # highlight latest

    # On first visit, set default Q&A if no history exists
    if not history:
        question = DEFAULT_QUESTION
        answer = get_ai_answer(question)
        history.append({"q": question, "a": answer})
        session["history"] = history
        latest_index = len(history) - 1

    # If no new question was asked, show latest from history
    if not question and history:
        question = history[-1]["q"]
        answer = history[-1]["a"]
        latest_index = len(history) - 1

    return render_template(
        "index.html",
        question=question,
        answer=answer,
        history=history,
        expand_history=expand_history,
        latest_index=latest_index
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
