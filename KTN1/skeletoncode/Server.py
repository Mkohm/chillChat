# -*- coding: utf-8 -*-
import SocketServer

"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""

dict= {}

class ClientHandler(SocketServer.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """

    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request

        print  self.ip +" is now connected"


        dict[self.ip] = self.connection
        msg = self.ip +" is now connected"
        for key,value in dict.items():
                    if key != self.ip:
                        value.send(msg)


        # Loop that listens for messages from the client
        while True:
            received_string = self.connection.recv(4096)
            if received_string != "" or not received_string == None:
                msg = self.ip + ": " + received_string
                print msg
                msg_ip = self.ip
                for key,value in dict.items():
                    if key != msg_ip:
                        value.send(msg)


            # TODO: Add handling of received payload from client


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):

    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations are necessary
    """
    allow_reuse_address = True

if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.

    No alterations are necessary
    """
    HOST, PORT = '78.91.37.16', 9998


    print 'Server running...'
    # Set up and initiate the TCP server

    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
