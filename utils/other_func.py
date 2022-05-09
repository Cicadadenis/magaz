# - *- coding: utf- 8 - *-
import asyncio
import datetime
import time

import requests
from aiogram import Dispatcher
from bs4 import BeautifulSoup

from data.config import admins, bot_version, bot_description
from loader import bot
from utils.db_api.sqlite import get_settingsx, update_settingsx



# Рассылка сообщения всем администраторам
async def send_all_admin(message, markup=None, not_me=0):
    if markup is None:
        for admin in admins:
            try:
                if str(admin) != str(not_me):
                    await bot.send_message(admin, message, disable_web_page_preview=True)
            except:
                pass
    else:
        for admin in admins:
            try:
                if str(admin) != str(not_me):
                    await bot.send_message(admin, message, reply_markup=markup, disable_web_page_preview=True)
            except:
                pass


# Получение текущей даты
def get_dates():
    return datetime.datetime.today().replace(microsecond=0)
