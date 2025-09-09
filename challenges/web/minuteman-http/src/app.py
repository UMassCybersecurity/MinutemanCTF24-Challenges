from flask import Flask, render_template, request, send_from_directory
import os

app = Flask(__name__,
            static_url_path='/static', 
            static_folder='/app/public/')

FLAG = os.environ["FLAG"]

# idk why i wrote it this way but its funny so its staying
CHALLENGE_ARRAY = [
    {
        'chall': lambda req: True,
        'message': "Hello, I only communicate with POST requests. Try using Burpsuite or Devtools to edit your request."
    },
    {
        'chall': lambda req: req.method == "POST",
        'message': "Thank you, but could you authenticate your requests with a cookie... How about one named 'mascot' with the value 'sam_the_minuteman'."
    },
    {
        'chall': lambda req: 'mascot' in req.cookies,
        'message': "You sent the cookie with the name mascot but I expected the value 'sam_the_minuteman'"
    },
    {
        'chall': lambda req: req.cookies.get('mascot') == 'sam_the_minuteman',
        'message': "Thank you for the cookie, but could you send me a url parameter with the name 'number_one' and the value 'in_student_dining'."
    }, 
    {
        'chall': lambda req: 'number_one' in req.args,
        'message': "You sent the url parameter with the name 'number_one' but I expected the value 'in_student_dining'."
    },
    {
        'chall': lambda req: req.args.get('number_one') == 'in_student_dining',
        'message': "Thank you for the url parameter, but could you send me a JSON in the body of your post request with the key 'deservesFlag' and value true."
    },
    {
        'chall': lambda req: req.headers.get('Content-Type') == 'application/json',
        'message': "You added the correct header, but I don't see any data!"
    },
    {
        'chall': lambda req: req.data,
        'message': "I see that there is JSON data, but I need a JSON object with the key 'deservesFlag' and the value true."
    },
    {
        'chall': lambda req: 'deservesFlag' in req.json,
        'message': "Your message includes a JSON with the key 'deservesFlag', however its value should be equal to the true boolean." 
    },
    {
        'chall': lambda req: req.json['deservesFlag'] == True,
        'message': f"I think you deserve the flag now... Here you go {FLAG}"
    }
]

@app.route("/", methods=["GET","POST"])
def index():
    message = ""
    for item in CHALLENGE_ARRAY:
        if(item['chall'](request)):
            message = item['message']
        else:
            break
    return render_template('index.html',message=message)
