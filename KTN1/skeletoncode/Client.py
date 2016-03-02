# -*- coding: utf-8 -*-
import socket
from MessageReceiver import MessageReceiver
from MessageParser import MessageParser


# This is the chat client class
class Client:
    connection = None
    server_port = 0
    host = None
    running = None

    # This method is run when creating a new Client object
    def __init__(self, host, server_port):
        # Set up the socket connection to the server
        # TODO: Finish init process with necessary code
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_port = server_port
        self.host = host
        self.running = True
        self.run()

    def run(self):
        # Initiate the connection to the server
        self.connection.connect((self.host, self.server_port))

    def disconnect(self):
        # TODO: Handle disconnection

        self.running = False
        pass

    def receive_message(self, message):
        # TODO: Handle incoming message
        msg_receiver = MessageReceiver(client, self.connection)
        msg_receiver.run()
        pass

    def send_payload(self, data):
        # TODO: Handle sending of a payload
        self.connection.send(data)



# This is the main method and is executed when you type "python Client.py"
if __name__ == '__main__':
    client = Client('78.91.37.16',9998)
    while True:
        msg = raw_input("send din melding")
        client.send_payload(msg)
