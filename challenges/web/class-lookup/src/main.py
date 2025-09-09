from flask import Flask, request, render_template
import subprocess, os

app = Flask(__name__, static_folder="style")

@app.route("/")
def index():
    if request.args.get("input"):
        try:
            process = "python3 ./classes.py " + request.args.get("input")
            fileStream = os.popen(process)
            output = fileStream.read()
        except Exception as e:
            output = e
    else:
        output = "Please enter a CS professor's last name"

    return render_template('index.html', value=output)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000, debug=True)