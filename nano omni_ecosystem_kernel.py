import os
from flask import Flask, request, render_template_string
from google import genai

app = Flask(__name__)

# Initialize the client (ensure your GEMINI_API_KEY environment variable is set)
client = genai.Client()

HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
    <title>Omni Ecosystem Kernel</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: sans-serif; margin: 20px; background: #121212; color: #e0e0e0; }
        textarea { width: 100%; height: 100px; background: #1e1e1e; color: #fff; border: 1px solid #444; padding: 10px; }
        input[type=submit] { background: #007acc; color: white; border: none; padding: 10px 20px; margin-top: 10px; cursor: pointer; }
        .response { margin-top: 20px; background: #1e1e1e; padding: 15px; border-left: 4px solid #007acc; white-space: pre-wrap; }
    </style>
</head>
<body>
    <h2>Omni Ecosystem AI Kernel</h2>
    <form method="POST">
        <textarea name="prompt" placeholder="Enter prompt...">{{ prompt }}</textarea><br>
        <input type="submit" value="Send to Gemini">
    </form>
    {% if response %}
        <div class="response"><strong>Response:</strong><br>{{ response }}</div>
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    response_text = ""
    prompt = ""
    if request.method == 'POST':
        prompt = request.form.get('prompt')
        if prompt:
            try:
                # Call the Gemini API using the modern google-genai SDK
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                )
                response_text = response.text
            except Exception as e:
                response_text = f"Error: {e}"
    return render_template_string(HTML_TEMPLATE, prompt=prompt, response=response_text)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
