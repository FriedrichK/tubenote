from message.models import Message


def create_message(user, content):
    message = Message(user=user, content=content)
    message.save()
    return message
