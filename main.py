# - *- coding: utf- 8 - *-
#check_update_bot
#on_startup_notify
#update_last_profit
#update_profit
#asyncio.create_task(update_last_profit())
#asyncio.create_task(check_update_bot())
import asyncio

from aiogram import executor

import filters
import middlewares
from handlers import dp
from utils.db_api.sqlite import create_bdx
from utils.set_bot_commands import set_default_commands

print("~~~~~ Бот был запущен ~~~~~")
async def on_startup(dp):
    await set_default_commands(dp)
    filters.setup(dp)
    middlewares.setup(dp)

    print("~~~~~ Бот был запущен ~~~~~")


if __name__ == "__main__":
    create_bdx()
    executor.start_polling(dp)
