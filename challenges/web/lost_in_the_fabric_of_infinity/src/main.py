from flask import Flask, Response, request, render_template, abort
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        if request.args.get("url"):
            try:
                page = request.args.get("url")
                message = open('/src/{}'.format(page)).read()
                    
                return render_template("messages.html", message=message)
            except Exception as e:
                return str(e)
        else:
            return render_template("index.html")
    else:
        return "Method not supported"


if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=8080)