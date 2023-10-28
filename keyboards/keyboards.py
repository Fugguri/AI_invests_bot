from config.config import Config
from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup,\
    ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from models import *


class Keyboards:
    def __init__(self, cfg: Config) -> None:
        self.text = cfg.misc.buttons_texts
        self.start_cd = CallbackData("start", "character_id")
        self.admin_cd = CallbackData("mailing", "command")
        self.mailing_cd = CallbackData("admin", "command")
        self.registration_confirm_cd = CallbackData("confirm", "command")

        self.back_cd = CallbackData("back", "role")

    async def start_kb(self, categories: tuple[Category]):
        res = []
        for category in categories:
            res.append([KeyboardButton(text=category.name)])
        
        return ReplyKeyboardMarkup(keyboard=res,resize_keyboard=True, row_width=3)

    async def bots_kb(self, bots):
        kb = InlineKeyboardMarkup()
        for bot in bots:
            # kb.add(InlineKeyboardButton(text="Рассылка сообщений",
            #                                 url="dsds"))
            1
        return kb

    async def category_kb(self, categories: list[Keyboard]):
        kb = InlineKeyboardMarkup()
        for cat in categories:
            if cat.link:
                kb.add(InlineKeyboardButton(text=cat.text, url=cat.link))
            elif cat.callback:
                kb.add(InlineKeyboardButton(
                    text=cat.text, callback_data=cat.callback))
        kb.add(InlineKeyboardButton(text="Назад",
               callback_data=self.back_cd.new(role='user')))
        return kb


    async def registration_confirm_kb(self):
        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton(text="Все верно",callback_data=self.registration_confirm_cd.new("confirm")))
        kb.add(InlineKeyboardButton(text="Начать сначала",callback_data=self.registration_confirm_cd.new("again")))
        
        return kb

    async def admin_kb(self):
        kb = InlineKeyboardMarkup()

        kb.add(InlineKeyboardButton(text="Рассылка сообщений",
               callback_data=self.admin_cd.new(command="mail")))
        kb.add(InlineKeyboardButton(text="Статистика",
               callback_data=self.admin_cd.new(command="statistic")))
        kb.add(InlineKeyboardButton(text="Назад",
               callback_data=self.back_cd.new(role='user')))

        return kb

    async def mailing_kb(self, state: str = None, photo: bool = False):
        kb = InlineKeyboardMarkup()
        if state == "wait_mail_text":
            kb.add(InlineKeyboardButton(text="Назад",
                                        callback_data=self.back_cd.new('admin')))
        if state == 'wait_mail_photo':
            kb.add(InlineKeyboardButton(text="Без фото",
                   callback_data=self.mailing_cd.new("no_photo")))
            if photo:
                kb.add(InlineKeyboardButton(text="Отправить с фото",
                                            callback_data=self.mailing_cd.new("start_with_photo")))
        if state == 'confirm':
            kb.add(InlineKeyboardButton(text="Начать рассылку",
                   callback_data=self.mailing_cd.new("start")))
            kb.add(InlineKeyboardButton(text="Редактировать",
                   callback_data=self.admin_cd.new(command="mail")))
        return kb

    async def back_kb(self, role):
        kb = InlineKeyboardMarkup()

        kb.add(InlineKeyboardButton(text="Назад",
               callback_data=self.back_cd.new(role=role)))

        return kb
