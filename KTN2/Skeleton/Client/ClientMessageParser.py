import json


class MessageParser:
    def __init__(self):

        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'message': self.parse_message,
            'history': self.parse_history
        }

    def parse(self, payload):
        try:
            message = json.loads(payload)
            return self.possible_responses[message['response']](message)
        except ValueError:
            print 'There is an error in the JSON-string trying to be parsed.'
            return ''

    def parse_error(self, payload):
        return payload['timestamp'] + ' - ' + payload['content']
    
    def parse_info(self, payload):
        # convert to string in case its a list (of the names)
        return payload['timestamp'] + ' - ' + str(payload['content'])

    def parse_message(self, payload):
        return payload['timestamp'] + ' - ' + payload['sender'] + ': ' + payload['content']

    def parse_history(self, payload):
        messages = payload["content"]
        out = ""
        for msg in messages:
            out += self.parse_message(json.loads(msg)) + "\n"

        return out
