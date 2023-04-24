import socket
import threading


def main():
    server = ('', 8080)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(server)

    t = threading.Thread(target=listener, args=(s,))
    t.start()

    while True:
        i = input('> ')
        s.send(i.encode('utf-8'))


def listener(conn):
    while True:
        m = conn.recv(2048).decode('utf-8')
        print(m)
        if m == "CLOSING":
            conn.close()
            return


if __name__ == "__main__":
    main()
