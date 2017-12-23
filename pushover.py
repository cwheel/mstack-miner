import requests

class Pushover(object):
    PRIORITY_ULTRA_LOW = -2
    PRIORITY_LOW = -1
    PRIORITY_NORMAL = 0
    PRIORITY_HIGH = 1
    PRIORITY_EMERGENCY = 2

    PUSH_ENDPOINT = 'https://api.pushover.net/1/messages.json'

    def __init__(self, user_token, app_token):
        self.user_token = user_token
        self.app_token = app_token

    def send_notification(self, message, title=None, priority=Pushover.PRIORITY_NORMAL):
        push_body = {
            'user': self.user_token,
            'token': self.app_token,
            'message': message,
            'priority': priority
        }

        if title:
            push_body['title'] = title

        request.post(Pushover.PUSH_ENDPOINT, data=push_body)
