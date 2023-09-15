from sqlalchemy.orm import Session

from core.db import main_engine
from core.test.utils import BaseFaker
from chat import models as mdl


class ChatFaker(BaseFaker):
    def chat_message(self, sender_id: int,
                     recipient_id: int,
                     text: int = None,
                     read: bool = None,
                     add=True):
        created_at = self.timestamp()
        chat_msg = mdl.ChatMessage(
            sender_id=sender_id,
            recipient_id=recipient_id,
            text=text or self.text(self.random.randrange(500, 2000)),
            read=read or False,
            created_at=created_at,
            updated_at=created_at
        )
        if add:
            self._add(chat_msg)
        return chat_msg

    def dialog(self, sender_id: int,
               recipient_id: int,
               amount=50,
               add=True):
        _messages = []
        for i in range(amount):
            _messages.append(self.chat_message(sender_id, recipient_id, add=False))
        if add:
            self._add(_messages)
        return _messages


if __name__ == "__main__":
    with Session(main_engine) as session:
        faker = ChatFaker(session)
        user = faker.users(5)

    print(user)
