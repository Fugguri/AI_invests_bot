from db import Database
from handlers.register import start_register
from handlers.register import RegisterStates
from aiogram import types
from aiogram.dispatcher import FSMContext, middlewares,handler
import logging

class IsUserRegisterMiddleware(middlewares.BaseMiddleware):
    def __init__(self,db:Database ):
        super().__init__()
        self.db = db
        self.logger = logging.getLogger("users_messages")
    async def on_process_message(self, message: types.Message, data: dict):
        state = data.get("state")
        logging.basicConfig(
        level=logging.INFO,
        format=u'[%(asctime)s] - %(message)s',
        filename="logs.log"
    )
        current_state = await state.get_state()
        self.logger.info(message)
        if message.text == "/admin" and self.db.get_user(message.from_user.id).role != "ADMIN":
            raise handler.CancelHandler()
        telegram_id= message.from_user.id
        if not self.db.is_user_registered(telegram_id) and not current_state:
            await start_register(message,state)
            raise handler.CancelHandler()
        