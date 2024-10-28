from flask import Flask, render_template, request, Response
from tempfile import mktemp
from os import remove
import ctypes

FLAG = "MINUTEMAN{nOW_w3_CaN_cOmmuNicATE}"

app = Flask(__name__)

# load simavr
ctf_avrsim = ctypes.CDLL(f"../sim/build/libctfavrsim.so")

@app.route("/")
def main_page():
    return render_template("index.html")

@app.route("/upload", methods=['POST'])
def upload():
    # check if the post request has the file part
    if 'file' not in request.files:
        return Response("No file part found. Please upload a elf binary for the server to run.", status=400)
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return Response("No filename found. Please upload a elf binary for the server to run.", status=400)
    
    filename = mktemp(dir="uploads")
    file.save(filename)

    try:
        ret = ctf_avrsim.run_sim(filename.encode())
    except:
        return Response("Fatal error while trying to simulate your code. Please make sure the file provided is an elf binary for the Arduino Uno(atmega328p).")
    finally:
        remove(filename)

    match ret:
        case 0:
            return Response(f"You got the flag! {FLAG}", 200)
        case 1:
            return Response("Simulation timed out without unlocking the flag. Are you pulsing pin 8 at 5 Hz?", 200)
        case 2:
            return Response("Server errored while loading the simulator or firmware. Please make sure the file provided is an elf binary for the Arduino Uno(atmega328p).", 500)
        case 3:
            return Response("Simulator exited with crashed state. This may mean the ELF binary is not for the Arduino Uno(atmega328p) or there are problems in your code.", 500)
        

