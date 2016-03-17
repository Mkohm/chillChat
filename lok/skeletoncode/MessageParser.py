
class MessageParser():
    payload = None

    def __init__(self):

        self.possible_responses = {
            # More key:values pairs are needed
            'error': self.parse_error,
            'info': self.parse_info,
            'login': self.parse_login,
            'logout': self.parse_logout,
            'msg': self.parse_msg,
            'names': self.parse_names,
            'help': self.parse_help,
        }

    def parse(self, payload):
        # decode the JSON object
        self.payload = payload

        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            return
            # Response not valid

    def parse_error(self, payload):

        return

    def parse_info(self, payload):
        return
    def parse_login(self, payload):
        return
    def parse_msg(self, payload):
        return
    def parse_names(self, payload):
        return
    def parse_help(self, payload):
        return
    # Include more methods for handling the different responses... 
