from flask import Flask, render_template, request
import webbrowser

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("browser.html")

@app.route("/navigate", methods=["POST"])
def navigate():
    url = request.form.get("url")
    if not url.startswith(("http://", "https://")):
        url = f"https://{url}"
    webbrowser.open(url)  # Opens in user's default browser
    return {"status": "success", "url": url}

if __name__ == "__main__":
    app.run(debug=True)
