import socket
import threading


HOST = "0.0.0.0"
PORT = 43800

QA = [
    { "What was the initial point of access for the attackers?": ["phishing", "email", "attachment"] },
    { "What email address did the attackers use to send the malicious attachment?": "joker.armory" },
    { "How did the attackers execute code on the victim's machine?": ["macro", "vba", "visual basic"] },
    { "What IP address did the Joker attack from?": "192.168.157.145" },
    { "What was the first command run once a shell was obtained?": ["ls", "new-computeruser"] },
    { "What is the name of the user that was created on the victim's machine?": "batmansux" },
    { "How did the attackers maintain persistence on the victim's machine?": "startup" },
    { "What is the name of the file that was used to maintain persistence?": "for_batman" },
    { "What files did the attackers remove?": ["Nolanverse_Joker_Render.webp", "images.png"]}
]


def handle_client(conn):
    i = 0
    while i < len(QA):
        question = list(QA[i].keys())[0]
        answer = QA[i][question]
        conn.sendall(f"({i + 1}/{len(QA)}) {question}\nAnswer: ".encode())
        response = conn.recv(1024).decode().strip().lower()
        if all(a not in response for a in answer):
            conn.sendall("Incorrect answer. Try again.\n".encode())
            continue
        conn.sendall("Correct!\n".encode())
        i += 1
    conn.sendall("Congratulations! You have answered all questions correctly.\n".encode())
    conn.sendall("Flag: MINUTEMAN{wh3n_1n_d0ub7_em4il_1s_alw4ys_th3_pr0bl3m}\n".encode())
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