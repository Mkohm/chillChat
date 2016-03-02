

class MessageParser():
    payload = None

    def __init__(self):

        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
	    # More key:values pairs are needed	
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
    # Include more methods for handling the different responses... 
