from db import Database

from aiogram import types
from aiogram.dispatcher import FSMContext, middlewares


class ActivityUpdaterMiddleware(middlewares.BaseMiddleware):
    def __init__(self,db:Database ):
        super().__init__()
        self.db = db

    async def on_process_message(self, message: types.Message, data: dict):
        try:
            telegram_id=message.from_user.id
            self.db.update_activity(telegram_id)
        except:
            pass