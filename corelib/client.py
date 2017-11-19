import socket

sock = socket.socket()
sock.connect(("127.0.0.1", 1001))
message = "Hello server"
sock.sendall(message.encode("utf8"))
sock.close()


