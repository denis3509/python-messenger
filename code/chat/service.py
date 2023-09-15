import dataclasses
from dataclasses import dataclass
from datetime import datetime
from typing import List

from sqlalchemy import update, text
from sqlalchemy.orm import Session

from chat import models as mdl
from core import models as core_mdl


class BaseDTO:
    @classmethod
    def match_kwargs(cls, **kwargs):
        filtered_kwargs = {}
        names = set([f.name for f in dataclasses.fields(cls)])
        for k, v in kwargs.items():
            if k in names:
                filtered_kwargs[k] = v
        return cls(**filtered_kwargs)

    def as_dict(self):
        result = {}
        for f in dataclasses.fields(self):
            result[f] = getattr(self, f.name)
        return result


@dataclass
class CreateMessageDTO(BaseDTO):
    recipient_id: int
    text: str


@dataclass
class EditMessageDTO(BaseDTO):
    id: int
    text: str


@dataclass
class Contact(BaseDTO):
    user_id: int
    username: str
    # max_time: datetime
    last_message: str
    last_message_read: bool
    last_message_time: datetime
    unread: bool


class Chat:
    def __init__(self, session: Session, auth_user: core_mdl.User | None):
        self.session = session
        self.auth_user = auth_user

    def is_auth(self):
        if self.auth_user is None:
            raise PermissionError("auth required")

    def create_message(self, message: CreateMessageDTO) -> mdl.ChatMessage:
        self.is_auth()
        if self.auth_user.id == message.recipient_id:
            raise ValueError("recipient_id cant be equal to sender_id")
        message = mdl.ChatMessage(
            sender_id=self.auth_user.id,
            recipient_id=message.recipient_id,
            text=message.text
        )

        self.session.add(message)
        return message

    def delete_message(self, message_id: int):
        self.is_auth()
        message = self.session.get(mdl.ChatMessage, message_id)
        if message.sender_id != self.auth_user.id:
            raise PermissionError(f"{str(self.auth_user)} are not sender of {message}")
        self.session.delete(message)

    def edit_message(self, edit_message: EditMessageDTO):
        self.is_auth()
        message = self.session.get(mdl.ChatMessage, edit_message.id)
        if message.sender_id != self.auth_user.id:
            raise PermissionError(f"{str(self.auth_user)} are not sender of {message}")
        message.text = edit_message

    def contact_list(self) -> List[Contact]:
        self.is_auth()
        raw_sql = """select u2        as user_id,

       user_account.username,


       max_time,
       (select text
        from chat_message
        where created_at = max_time
          and (sender_id  = :u_id or recipient_id  = :u_id)
        limit 1) as last_message,
       (select read
        from chat_message
        where created_at = max_time
          and (sender_id  = :u_id or recipient_id  = :u_id)
        limit 1) as last_message_read,
       (select chat_message.created_at
        from chat_message
        where created_at = max_time
          and (sender_id  = :u_id or recipient_id  = :u_id)
        limit 1) as last_message_time,
       unread
from (select (case
                  when (sender_id  = :u_id)
                      then (sender_id)
                  when (sender_id != :u_id)
                      then recipient_id
    end)                     as u1,
             (case
                  when (sender_id  = :u_id)
                      then (recipient_id)
                  when (sender_id != :u_id)
                      then sender_id
                 end)        as u2,

             max(created_at) as max_time

      from chat_message
      where (sender_id  = :u_id or recipient_id  = :u_id)
        and (sender_id is not null and recipient_id is not null)


      group by u1, u2
     ) as receivers_id
         left join user_account
                   on receivers_id.u2 = user_account.id

         left join (select sender_id, count(id) as unread
                    from chat_message m
                    where recipient_id  = :u_id
                      and read = false
                    group by sender_id
) as counter
                   on
                       u2 = counter.sender_id
order by max_time desc;"""
        stmt = text(raw_sql)
        rows = self.session.execute(stmt, params=dict(u_id=self.auth_user.id)).all()
        result = []
        for r in rows:
            result.append(Contact.match_kwargs(**r._mapping))
        return result

    def read_contact_messages(self, contact_id: int):
        stmt = (
            update(mdl.ChatMessage).
            where(mdl.ChatMessage.sender_id == contact_id and
                  mdl.ChatMessage.recipient_id == self.auth_user.id).
            values(read=True)
        )
        self.session.execute(stmt)

#
#
#
#
# class Chat:
#     @staticmethod
#     def create_message(session: Session, message: CreateMessageDTO, user: core_mdl.User) -> mdl.Message:
#         if user is None:
#             raise PermissionError("auth required")
#         if user.id == message.recipient_id:
#             raise ValueError("recipient_id cant be equal to sender_id")
#         message = mdl.Message(
#             sender_id=user.id,
#             recipient_id=message.recipient_id,
#             text=message.text
#         )
#
#         session.add(message)
#         return message
#
#     @staticmethod
#     def delete_message(session: Session, message_id: int, user: core_mdl.User):
#         if user is None:
#             raise PermissionError("auth required")
#         message = session.get(mdl.Message, message_id)
#         if message.sender_id != user.id:
#             raise PermissionError(f"{str(user)} are not sender of {message}")
#         session.delete(message)
#
#     @staticmethod
#     def edit_message():
#         pass
#     @staticmethod
#     def dialog_list(session: Session, user: core_mdl.User):
#         pass
#
#     @staticmethod
#     def read_dialog(session: Session, user: core_mdl):
#         pass
#
#
