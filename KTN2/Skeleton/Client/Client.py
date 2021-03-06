import socket
from ClientMessageParser import MessageParser
import threading
import json

# Client Class
class Client:

    # Constructor runs when creating a new Client object
    def __init__(self, host, server_port):

        self.valid_reqs = ['login', 'logout', 'msg', 'names', 'help']
        self.host = host
        self.server_port = server_port
        self.parser = MessageParser()
        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.run()

    def run(self):
        # Initiate the connection to the server
        self.connection.connect((self.host, self.server_port))
        # Setup and start a daemon-reciever thread
        recieve_thread = threading.Thread(target=self.receive_message)
        recieve_thread.setDaemon(True)
        recieve_thread.start()
        # And a daemon-sender thread
        send_thread = threading.Thread(target=self.send_payload)
        send_thread.setDaemon(True)
        send_thread.start()
        while 1:
            # Let client send payloads
            #self.send_payload()
            pass


    # close() releases the resource associated with a connection but does not necessarily close the connection
    # immediately. If you want to close the connection in a timely fashion, call shutdown() before close(). - python docs.
    def disconnect(self):
        self.connection.shutdown()
        self.connection.close()

    def receive_message(self):
        while 1:
            message = self.connection.recv(4096)
            print self.parser.parse(message)

    def valid_payload(self, req):
        return req in self.valid_reqs

    def send_payload(self):
        while 1:
            req = raw_input("Request: ").lower()
            while not self.valid_payload(req):
                req = raw_input("Request: ").lower()
            msg_to_send = {'request': req, 'content': None}
            # Add content to payload if required
            if req == "login" or req == "msg":
                content = raw_input("Content: ")
                msg_to_send['content'] = content
            # Json-dump the string for standard JSON-formatted string
            self.connection.send(json.dumps(msg_to_send))
            # Let the console have time to output response from server, find better solution?
            threading._sleep(0.5)


# Main method
if __name__ == '__main__':
    client = Client("localhost", 9998)
