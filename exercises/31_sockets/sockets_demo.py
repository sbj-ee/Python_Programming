"""Exercise 31: Sockets.

A TCP echo server and client over the loopback interface, run in the same
process via a background thread so the exercise is self-contained.
"""

import socket
import threading


def run_echo_server(server_socket: socket.socket, ready: threading.Event) -> None:
    server_socket.bind(("127.0.0.1", 0))  # port 0 -> OS picks a free port
    server_socket.listen(1)
    ready.set()

    conn, _addr = server_socket.accept()
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break  # client closed the connection
            conn.sendall(data)  # echo it back verbatim


def send_all(sock: socket.socket, data: bytes) -> None:
    """TCP makes no promise that one send() call delivers all your bytes in
    one write; sendall() loops until everything is sent.
    """
    sock.sendall(data)


def recv_exactly(sock: socket.socket, n: int) -> bytes:
    """Symmetric problem on the receive side: recv() can return fewer bytes
    than requested. Loop until exactly n bytes have arrived.
    """
    chunks = []
    remaining = n
    while remaining > 0:
        chunk = sock.recv(remaining)
        if not chunk:
            raise ConnectionError("socket closed before all bytes received")
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)


def main() -> None:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ready = threading.Event()
    server_thread = threading.Thread(
        target=run_echo_server, args=(server_socket, ready), daemon=True
    )
    server_thread.start()
    ready.wait()  # don't connect until the server is actually listening

    host, port = server_socket.getsockname()
    print(f"server listening on {host}:{port}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((host, port))

        message = b"Hello over TCP!"
        send_all(client, message)
        echoed = recv_exactly(client, len(message))
        print(f"sent: {message!r}")
        print(f"echoed back: {echoed!r}")
        assert echoed == message

        # A longer message, to show recv may need more than one call
        big_message = b"x" * 100_000
        send_all(client, big_message)
        echoed_big = recv_exactly(client, len(big_message))
        print(f"large message round-trip ok: {echoed_big == big_message}")

    server_socket.close()

    # --- UDP: connectionless, datagram-oriented, no delivery guarantee ---
    udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_server.bind(("127.0.0.1", 0))
    udp_host, udp_port = udp_server.getsockname()

    udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_client.sendto(b"ping", (udp_host, udp_port))
    data, client_addr = udp_server.recvfrom(1024)
    print(f"UDP server received {data!r} from {client_addr}")
    udp_server.sendto(b"pong", client_addr)
    reply, _ = udp_client.recvfrom(1024)
    print(f"UDP client received {reply!r}")

    udp_server.close()
    udp_client.close()


if __name__ == "__main__":
    main()
