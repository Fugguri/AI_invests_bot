from db import Database
from handlers.register import start_register
from handlers.register import RegisterStates
from aiogram import types
from aiogram.dispatcher import FSMContext, middlewares,handler


class IsUserRegisterMiddleware(middlewares.BaseMiddleware):
    def __init__(self,db:Database ):
        super().__init__()
        self.db = db

    async def on_process_message(self, message: types.Message, data: dict):
        state = data.get("state")
        current_state = await state.get_state()
        if message.text == "/start":
            return
        if message.text == "/admin" and self.db.get_user(message.from_user.id).role != "ADMIN":
            raise handler.CancelHandler()

        telegram_id= message.from_user.id
        if not self.db.is_user_registered(telegram_id) and not current_state:
            await start_register(message,state)
            raise handler.CancelHandler()
        