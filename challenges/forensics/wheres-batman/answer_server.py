import socket
import threading


HOST = "0.0.0.0"
PORT = 48090

QA = [
    { "What are the names of the three criminals Batman was investigating?": ["joker", "riddler", "penguin"] }, 
    { "How much did the penguins spend on healthcare last quarter?": "10000" }, 
    { "What country were the penguins on vacation in?": "bahamas" }, 
    { "How many riddles did the Riddler send to Batman?": "3" }, 
    { "What riddle did Batman respond with?": "what can never be put in a saucepan" }, 
    { "We just got a tip that Batman is a big fan of Notepad++!  What does he claim to need in his notes?": "vacation" }, 
    { "What place did Batman search for when making his plans?": "cancun" }, 
    { "What was Batman's flight number?": "65348" },
    { "What is the name of the hotel Batman is staying at?": "nyx" },
]


def handle_client(conn):
    i = 0
    while i < len(QA):
        question = list(QA[i].keys())[0]
        answer = QA[i][question]
        conn.sendall(f"({i + 1}/{len(QA)}) {question}\nAnswer: ".encode())
        response = conn.recv(1024).decode().strip().lower()
        if any(a not in response for a in answer):
            conn.sendall("Incorrect answer. Try again.\n".encode())
            continue
        conn.sendall("Correct!\n".encode())
        i += 1
    conn.sendall("Congratulations! You have answered all questions correctly.\n".encode())
    conn.sendall("Flag: MINUTEMAN{wh7_f1gh7_cr1m3_wh3n_c4ncun_1s_an_0pt10n}\n".encode())
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