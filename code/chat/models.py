from sqlalchemy import ForeignKey
from sqlalchemy import String, select
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from core.db.index import Base
from core.models import User


class ChatMessage(Base):
    __tablename__ = "chat_message"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    sender: Mapped["User"] = relationship(foreign_keys=[sender_id])
    recipient_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    recipient: Mapped["User"] = relationship(foreign_keys=[recipient_id])
    text: Mapped[str] = mapped_column(String(2000))
    read: Mapped[bool] = mapped_column(default=False)

    def __repr__(self) -> str:
        return f"Message(id={self.id!r}, text={self.text!r})"


    @classmethod
    def dialog(cls, session, user1_id: int, user2_id: int):
        """return dialog between user and user2"""
        stmt = (select(ChatMessage)
                .where((ChatMessage.sender_id == user1_id
                        and ChatMessage.recipient_id == user2_id)
                       or (ChatMessage.sender_id == user2_id
                           and ChatMessage.recipient_id == user1_id))
                )
        # TODO
        dialog = session.scalars(stmt).all()
        return dialog
