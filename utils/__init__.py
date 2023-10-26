from .channel_joined import *
from .text_to_speech import *
from .texts import Texts
import re
create_text = Texts()
is_member_in_channel

async def phone_formatter(phone_number:str) -> str:
    if phone_number.startswith("8"):
        phone_number = "+7"+ phone_number[1:]
    if "-" in phone_number:
        phone_number = phone_number.replace("-","")
    if "(" in phone_number:
        phone_number = phone_number.replace("(","")
    if ")" in phone_number:
        phone_number = phone_number.replace(")","")

    return phone_number

async def validate_phone_number(phone_number:str):
    pattern = re.compile(r"(\+\d{1,3})?\s?\(?\d{1,4}\)?[\s.-]?\d{3}?[\s.-]?\d{2}?[\s.-]?\d{2}")
    match = re.search(pattern, phone_number)

    if match:
        return  await phone_formatter(phone_number)
    return False  


__all__ = [
    "text_to_speech",
    'create_text',
    "on_process_message",
    "get_channel_member",
    "is_member_in_channel",

]
