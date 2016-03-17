# -*- coding: utf-8 -*-
import SocketServer
import json
import time

"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""

connected_clients = {}
history = []

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
        self.username = ""
        self.logged_in = False
        print self.ip, self.port, self.request

        # Loop that listens for messages from the client
        while True:
            try:
                received_string = self.connection.recv(4096)
            except:
                # handles the errno-10054, might not be the best solution.
                # drops this BaseRequestHandler with finish() thats called after handle returns
                return
            print received_string
            try:
                received_json = json.loads(received_string)

                request = received_json["request"]
                content = received_json["content"]

                if request == "login":
                    self.handle_login(content)
                elif request == "logout" and self.logged_in:
                    self.handle_logout()
                elif request == "msg" and self.logged_in:
                    message = received_json["content"]
                    self.handle_message(message)
                elif request == "names" and self.logged_in:
                    self.handle_names()
                elif request == "help":
                    self.handle_help()
                else:
                    self.send_response("server", "error", "Not logged in.")
            except ValueError:
                return

    def handle_login(self, username):
        if self.logged_in:
            self.send_response("server", "error", "Already logged in.")
        else:
            self.username = username
            if not self.username.isalnum():
                self.send_response("server", "error", "Username can only contain letters a-z and numbers 0-9")
            else:
                if self.username not in connected_clients.keys():
                    self.logged_in = True
                    connected_clients[self.username] = self
                    self.send_response("server", "info", "Login successful")
                    self.send_history()
                else:
                    self.send_response("server", "error", "Username taken.")

    def send_history(self):
        if len(history) > 0:
            history_json = []
            for i in range(0, len(history)):
                history_json.append(json.dumps(history[i]))
            out = json.dumps(self.get_payload("server", "history", history_json))
            print out
            self.connection.send(out)

    def handle_logout(self):
        self.logged_in = False
        connected_clients.pop(self.username)
        self.send_response("server", "info", "Logout successful")

    def handle_message(self, message):
        for client in connected_clients:
            connected_clients[client].send_response(self.username, "message", message)

        history.append(self.get_payload(self.username, "message", message))

    def handle_names(self):
        self.send_response("server", "info", connected_clients.keys())

    def handle_help(self):
        out = ""
        with open("Help.txt") as f:
            lines = f.readlines()
            for line in lines:
                out += line

        self.send_response("server", "info", out)

    def send_response(self, sender, response, content):
        print "sending a respone: " + str(self.get_payload(sender, response, content))
        self.connection.send(json.dumps(self.get_payload(sender, response, content)))

    def get_payload(self, sender, response, content):
        return {
            "timestamp": self.make_time_appear_pretty(time.time()),
            "sender": sender,
            "response": response,
            "content": content
        }

    def finish(self):
        self.logged_in = False
        if self.username in connected_clients.keys():
            connected_clients.pop(self.username)
        print(self.username + " disconnected, removing from connected clients.")

    def make_time_appear_pretty(self, timeNow):
        return time.asctime(time.localtime(timeNow))

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
    HOST, PORT = "localhost", 9998
    print 'Server running...'

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
