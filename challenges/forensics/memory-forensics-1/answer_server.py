import socket
import threading


HOST = "0.0.0.0"
PORT = 31663

QA = [
    { "What is the exact Major / Minor version of Windows that was running on the computer this memory image came from? (in the format MAJOR_VERSION.MINOR_VERSION)": "15.19041" }, 
    { "What was the system time when this memory image was taken?": "2024-10-20" }, 
    { "What is the name of the process with process ID (PID) 8220?": "chrome" }, 
    { "What IP address was this Google Chrome process connected to?": "142.251.35.174" }, 
    { "What is the PID of the Microsoft Word (WINWORD) process running on the computer?": "7924" }, 
    { "What is the name of the document open in Word?": "rizz" }, 
    { "What is the name of the user who had this document open?": "oppenheimer" }
]


def handle_client(conn):
    i = 0
    while i < len(QA):
        question = list(QA[i].keys())[0]
        answer = QA[i][question]
        conn.sendall(f"({i + 1}/{len(QA)}) {question}\nAnswer: ".encode())
        response = conn.recv(1024).decode().strip().lower()
        if answer not in response:
            conn.sendall("Incorrect answer. Try again.\n".encode())
            continue
        conn.sendall("Correct!\n".encode())
        i += 1
    conn.sendall("Congratulations! You have answered all questions correctly.\n".encode())
    conn.sendall("Flag: MINUTEMAN{m3m0ry_f0r3ns1cs_1s_c00l}\n".encode())
    conn.close()


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(20)
    try:
        while True:
            conn, _ = s.accept()
            threading.Thread(target=handle_client, args=(conn,)).start()
    except KeyboardInterrupt:
        s.close()


if __name__ == "__main__":
    main()