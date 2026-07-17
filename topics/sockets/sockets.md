# Sockets

The `socket` module wraps the BSD sockets API directly — the same system
calls C uses, with a thinner, more Pythonic layer on top. TCP
(`SOCK_STREAM`) is a reliable, ordered byte stream; UDP (`SOCK_DGRAM`) is
connectionless, unordered, and can lose or duplicate datagrams.

## TCP server

```python
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("0.0.0.0", 8080))
server.listen()

conn, addr = server.accept()     # blocks until a client connects
data = conn.recv(1024)
conn.sendall(b"echo: " + data)
conn.close()
```

## TCP client

```python
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 8080))
client.sendall(b"hello")
response = client.recv(1024)
client.close()

# Context manager form closes automatically:
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("127.0.0.1", 8080))
    ...
```

## TCP gives no message boundaries: sendall/recv discipline

```python
def send_all(sock, data: bytes) -> None:
    sock.sendall(data)     # loops internally until ALL bytes are sent

def recv_exactly(sock, n: int) -> bytes:
    chunks = []
    remaining = n
    while remaining > 0:
        chunk = sock.recv(remaining)
        if not chunk:
            raise ConnectionError("socket closed early")
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)
```

A single `send()` may not transmit all bytes in one call, and a single
`recv()` may return fewer bytes than requested (or than the sender sent in
one call) — TCP is a byte stream, not a message stream. Real protocols use
a length prefix or a delimiter to know where one message ends.

## UDP: connectionless datagrams

```python
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind(("0.0.0.0", 9000))
data, addr = udp.recvfrom(1024)      # each recvfrom() gets ONE whole datagram
udp.sendto(b"reply", addr)            # no connect() needed -- address per-call
```

## getaddrinfo: portable DNS/address resolution

```python
# Resolves a hostname to (family, socktype, proto, canonname, sockaddr) tuples,
# handling both IPv4 and IPv6 uniformly -- the portable alternative to
# hardcoding AF_INET.
for family, socktype, proto, _, addr in socket.getaddrinfo("example.com", 80):
    s = socket.socket(family, socktype, proto)
    s.connect(addr)
    break
```

## Common pitfalls

| Pitfall | Consequence | Fix |
|---------|-------------|-----|
| Assuming one `send()`/`recv()` = one message on TCP | Messages get split or merged unpredictably | Use a length prefix or delimiter; loop until the full message is sent/received |
| Forgetting `SO_REUSEADDR` on a server | `OSError: Address already in use` after a quick restart | Set `setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)` before `bind()` |
| Blocking `accept()`/`recv()` in a single-threaded server | Only one client can be served at a time | Use threads, `selectors` (see [[io_multiplexing]]), or `asyncio` for multiple clients |
| Not closing sockets | File descriptor leak over the process lifetime | Use `with socket.socket(...) as s:` |
| Assuming UDP delivers, preserves order, or avoids duplicates | Silent data loss/reordering under real network conditions | Use TCP, or build acknowledgment/sequencing into the application protocol |
