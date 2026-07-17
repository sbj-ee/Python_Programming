"""Exercise 32: I/O Multiplexing.

The selectors module wraps the best available OS mechanism (epoll on Linux,
kqueue on BSD/macOS, select as a fallback) behind one API: register file
objects for read/write readiness, then block on all of them at once instead
of one thread per connection. This is how a single-threaded server handles
thousands of concurrent clients.
"""

import selectors
import socket
import threading
from typing import cast

sel = selectors.DefaultSelector()


def start_multiclient_server(server_socket: socket.socket, ready: threading.Event) -> None:
    server_socket.bind(("127.0.0.1", 0))
    server_socket.listen()
    server_socket.setblocking(False)
    sel.register(server_socket, selectors.EVENT_READ, data="accept")
    ready.set()

    connections_served = 0
    while connections_served < 3:
        # select() blocks here until at least one registered socket is
        # ready -- no polling loop, no per-client thread.
        events = sel.select(timeout=2)
        for key, _mask in events:
            if key.data == "accept":
                listener = cast(socket.socket, key.fileobj)
                conn, _addr = listener.accept()
                conn.setblocking(False)
                sel.register(conn, selectors.EVENT_READ, data="client")
            else:
                conn = cast(socket.socket, key.fileobj)
                data = conn.recv(1024)
                if data:
                    conn.sendall(data)  # echo
                else:
                    sel.unregister(conn)
                    conn.close()
                    connections_served += 1

    sel.unregister(server_socket)
    server_socket.close()


def main() -> None:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ready = threading.Event()
    server_thread = threading.Thread(
        target=start_multiclient_server, args=(server_socket, ready)
    )
    server_thread.start()
    ready.wait()
    host, port = server_socket.getsockname()
    print(f"multiplexed server listening on {host}:{port}")

    # Three separate clients, all served by ONE thread on the server side.
    for i in range(3):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((host, port))
            message = f"client-{i}".encode()
            client.sendall(message)
            response = client.recv(1024)
            print(f"client {i}: sent {message!r}, received {response!r}")

    server_thread.join()
    print("server handled all 3 clients on a single thread via selectors")

    # --- What selectors abstracts over ---
    print(f"\nselector implementation in use: {type(selectors.DefaultSelector()).__name__}")
    print("  Linux -> EpollSelector, macOS/BSD -> KqueueSelector, fallback -> SelectSelector")


if __name__ == "__main__":
    main()
