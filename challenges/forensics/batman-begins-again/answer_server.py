import socket
import threading


HOST = "0.0.0.0"
PORT = 41451

QA = [
    { "According to the prefetch files, which program was run for the FIRST TIME after 2:00PM on 2024-10-24?": "vnc" },
    { "What was the device ID USB device was connected to the computer just before VNC Server was installed?": "07038579b2019540" },
    { "After VNC server was installed, what the next non-system program run?": "notepad" },
    { "What is the name of the file that was opened in Notepad after VNC server was installed?": "todo.txt" },
    { "What is the first line of todo.txt?": ["pay", "alfred"] },
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
    conn.sendall("Flag: MINUTEMAN{4lw4ys_p4y_y0ur_empl0y33s_w3ll}\n".encode())
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