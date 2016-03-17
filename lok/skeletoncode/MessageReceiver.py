# -*- coding: utf-8 -*-
from threading import Thread


class MessageReceiver(Thread):
    client = None
    connection = None

    # This method is executed when creating a new MessageReceiver object
    def __init__(self, client, connection):
        super(MessageReceiver, self).__init__()
        self.client = client
        self.connection = connection
        # Flag to run thread as a deamon
        self.daemon = False
        # TODO: Finish initialization of MessageReceiver

    def run(self):
        while True:
            msg = self.client.connection.recv(4096)
            if msg != "" or not msg == None:
                print msg


