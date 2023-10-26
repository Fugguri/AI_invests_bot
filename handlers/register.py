from aiogram import types, Bot
from aiogram import Dispatcher, filters
from aiogram.dispatcher.handler import ctx_data
from aiogram.dispatcher import FSMContext

from utils import validate_phone_number, texts
from config.config import Config
from db import Database
from keyboards.keyboards import Keyboards
from models import *
from .users import start

@dataclass
class RegisterStates:
    FIRSTNAME = "firstname"
    LASTNAME = "lastname"
    PHONE = "phone"
    ORGANIZATION = "organization"
    VERIFY = "verify"

    def is_in(self, value: str) -> bool:
        return  value in (self.FIRSTNAME,self.LASTNAME,self.ORGANIZATION,self.PHONE,self.VERIFY)
    
    
async def start_register(message: types.Message, state: FSMContext):
    await message.answer("Пожалуйста, пройдите небольшую регистрацию.\n<b>Введите ваше имя</b> ")
    await state.set_state(RegisterStates.FIRSTNAME)
    
async def wait_firstname(message: types.Message, state: FSMContext):
    kb: Keyboards = ctx_data.get()['keyboards']
    await state.update_data(firstname=message.text)
    await state.set_state(RegisterStates.LASTNAME)
    await message.answer("<b>Введите вашу фамилию</b>")
    
async def wait_lastname(message: types.Message, state: FSMContext):
    cfg: Config = ctx_data.get()['config']
    kb: Keyboards = ctx_data.get()['keyboards']
    db: Database = ctx_data.get()['db']
    await state.update_data(lastname=message.text)
    await state.set_state(RegisterStates.PHONE)
    await message.answer("<b>Введите ваш номер телефона</b>")
    
async def wait_phone(message: types.Message, state: FSMContext):
    cfg: Config = ctx_data.get()['config']
    kb: Keyboards = ctx_data.get()['keyboards']
    db: Database = ctx_data.get()['db']
    phone = await validate_phone_number(message.text)
    if not phone:
        await message.answer("<b>Проверьте введеный вами телефон. Возможно в нем ошибка</b>")
        return
    await state.update_data(phone=phone)
    await state.set_state(RegisterStates.ORGANIZATION)
    await message.answer("<b>Вы самостоятельный инвестор да/нет если нет, то напишите название фонда или организации</b>")
    
async def wait_organization(message: types.Message, state: FSMContext):
    kb: Keyboards = ctx_data.get()['keyboards']
    await state.update_data(organization=message.text)
    markup= await kb.registration_confirm_kb()
    data = await state.get_data()
    
    await message.answer("Подтвердите введенные вами данные:\n"+ await texts.Texts.create_profile_str(data),reply_markup=markup)

    await state.set_state(RegisterStates.VERIFY)

async def verify_registration(callback: types.CallbackQuery, state: FSMContext,callback_data:dict):
    cfg: Config = ctx_data.get()['config']
    kb: Keyboards = ctx_data.get()['keyboards']
    db: Database = ctx_data.get()['db']

    command = callback_data.get("command")
    match command:
        
        case "confirm":
            data = await state.get_data()
            db.update_user_data(callback.from_user.id, data)
            await start(callback.message,state)
        case "again":
            await callback.message.answer("<b>Введите ваше имя</b> ")
            await state.set_state(RegisterStates.FIRSTNAME)
            await state.reset_data()
            return
        
    await state.finish()

async def back(callback: types.CallbackQuery, state: FSMContext, callback_data: dict):
    db: Database = ctx_data.get()['db']
    kb: Keyboards = ctx_data.get()['keyboards']

    if callback_data['role'] == "admin":
        await admin(callback.message)
    if callback_data['role'] == "user":
        await start(callback.message, state)

    await callback.message.delete()


def register_register_handlers(dp: Dispatcher, kb: Keyboards):
    dp.register_message_handler(start_register,lambda m: m.text=="Регистрация")
    dp.register_message_handler(wait_firstname, state=RegisterStates.FIRSTNAME)
    dp.register_message_handler(wait_lastname, state=RegisterStates.LASTNAME)
    dp.register_message_handler(wait_phone,  state=RegisterStates.PHONE)
    dp.register_message_handler(wait_organization,  state=RegisterStates.ORGANIZATION)
    # dp.register_message_handler(verify_registration,  state=RegisterStates.VERIFY)
    dp.register_callback_query_handler(verify_registration, kb.registration_confirm_cd.filter(), state=RegisterStates.VERIFY)