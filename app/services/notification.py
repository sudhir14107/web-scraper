# services/notification.py
class Notification:
    def __init__(self, recipients: list):
        self.recipients = recipients

    def send_notification(self, success: bool, message: str, data_length: int = 0):
        if success:
            print(f"Success: {message}. Total items: {data_length}")
            # can be extend for email notif
        else:
            print(f"Error: {message}")
            # can be extend for email notif