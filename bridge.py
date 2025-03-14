import socket
import json

class Element:
    def __intit__(self):
        pass
    def start():
        global client
        try:

            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(("192.168.137.47", 12345)) 
            return "Connection Successful and stabilising..."
        except Exception as e:
            return "Error Refused!"



    def send(key,value):
        d = {key: value}

        client.sendall(json.dumps(d).encode("utf-8"))

        if key == "1":
            response = client.recv(1024).decode("utf-8")
            return response
        
        else:
            return False
