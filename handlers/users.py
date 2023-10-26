from aiogram import types
from aiogram import Dispatcher
from aiogram.dispatcher.handler import ctx_data
from aiogram.dispatcher import FSMContext

from utils import *
from config.config import Config
from db import Database
from keyboards.keyboards import Keyboards
from models import *
import os
from .admin import admin


async def start(message: types.Message, state: FSMContext):
    cfg: Config = ctx_data.get()['config']
    kb: Keyboards = ctx_data.get()['keyboards']
    db: Database = ctx_data.get()['db']
    try:
        db.get_user(message.from_user.id)
    except:
        db.add_user(message.from_user)

    characters = db.get_all_categories()
    markup = await kb.start_kb(characters)
    await message.answer(cfg.misc.messages.start, reply_markup=markup)
    try:
        pass
    except:
        await message.message.answer(cfg.misc.messages.start, reply_markup=markup)

    await state.finish()


async def projects(message: types.Message, state: FSMContext):
    cfg: Config = ctx_data.get()['config']
    kb: Keyboards = ctx_data.get()['keyboards']
    db: Database = ctx_data.get()['db']
    # await check(message)
    cat: Category = db.get_category(message.text)
    if cat:
        await message.delete()
        markup = await kb.category_kb(cat.keyboards)
        await message.answer(cat.description, reply_markup=markup)
        db.update_category_count(message.text)
    else:
        pass

    # categories: tuple[Category] = db.get_all_categories()

    # for cat in categories:
    #     # print(cat)
    #     if cat.name == message.text:


async def check(callback: types.CallbackQuery):
    cfg: Config = ctx_data.get()['config']
    kb: Keyboards = ctx_data.get()['keyboards']
    db: Database = ctx_data.get()['db']
    channels_text = ""
    all_joined = True
    for channel in db.get_channels():
        member = await get_channel_member(channel.channel_id, callback)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(
            text="Проверить подписку", callback_data="check"))
        if not is_member_in_channel(member):
            all_joined = False
            channels_text += "\n"+channel.name
    if channels_text == "":
        return

    try:
        await callback.message.answer(channels_text)
    except:
        await callback.answer(channels_text)


async def back(callback: types.CallbackQuery, state: FSMContext, callback_data: dict):
    db: Database = ctx_data.get()['db']
    kb: Keyboards = ctx_data.get()['keyboards']

    if callback_data['role'] == "admin":
        await admin(callback.message)
    if callback_data['role'] == "user":
        await start(callback.message, state)

    await callback.message.delete()


def register_user_handlers(dp: Dispatcher, kb: Keyboards):
    dp.register_message_handler(start, commands=["start"], state="*")
    dp.register_message_handler(projects, state="*")
    dp.register_callback_query_handler(back, kb.back_cd.filter(), state="*")
    dp.register_callback_query_handler(
        back, lambda x: x.data == "check", state="*")
