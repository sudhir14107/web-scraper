# services/notification.py
class Notification:
    def __init__(self, recipients: list):
        self.recipients = recipients

    def send_notification(self, success: bool, message: str, data: dict= None):
        if success:
            print(f"Success: {message}, data: {data}")
            # can be extend for email notif
        else:
            print(f"Error: {message}")
            # can be extend for email notif