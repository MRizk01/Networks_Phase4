from socket import *

s = socket(AF_INET, SOCK_STREAM)
s.connect(("127.0.1.1", 8000))

while 1:
    s.send(input("Enter message to send: ").encode())